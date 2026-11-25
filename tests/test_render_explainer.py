import importlib.util
import json
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest
import wave

SPEC = importlib.util.spec_from_file_location('render_explainer', Path(__file__).resolve().parents[1] / 'scripts/render_explainer.py')
exporter = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(exporter)
SAMPLE = {'title': 'Synthetic test only', 'scenes': [
    {'title': 'Recorded event', 'text': 'A fictional event has a qualified interpretation.', 'source_ids': ['test-one']},
    {'title': 'Limits', 'text': 'This example does not establish causation.', 'source_ids': []}]}


class ExportModelTests(unittest.TestCase):
    def test_script_rejects_missing_text_and_unsafe_source_ids(self):
        for bad in ({'title': 'x', 'scenes': []}, {'title': 'x', 'scenes': [{'title': 'a', 'text': 'b', 'source_ids': ['<script>']}]},
                    {'title': 'x', 'scenes': [{'title': 'a', 'text': ''}]}):
            with self.assertRaises(ValueError):
                exporter.validate_script(bad)

    def test_captions_cover_exact_duration_and_escape_markup(self):
        scene = {'title': 'Test', 'text': '<b>literal</b> & qualified', 'source_ids': []}
        captions = exporter.make_captions([scene], [75])
        self.assertTrue(captions.startswith('WEBVTT\n'))
        self.assertIn('00:00:00.000 --> 00:01:15.000', captions)
        self.assertIn('&lt;b&gt;literal&lt;/b&gt; &amp; qualified', captions)
        self.assertNotIn('<b>', captions)

    def test_duration_allocation_preserves_total_and_weights(self):
        values = exporter.allocate_durations(SAMPLE['scenes'], 75)
        self.assertAlmostEqual(sum(values), 75)
        self.assertGreater(values[0], values[1])
        with self.assertRaises(ValueError):
            exporter.allocate_durations(SAMPLE['scenes'], float('nan'))

    def test_transcript_keeps_original_qualifications_and_references(self):
        text = exporter.transcript(SAMPLE)
        for scene in SAMPLE['scenes']:
            self.assertIn(scene['text'], text)
        self.assertIn('test-one', text)

    def test_scene_audio_cannot_escape_input_directory_or_use_network(self):
        with tempfile.TemporaryDirectory() as root:
            base = Path(root) / 'input'
            base.mkdir()
            outside = Path(root) / 'outside.wav'
            outside.write_bytes(b'test')
            for path in ('../outside.wav', 'https://example.test/audio.wav'):
                with self.assertRaises(ValueError):
                    exporter.local_audio(path, base)


    @unittest.skipUnless(shutil.which('node'), 'Node is needed for the hosted caption contract check')
    def test_captions_pass_the_hosted_media_upload_validator(self):
        scene = {'title': 'Markup <literal>',
                 'text': 'Use https://example.test safely; no javascript: code > executes.', 'source_ids': []}
        captions = exporter.make_captions([scene], [75])
        module = (Path(__file__).resolve().parents[1] / 'web/worker/media-model.js').as_uri()
        code = ("import {validateCaptions} from " + json.dumps(module) + ";"
                "import {readFileSync} from 'node:fs';validateCaptions(readFileSync(0,'utf8'));"
                "process.stdout.write('accepted');")
        result = subprocess.run(['node', '--input-type=module', '-e', code], input=captions,
                                check=True, capture_output=True, text=True)
        self.assertEqual(result.stdout, 'accepted')


@unittest.skipUnless(shutil.which('ffmpeg') and shutil.which('ffprobe') and importlib.util.find_spec('PIL'),
                     'Video rendering requires Pillow, ffmpeg and ffprobe')
