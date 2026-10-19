#!/usr/bin/env python3
import concurrent.futures,json,urllib.request,re,pathlib,time,hashlib
from html import unescape
ROOT=pathlib.Path(__file__).resolve().parent;OUT=ROOT/'sources_2027';OUT.mkdir(exist_ok=True)
sha='5b07b9aa7c2c5fbca35a9f4bb765cf71c489dbf0';BASE=f'https://raw.githubusercontent.com/yzc-666/iclr2027-explorer/{sha}/'
cache=ROOT/'.git'/'literature_cache'/'iclr2027';cache.mkdir(exist_ok=True,parents=True)
def fetch(url):
 for attempt in range(3):
  try:return urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0'}),timeout=35).read()
  except Exception:
   if attempt==2:raise
   time.sleep(2)
meta=json.loads(fetch(BASE+'docs/data/meta.json'));rows=json.loads(fetch(BASE+'docs/data/papers.json'))
(OUT/'snapshot_meta.json').write_text(json.dumps(meta,ensure_ascii=False,indent=2)+'\n')
(OUT/'upstream_provenance.json').write_text(json.dumps({'source':'https://github.com/yzc-666/iclr2027-explorer','commit':sha,'snapshot_built':meta['built'],'retrieved_at':'2026-10-19','total_records':len(rows),'limitations':'第三方对公开 OpenReview 元数据的快照，非当前官方全量列表；状态截至快照日期。官方 API 本次返回 HTTP 403。'},ensure_ascii=False,indent=2)+'\n')
def shard(k):
 p=cache/f'{k}.json'
 if not p.exists():p.write_bytes(fetch(BASE+f'docs/data/abs/{k}.json'))
 return k,json.loads(p.read_text())
abstracts={}
with concurrent.futures.ThreadPoolExecutor(max_workers=6) as ex:
 for k,values in ex.map(shard,range((len(rows)+499)//500)):
  for i,a in enumerate(values):abstracts[k*500+i]=a
  if k%10==0:print('Abstract shards',k,flush=True)
pattern=r'speculat|draft(?:ing|er|ers)?|eagle|multi.token predict'
selected=[];abstract_only=[]
for i,row in enumerate(rows):
 title,keywords,abstract=row[2],row[3],abstracts[i]
 titlehit=bool(re.search(pattern,title,re.I));keyhit=bool(re.search(r'speculat(?:ive|ion)|multi.token predict',keywords,re.I))
 abshit=bool(re.search(r'speculative (?:decod|sampl)|draft(?:er|ing)',abstract[:600],re.I))
 if titlehit or keyhit or abshit:
  d=dict(id=row[0],number=row[1],title=title,keywords=keywords,status_at_snapshot=meta['statuses'][row[5]],abstract=abstract,index=i,source_url='https://openreview.net/forum?id='+row[0],discovery_source=BASE+'docs/data/papers.json',match_basis='title' if titlehit else 'keywords' if keyhit else 'abstract opening')
  selected.append(d)
  if not titlehit:abstract_only.append((d['id'],title,d['match_basis']))
(OUT/'search_candidates.json').write_text(json.dumps({'snapshot_total':len(rows),'retrieved_at':'2026-10-19','pattern':pattern,'candidates':selected},ensure_ascii=False,indent=2)+'\n')
print('ALL CANDIDATES',len(selected));print('ADDITIONAL',json.dumps(abstract_only,ensure_ascii=False),flush=True)
# Primary arXiv discovery: parse public search results, not secondary summaries.
arp=[]
for start in [0,200,400,600]:
 p=cache/f'arxiv-{start}.html'
 if p.exists():s=p.read_text()
 else:
  try:
   if not p.exists():p.write_bytes(fetch('https://arxiv.org/search/?query=speculative+decoding&searchtype=all&abstracts=show&order=-announced_date_first&size=200&start='+str(start)))
   s=p.read_text()
  except Exception as e:print('ARXIV SEARCH',start,str(e),flush=True);continue
 for block in re.split(r'<li class="arxiv-result">',s)[1:]:
  a=re.search(r'https://arxiv.org/abs/([\d.]+)',block);t=re.search(r'<p class="title is-5 mathjax">(.*?)</p>',block,re.S)
  if a and t:arp.append({'arxiv_id':a[1],'title':' '.join(unescape(re.sub('<[^>]*>',' ',t[1])).split()),'source_url':'https://arxiv.org/abs/'+a[1]})
 print('Arxiv metadata records',len(arp),flush=True)
(OUT/'arxiv_candidates.json').write_text(json.dumps(arp,ensure_ascii=False,indent=2)+'\n')
