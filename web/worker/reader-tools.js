// Shared by browser rendering and Node regression tests. No network or storage side effects.
export function filterFeed(items,filters={},today=new Date().toISOString().slice(0,10)){
 const text=String(filters.q||'').trim().toLocaleLowerCase();
 const days={'month':30,'quarter':90,'half':180,'year':365}[filters.period];
 const boundary=days?new Date(Date.parse(today+'T00:00:00Z')-days*86400000).toISOString().slice(0,10):null;
 const saved=new Set(filters.savedIds||[]);
 return items.filter(x=>(!text||[x.title,x.subtitle,x.summary].join(' ').toLocaleLowerCase().includes(text))&&(!filters.region||x.region===filters.region)&&(!filters.category||x.category===filters.category)&&(!filters.saved||saved.has(x.id))&&(!boundary||(x.coverage_end>=boundary&&x.coverage_end<=today))).sort((a,b)=>b.coverage_end.localeCompare(a.coverage_end)||a.id.localeCompare(b.id));
}
export function parseRoute(hash){
 const [path,search='']=hash.replace(/^#/,'').split('?');const params=new URLSearchParams(search);
 const match=/^\/story\/([a-z0-9][a-z0-9-]{0,119})$/.exec(path);
 return {view:path==='/new'?'new':path==='/workspace'?'workspace':path==='/review'?'review':path==='/timeline'?'timeline':match?'story':'feed',story:match?.[1]||params.get('story')||'',year:/^\d{4}$/.test(params.get('year')||'')?params.get('year'):'',month:/^(0[1-9]|1[0-2])$/.test(params.get('month')||'')?params.get('month'):''};
}
export function storyLink(id,year='',month=''){
 const p=new URLSearchParams();if(year)p.set('year',year);if(month)p.set('month',month);
 return '#/story/'+encodeURIComponent(id)+(p.size?'?'+p:'');
}
export const browserTools=[filterFeed,parseRoute,storyLink].map(f=>f.toString()).join('\n');