class RenderSmokeTests(unittest.TestCase):
    def test_actual_silent_mp4_and_traceable_sidecars(self):
        with tempfile.TemporaryDirectory() as root:
            directory = Path(root)
            source = directory / 'script.json'
            script = {**SAMPLE, 'story_id': 'synthetic-story', 'story_version': 7, 'version': 2,
                      'story_hash': 'immutable-story-hash', 'script_hash': 'explicit-script-hash',
                      'hash': 'legacy-script-hash', 'review_status': 'draft'}
            source.write_text(json.dumps(script))
            output = directory / 'story.mp4'
            metadata = exporter.render(source, output, duration=2)
            self.assertFalse(metadata['has_narration'])
            self.assertFalse(metadata['published'])
            self.assertEqual(metadata['story_id'], 'synthetic-story')
            self.assertEqual(metadata['story_version'], 7)
            self.assertEqual(metadata['story_hash'], 'immutable-story-hash')
            self.assertEqual(metadata['script_hash'], 'explicit-script-hash')
            self.assertEqual(metadata['input_review_status'], 'draft')
            saved_metadata = json.loads(output.with_suffix('.metadata.json').read_text())
            self.assertEqual(saved_metadata['script_hash'], 'explicit-script-hash')
            self.assertGreater(output.stat().st_size, 1000)
            self.assertEqual(metadata['files']['video']['sha256'], exporter.file_hash(output))
            probe = json.loads(subprocess.run(['ffprobe', '-v', 'error', '-show_streams', '-of', 'json', str(output)],
                                              check=True, capture_output=True, text=True).stdout)
            self.assertEqual([stream['codec_type'] for stream in probe['streams']], ['video'])
            self.assertIn('00:00:02.000', output.with_suffix('.vtt').read_text())
            self.assertIn(SAMPLE['scenes'][1]['text'], output.with_suffix('.transcript.txt').read_text())
            with self.assertRaises(ValueError):
                exporter.render(source, output, duration=2)

    def test_full_audio_duration_overrides_requested_duration(self):
        with tempfile.TemporaryDirectory() as root:
            directory = Path(root)
            source = directory / 'script.json'
            source.write_text(json.dumps({**SAMPLE, 'version': 3, 'hash': 'legacy-script-hash'}))
            audio = directory / 'narration.wav'
            with wave.open(str(audio), 'wb') as recording:
                recording.setnchannels(1)
                recording.setsampwidth(2)
                recording.setframerate(24000)
                recording.writeframes(b'\0\0' * 24000)
            output = directory / 'audio-story.mp4'
            metadata = exporter.render(source, output, duration=75, audio=audio)
            self.assertTrue(metadata['has_narration'])
            self.assertEqual(metadata['story_version'], 3)
            self.assertEqual(metadata['script_hash'], 'legacy-script-hash')
            self.assertAlmostEqual(metadata['duration_seconds'], 1, places=2)
            probe = json.loads(subprocess.run(['ffprobe', '-v', 'error', '-show_streams', '-of', 'json', str(output)],
                                              check=True, capture_output=True, text=True).stdout)
            self.assertEqual({stream['codec_type'] for stream in probe['streams']}, {'video', 'audio'})

    def test_per_scene_audio_uses_individual_measured_durations(self):
        with tempfile.TemporaryDirectory() as root:
            directory = Path(root)
            script = json.loads(json.dumps(SAMPLE))
            for index, scene in enumerate(script['scenes'], 1):
                audio = directory / f'chapter-{index}.wav'
                with wave.open(str(audio), 'wb') as recording:
                    recording.setnchannels(1)
                    recording.setsampwidth(2)
                    recording.setframerate(24000)
                    recording.writeframes(b'\0\0' * 24000 * index)
                scene['audio'] = audio.name
            source = directory / 'script.json'
            source.write_text(json.dumps(script))
            metadata = exporter.render(source, directory / 'chapters.mp4')
            self.assertEqual(metadata['scene_durations'], [1.0, 2.0])
            self.assertAlmostEqual(metadata['duration_seconds'], 3)
            self.assertTrue(metadata['has_narration'])
