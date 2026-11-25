#!/usr/bin/env python3
"""Render a source-linked storyboard to MP4, captions and traceable sidecars.

No network requests, generation, editorial approval, or publication occur here.
Pillow and the ffmpeg/ffprobe command-line tools are required for rendering.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path
import re
import shutil
import subprocess
import tempfile

MAX_INPUT_BYTES = 1_000_000
MAX_DURATION = 7200
WIDTH, HEIGHT, FPS = 1280, 720, 24


def require(condition, message):
    if not condition:
        raise ValueError(message)


def validate_script(value):
    require(isinstance(value, dict), "Storyboard must be a JSON object")
    require(isinstance(value.get("title"), str) and 0 < len(value["title"].strip()) <= 2000,
            "Provide a title up to 2000 characters")
    scenes = value.get("scenes")
    require(isinstance(scenes, list) and 1 <= len(scenes) <= 100, "Provide 1–100 scenes")
    for scene in scenes:
        require(isinstance(scene, dict), "Each scene must be an object")
        for key in ("title", "text"):
            require(isinstance(scene.get(key), str) and 0 < len(scene[key].strip()) <= 20_000,
                    "Scene titles and text must contain 1–20000 characters")
        refs = scene.get("source_ids", [])
        require(isinstance(refs, list) and len(refs) <= 100 and
                all(isinstance(ref, str) and re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_-]{0,119}", ref)
                    for ref in refs), "Invalid source IDs")
        if "audio" in scene:
            require(isinstance(scene["audio"], str) and scene["audio"], "Invalid scene audio path")
    return value


def load_script(path):
    require(path.is_file() and path.stat().st_size <= MAX_INPUT_BYTES, "Storyboard missing or too large")
    return validate_script(json.loads(path.read_text(encoding="utf-8")))


def local_audio(path, base=None):
    require(isinstance(path, (str, Path)) and "://" not in str(path) and "\x00" not in str(path),
            "Audio must be a local regular file")
    resolved = ((base / path) if base else Path(path)).resolve()
    if base:
        require(resolved.is_relative_to(base.resolve()), "Scene audio must stay inside the input directory")
    require(resolved.is_file() and resolved.stat().st_size <= 500_000_000,
            "Audio is missing or exceeds 500 MB")
    require(resolved.suffix.lower() in (".wav", ".mp3", ".m4a", ".aac", ".ogg", ".flac"),
            "Unsupported audio extension")
    return resolved


def run(args, timeout=300):
    return subprocess.run(args, check=True, capture_output=True, text=True, timeout=timeout)


def audio_duration(path):
    result = run(["ffprobe", "-v", "error", "-protocol_whitelist", "file,pipe", "-show_entries", "format=duration", "-of", "json", str(path)])
    duration = float(json.loads(result.stdout)["format"]["duration"])
    require(math.isfinite(duration) and 0 < duration <= MAX_DURATION, "Audio duration must be 0–7200 seconds")
    return duration


def word_count(text):
    return max(1, len(text.split()))


def allocate_durations(scenes, duration):
    require(math.isfinite(duration) and 1 <= duration <= MAX_DURATION, "Duration must be 1–7200 seconds")
    weights = [word_count(s["title"] + " " + s["text"]) for s in scenes]
    total = sum(weights)
    values = [duration * weight / total for weight in weights]
    require(min(values) >= 0.25, "Duration is too short to show every scene")
    return values


def transcript(script):
    # Every title/text is retained verbatim, including qualifications omitted from a short excerpt.
    return script["title"] + "\n\n" + "\n\n".join(
        scene["title"] + ". " + scene["text"] + "\nSources: " +
        (", ".join(scene.get("source_ids", [])) or "No additional source reference")
        for scene in script["scenes"]) + "\n"


def timestamp(seconds):
    millis = round(seconds * 1000)
    hours, remain = divmod(millis, 3_600_000)
    minutes, remain = divmod(remain, 60_000)
    secs, ms = divmod(remain, 1000)
    return f"{hours:02d}:{minutes:02d}:{secs:02d}.{ms:03d}"


def caption_text(text):
    # WebVTT markup delimiters and cue arrows cannot be interpreted as executable markup.
    escaped = text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    # The media upload contract reserves URI schemes even in otherwise harmless
    # caption text. Full original text is retained in the transcript sidecar.
    return re.sub(r"(?i)(https?|javascript):", lambda match: match.group(1) + "：", escaped)


def make_captions(scenes, durations):
    lines = ["WEBVTT", ""]
    elapsed = 0.0
    for scene, duration in zip(scenes, durations):
        words = (scene["title"] + ". " + scene["text"]).split()
        chunks = [words[index:index + 14] for index in range(0, len(words), 14)]
        offset = 0
        for chunk in chunks:
            start = elapsed + duration * offset / len(words)
            offset += len(chunk)
            end = elapsed + duration * offset / len(words)
            lines.extend([f"{timestamp(start)} --> {timestamp(end)}", caption_text(" ".join(chunk)), ""])
        elapsed += duration
    return "\n".join(lines)


def font(size, heading=False):
    from PIL import ImageFont
    candidates = (["/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"] if heading else []) + [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/liberation2/LiberationSans-Regular.ttf"]
    for path in candidates:
        if Path(path).is_file():
            return ImageFont.truetype(path, size)
    return ImageFont.load_default(size=size)


def wrap(draw, text, selected_font, width):
    words = text.split()
    lines, line = [], ""
    for word in words:
        if draw.textlength(word, font=selected_font) > width:
            # Bound pathological unbroken tokens without silently dropping them.
            for char in word:
                if draw.textlength(line + char, font=selected_font) > width:
                    lines.append(line)
                    line = ""
                line += char
            continue
        candidate = line + (" " if line else "") + word
        if line and draw.textlength(candidate, font=selected_font) > width:
            lines.append(line)
            line = word
        else:
            line = candidate
    if line:
        lines.append(line)
    return lines or [""]


def render_frames(script, durations, directory, has_audio):
    from PIL import Image, ImageDraw
    entries = []
    for number, (scene, duration) in enumerate(zip(script["scenes"], durations), 1):
        dummy = ImageDraw.Draw(Image.new("RGB", (WIDTH, HEIGHT)))
        title_lines = wrap(dummy, scene["title"], font(36, True), 1110)
        require(len(title_lines) <= 3, "Scene title exceeds three slide lines; shorten the title")
        body_lines = wrap(dummy, scene["text"], font(29), 1110)
        pages = [body_lines[i:i + 8] for i in range(0, len(body_lines), 8)]
        page_words = [word_count(" ".join(page)) for page in pages]
        for page_number, page in enumerate(pages, 1):
            image = Image.new("RGB", (WIDTH, HEIGHT), "#f4f7f3")
            draw = ImageDraw.Draw(image)
            draw.rectangle((0, 0, WIDTH, 12), fill="#226645")
            draw.text((65, 35), "EPSTMC · VISUAL EXPLANATION", font=font(20), fill="#52695c")
            for line_index, line in enumerate(title_lines):
                draw.text((65, 86 + line_index * 44), line, font=font(36, True), fill="#173d2e")
            body_y = 100 + len(title_lines) * 44
            for line_index, line in enumerate(page):
                draw.text((65, body_y + line_index * 39), line, font=font(29), fill="#173d2e")
            refs = ", ".join(scene.get("source_ids", [])) or "See story coverage limits"
            for line_index, line in enumerate(wrap(draw, "Sources: " + refs, font(17), 1110)[:2]):
                draw.text((65, 595 + line_index * 23), line, font=font(17), fill="#52695c")
            disclosure = "Narration supplied · source-linked storyboard" if has_audio else "Silent captioned storyboard · no generated narration"
            draw.text((65, 655), disclosure, font=font(18), fill="#52695c")
            draw.text((1100, 655), f"{number}/{len(durations)} · {page_number}/{len(pages)}",
                      font=font(17), fill="#52695c")
            path = directory / f"scene-{number:03d}-{page_number:03d}.png"
            image.save(path)
            entries.append((path, duration * page_words[page_number - 1] / sum(page_words)))
    return entries


def file_hash(path):
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for chunk in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def render(input_path, output_path, duration=75.0, audio=None, overwrite=False):
    require(shutil.which("ffmpeg") and shutil.which("ffprobe"), "Install ffmpeg and ffprobe")
    input_path = Path(input_path).resolve()
    output_path = Path(output_path).resolve()
    require(output_path.suffix.lower() == ".mp4", "Output must end in .mp4")
    require(input_path != output_path, "Output cannot replace the input")
    sidecars = {"captions": output_path.with_suffix(".vtt"),
                "transcript": output_path.with_suffix(".transcript.txt"),
                "metadata": output_path.with_suffix(".metadata.json")}
    require(input_path not in sidecars.values(), "Output sidecars cannot replace the input")
    if not overwrite:
        require(not any(p.exists() for p in [output_path, *sidecars.values()]),
                "Output already exists; pass --overwrite to replace it")
    script = load_script(input_path)
    scene_audio = [scene.get("audio") for scene in script["scenes"]]
    require(not audio or not any(scene_audio), "Choose full recording or scene recordings, not both")
    if any(scene_audio):
        require(all(scene_audio), "Every scene needs audio when per-scene recordings are used")
    audio_paths = [local_audio(item, input_path.parent) for item in scene_audio] if all(scene_audio) else []
    full_audio = local_audio(audio) if audio else None
    if audio_paths:
        durations = [audio_duration(path) for path in audio_paths]
    else:
        durations = allocate_durations(script["scenes"], audio_duration(full_audio) if full_audio else duration)
    actual_duration = sum(durations)
    require(actual_duration <= MAX_DURATION, "Combined duration exceeds 7200 seconds")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="epstmc-video-") as temp:
        directory = Path(temp)
        audio_file = full_audio
        if audio_paths:
            # Decode each recording to a fixed PCM format, then concatenate generated safe paths.
            decoded = []
            for i, source in enumerate(audio_paths):
                target = directory / f"audio-{i:03d}.wav"
                run(["ffmpeg", "-nostdin", "-v", "error", "-protocol_whitelist", "file,pipe", "-i", str(source), "-vn", "-ar", "24000",
                     "-ac", "1", "-c:a", "pcm_s16le", str(target)])
                decoded.append(target)
            manifest = directory / "audio.txt"
            manifest.write_text("".join(f"file '{p.name}'\n" for p in decoded), encoding="utf-8")
            audio_file = directory / "narration.wav"
            run(["ffmpeg", "-nostdin", "-v", "error", "-protocol_whitelist", "file,pipe", "-f", "concat", "-safe", "1", "-i", str(manifest),
                 "-c:a", "pcm_s16le", str(audio_file)])
        entries = render_frames(script, durations, directory, bool(audio_file))
        manifest = directory / "frames.txt"
        manifest.write_text("".join(f"file '{p.name}'\nduration {seconds:.9f}\n" for p, seconds in entries)
                            + f"file '{entries[-1][0].name}'\n", encoding="utf-8")
        rendered = directory / "rendered.mp4"
        args = ["ffmpeg", "-nostdin", "-v", "error", "-protocol_whitelist", "file,pipe", "-f", "concat", "-safe", "1", "-i", str(manifest)]
        if audio_file:
            args += ["-protocol_whitelist", "file,pipe", "-i", str(audio_file), "-map", "0:v:0", "-map", "1:a:0", "-c:a", "aac", "-b:a", "128k"]
        args += ["-c:v", "libx264", "-preset", "veryfast", "-pix_fmt", "yuv420p", "-r", str(FPS),
                 "-t", f"{actual_duration:.6f}", "-movflags", "+faststart", str(rendered)]
        run(args, timeout=max(300, actual_duration * 3))
        shutil.copyfile(rendered, output_path)
    sidecars["captions"].write_text(make_captions(script["scenes"], durations), encoding="utf-8")
    sidecars["transcript"].write_text(transcript(script), encoding="utf-8")
    word_total = sum(word_count(s["title"] + " " + s["text"]) for s in script["scenes"])
    metadata = {"status": "requires_editorial_review", "published": False,
                "title": script["title"], "duration_seconds": actual_duration,
                "scene_durations": durations, "has_narration": bool(audio_paths or full_audio),
                "narration_origin": "supplied_recording" if audio_paths or full_audio else "none",
                "disclosure": "Captioned source-linked storyboard; not documentary footage. " +
                              ("Narration supplied by operator; provenance must be reviewed." if audio_paths or full_audio
                               else "Silent video; no AI-generated voice is claimed."),
                "readability_warning": actual_duration < word_total / 3,
                "recommended_minimum_seconds": math.ceil(word_total / 3),
                "story_id": script.get("story_id"),
                "story_version": script.get("story_version", script.get("version")),
                "story_hash": script.get("story_hash"),
                "script_hash": script.get("script_hash", script.get("hash")),
                "input_review_status": script.get("review_status"),
                "input_sha256": file_hash(input_path),
                "source_ids": sorted({ref for s in script["scenes"] for ref in s.get("source_ids", [])}),
                "files": {key: {"name": path.name, "sha256": file_hash(path)}
                          for key, path in {"video": output_path, "captions": sidecars["captions"],
                                            "transcript": sidecars["transcript"]}.items()}}
    sidecars["metadata"].write_text(json.dumps(metadata, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return metadata


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path, help="JSON storyboard exported from the private media studio")
    parser.add_argument("output", type=Path, help="Destination .mp4")
    parser.add_argument("--duration", type=float, default=75, help="Silent video seconds (default: 75)")
    parser.add_argument("--audio", type=Path, help="Optional full local narration; measured duration overrides --duration")
    parser.add_argument("--overwrite", action="store_true")
    args = parser.parse_args()
    try:
        metadata = render(args.input, args.output, args.duration, args.audio, args.overwrite)
    except (ValueError, OSError, subprocess.SubprocessError, KeyError) as error:
        parser.exit(1, f"Video export failed: {error}\n")
    print(json.dumps({"video": str(args.output.resolve()), "duration_seconds": metadata["duration_seconds"],
                      "has_narration": metadata["has_narration"], "status": metadata["status"],
                      "readability_warning": metadata["readability_warning"]}))


if __name__ == "__main__":
    main()
