#!/usr/bin/env python3
"""Collect public conference metadata for the 2026 speculative-decoding index."""
import concurrent.futures, html, json, pathlib, re, urllib.request, time
from html.parser import HTMLParser

ROOT=pathlib.Path(__file__).resolve().parent
class Links(HTMLParser):
    def __init__(self):super().__init__();self.a=None;self.rows=[]
    def handle_starttag(self,t,a):
        if t=='a':self.a=[dict(a).get('href',''),'']
    def handle_data(self,d):
        if self.a is not None:self.a[1]+=d
    def handle_endtag(self,t):
        if t=='a' and self.a is not None:self.rows.append(self.a);self.a=None
def plain(s):return ' '.join(html.unescape(re.sub('<[^>]+>',' ',s)).split())
def fetch(url):
    for attempt in range(3):
        try:
            req=urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0'})
            with urllib.request.urlopen(req,timeout=50) as r:return r.read().decode('utf-8',errors='replace')
        except Exception:
            if attempt==2:raise
            time.sleep(1)

EXCLUDE={
 'Draft-and-Audit Reinforcement Learning for Optimization Modeling':'优化建模的 draft-and-audit，不是解码加速',
 'SpecMD: A Comprehensive Study On Speculative Expert Prefetching':'MoE expert prefetching，不是 speculative decoding',
 'Speculative Safety Honeypot: Toward Proactive Defense Against Multi-turn Agent Attacks':'安全防御，不是 speculative decoding',
 'Speculative Sampling For Faster Molecular Dynamics':'分子动力学采样，不是语言或生成模型解码',
 'Towards Cold-Start Drafting and Continual Refining: A Value-Driven Memory Approach with Application to NPU Kernel Synthesis':'核函数合成的起草与改进，不是 token 解码加速',
 'FlowCast: Trajectory Forecasting for Scalable Zero-Cost Speculative Flow Matching':'连续 flow matching 加速，与 token speculative decoding 不同',
 'Synergizing Understanding and Generation with Interleaved Analyzing-Drafting Thinking':'多模态思维组织，不是 speculative decoding',
 'BEAGLE: Behavior-Enforced Agent for Grounded Learner Emulation':'EAGLE 关键词误命中',
 'LogicTree-RAG: Logic Tree-guided Retrieval-Augmented Generation for Long-form Patent Drafting':'专利起草，不是 speculative decoding',
 'MoE-SpAc: Efficient MoE Inference Based on Speculative Activation Utility in Heterogeneous Edge Scenario':'MoE activation 推测优化，不是 token speculative decoding',
}
def get_event(p):
    cache=ROOT/'sources_2026'/'events'/f"{p['conference']}-{p['url'].rsplit('/',1)[-1]}.html"
    try:
        s=cache.read_text() if cache.exists() else fetch(p['url'])
        if not cache.exists():cache.write_text(s)
        links=Links();links.feed(s)
        p['links']=[dict(url=u,text=plain(t)) for u,t in links.rows if any(x in u for x in ['openreview.net','arxiv.org','proceedings.','github.com'])]
        m=re.search(r'<div[^>]+class="abstract-text-inner"[^>]*>(.*?)</div>',s,re.S)
        if m:p['abstract']=plain(m.group(1))
        p['metadata_status']='ok' if p.get('abstract') else 'abstract not found'
    except Exception as e:p['metadata_status']=str(e)
    print(p['conference'],p['title'][:65],p['metadata_status'],flush=True)
    return p

if __name__=='__main__':
    (ROOT/'sources_2026'/'events').mkdir(parents=True,exist_ok=True)
    allrows=[]
    for name,domain in [('ICML','icml'),('ICLR','iclr'),('NeurIPS','neurips')]:
        s=pathlib.Path('/tmp/'+domain+'2026.html').read_text()
        (ROOT/'sources_2026'/f'{name}2026_downloads.html').write_text(s)
        links=Links();links.feed(s)
        for href,title in links.rows:
            title=plain(title)
            if re.search(r'speculat|draft|eagle|multi.token predict',title,re.I) and '/poster/' in href:
                allrows.append(dict(conference=name,title=title,url=href if href.startswith('http') else 'https://'+domain+'.cc'+href,
                    included=title not in EXCLUDE,exclusion_reason=EXCLUDE.get(title,'')))
    selected=[p for p in allrows if p['included']]
    with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool:results=list(pool.map(get_event,selected))
    (ROOT/'sources_2026'/'candidates.json').write_text(json.dumps(dict(search_date='2026-10-11',search_pattern='speculat|draft|eagle|multi.token predict',papers=results,excluded=[p for p in allrows if not p['included']]),ensure_ascii=False,indent=2)+'\n')
