#!/usr/bin/env python3
"""Integrate the new snapshot without replacing older paper notes or PDF provenance."""
import collections,csv,datetime,json,pathlib,re
from collect_2027 import NEW_CATEGORIES,WHY
ROOT=pathlib.Path(__file__).resolve().parent
def read(name):return json.loads((ROOT/name).read_text())
def write(name,v):(ROOT/name).write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
SPECIAL={
 'DLite':'复用目标上下文隐藏状态，以无历史并行骨干和轻量顺序头起草，减少 Agent 多轮长上下文中的草稿历史 KV 开销；不是工具动作级推测。',
 'JetSpec':'针对并行块草稿与候选树之间的条件依赖矛盾，研究因果并行树起草；与单纯增加候选节点预算分开比较。',
 'H-Spec':'研究不维护草稿端历史 KV 的并行推测起草，与 DLite 的历史依赖问题可以对照。',
 'SpecSplice':'把参数草稿与检索片段放入共同节点预算，在多个草稿节点处选择拼接；属于 Agentic token 级候选构建。',
 'AgSpec':'利用代码 Agent 流程中的可复用片段构建检索草稿；属于 token 级加速，不是提前执行真实工具。',
 'SpecSys':'面向 Agentic 多轮 LLM 服务，结合选择性 SD 和完成感知调度；需区分模型调用与完整任务耗时。',
 'MoE-Spec':'验证时给专家加载设置预算；作者明确讨论速度与质量权衡，不能标为严格保留完整 MoE 目标分布。',
 'GhostToolCalls':'关注推测工具调用在发出时已经泄露信息的问题；回滚本地状态无法撤回外部服务已经观察到的请求。',
 'D-Loop':'研究循环式扩散起草；与已有 DLoop: Looped Speculative Decoding 的 OpenReview ID、题名和预印本均不同，分别保留。',
 'SMC-SD':'以粒子重要性加权和重采样代替逐 token 首拒绝；作者将其定位为具有误差界的近似方案，并非精确 SD。',
}

def pdfcell(p,relative=''):
 return f"[PDF]({relative+p['pdf_file']})" if p.get('pdf_file') and p.get('status')=='downloaded' else '待补'

if __name__=='__main__':
 exp=read('conference_2027_manifest.json');papers=exp['papers'];layout=read('classification_manifest.json');base=read('papers_manifest.json')
 cats={c['directory']:c for c in layout['categories']}
 for d,n,description in NEW_CATEGORIES:cats[d]=dict(directory=d,name=n,description=description)
 records={p['folder']:p for p in layout['papers']};merged={p['folder']:p for p in base['papers']}
 for p in papers:
  p['summary_zh']=SPECIAL.get(p['acronym'],p['summary_zh'])
  p['output_guarantee']='尚未逐篇独立核查；须区别目标采样分布、贪心输出一致、语义质量及工具轨迹保证。'
  if p['id']=='FFeFbTdmFb':p['status_observation']='10/7 镜像为 active；另见官方搜索缓存显示 Withdrawn Submission（10/11），当前状态仍待实时复核。';p['status_observation_url']='https://openreview.net/search?content=authors&group=all&sort=cdate%3Adesc&source=forum&term=~Yuxuan_Zhou2'
  if p['id']=='NcnAlaUt76':p['pdf_source_note']='复用迁移前用户提供的原始 PDF；未重新下载，也不根据候选链接反推实际文件来源。';p.pop('download_url',None)
  d=ROOT/p['directory_path'];d.mkdir(exist_ok=True,parents=True)
  record={'folder':p['folder'],'title':p['title'],'primary_category':p['primary_category'],'original_category':p['category'],'directory_path':p['directory_path'],'basis':p['classification_basis'],'secondary_topics':p['secondary_topics'],'kind':'paper'}
  # Existing DLoop notes are retained; only attach the new snapshot metadata.
  if p['id']!='NcnAlaUt76':
   text=f"# {p['title']}\n\n## 1. 来源与状态\n\n- OpenReview ID：`{p['id']}`，投稿编号：{p['number']}。\n- [投稿页面]({p['source_url']})；{p['venue_status']}。\n- 发现依据：[公开元数据镜像](https://github.com/yzc-666/iclr2027-explorer)，2026-10-07 快照；当前官方 API 返回 HTTP 403。\n- 快照状态：`{p['status_at_snapshot']}`；它不表示今天的实时状态。\n"
   if p.get('arxiv_id'):text+=f"- [作者预印本](https://arxiv.org/abs/{p['arxiv_id']})；arXiv 与投稿版本可能不同。\n"
   if p.get('pdf_searches'):text+='- PDF 补充检索：2026-10-19 已按完整题名检索；未下载条目另按方法名与辨识词补搜。检索失败不能推断论文没有公开 PDF。\n'
   if p.get('title_version_note'):text+=f"- 版本对应说明：{p['title_version_note']}\n"
   if p.get('status_observation'):text+=f"- 状态差异：{p['status_observation']} [观察来源]({p['status_observation_url']})。\n"
   text+=f"\n## 2. 分类与定位\n\n主分类：**{p['primary_category']}**。\n\n{p['summary_zh']}\n\n分类依据：{p['classification_basis']}\n\n交叉主题：{', '.join(p['secondary_topics']) or '未单独标注'}。这是题名与摘要的初筛分类，尚未逐篇重新精读全文；目录采用主要贡献，其余主题交叉标记。描述性目录简称不一定是作者给定的方法缩写。\n\n## 3. 本地文件与证据边界\n\n"
   if p['status']=='downloaded':
    text+=f"[阅读 PDF]({pathlib.Path(p['pdf_file']).name})，{p['pages']} 页。文件头、`pdfinfo` 与 SHA-256 已核查。标题核对采用元数据匹配与首页词项覆盖检查，不表示独立复现全部论文实验。\n\nSHA-256：`{p['sha256']}`。\n"
    if p.get('download_url'):text+=f"\n[文件下载来源]({p['download_url']})。\n"
   else:text+='**已检索，尚未下载成功；不表示论文没有公开 PDF。** 当前环境访问 OpenReview 会遇到 HTTP 403 或浏览器验证；公开页面、作者预印本和下载文件分别记录。未取得可校验文件时保持待补，不以网页或其他论文替代。逐条检索与请求记录保存在 `conference_2027_manifest.json` 和根目录 `sources_2027/pdf_search_2026-10-19.json`。\n'
   text+='\n输出保证：'+p['output_guarantee']+'\n'
   if p['id']=='UwMYxYHQSG':text+='\n## 4. 进一步阅读\n\n[定位与阅读笔记](定位与阅读笔记.md)：token 级与动作级区别、历史 KV、训练方式，以及 Agentic 评测的时间口径。\n'
   (d/'README.md').write_text(text)
  records[p['folder']]=record
  if p['folder'] in merged and merged[p['folder']].get('id')!=p['id']:
   previous=merged[p['folder']];previous['iclr2027_submission']=p
  else:merged[p['folder']]=p
 layout.update(organized_at='2026-10-19',scope='原有分类文献与用户授权新增的 ICLR2027 公开投稿快照候选；所有投稿状态与下载状态分别记录。',basis='已有记录保持；新条目依据题名、关键词与摘要初筛，DLite 另核查公开 PDF 正文和评测附录。',categories=list(cats.values()),papers=list(records.values()))
 base.update(updated_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),papers=list(merged.values()),iclr2027_index='ICLR2027.md')
 write('classification_manifest.json',layout);write('papers_manifest.json',base);write('conference_2027_manifest.json',exp)
 downloaded=sum(p['status']=='downloaded' for p in papers);new=sum(not p['existing_in_library'] for p in papers)
 intro=f'''# ICLR 2027 推测解码与相关推测执行论文

## 1. 检索范围与可确认程度

检索日期：2026-10-19。官方入口：[ICLR 2027 OpenReview](https://openreview.net/group?id=ICLR.cc/2027/Conference)。本次官方页面/API/PDF 返回 HTTP 403 或浏览器验证，无法直接导出今天的完整官方列表；ICLR 官网 2027 Downloads 页也没有论文条目。

因此扫描了第三方 [iclr2027-explorer](https://github.com/yzc-666/iclr2027-explorer) 对公开 OpenReview 元数据的固定快照：commit `5b07b9aa7c2c5fbca35a9f4bb765cf71c489dbf0`，构建日期 **2026-10-07**，共 **43,013 条记录**。按题名、关键词和摘要开头筛出 **{exp['candidates']} 条候选**，排除 **{exp['excluded']} 条**，本批保留 **{len(papers)} 条**，其中 **{downloaded} 篇有本地 PDF，{len(papers)-downloaded} 篇待补**。已有 DLoop 去重保留，新增 {new} 条。

**这是公开快照的系统检索，不是当前 ICLR 2027 官方全量完整性声明。** 快照之后的新增、改题、撤稿和 desk reject 可能未反映；所有 `ICLR2027-*` 是投稿来源标识，不能理解为录用。PDF 可为作者 arXiv 版本。部分相邻工作是动作／工具级推测、训练或连续生成，不全是经典 LLM token SD。

去重以完整题名与 OpenReview ID 为主，不按简称合并；`DLoop` / `D-Loop`、两篇 TreeSpark、两篇 ProSpect 分别保留。存在预印本改题而未被精确题名检索匹配的可能，不能据本次未下载推断没有公开 PDF。

## 2. DLite 与 Agentic 方向

- **DLite**：[笔记](03_并行与半自回归草稿/ICLR2027-DLite/定位与阅读笔记.md)。主贡献是无历史的半自回归 token drafter，Agentic 是应用负载，故主目录在 `03`；`15` 中交叉链接。
- **Agentic token 级 SD**：DLite、SpecSplice、AgSpec、SchemaFill 等，解决一次模型调用内部的生成成本。
- **Agentic 服务与 rollout**：SpecSys、Agent Turns Are Not Chat Turns、RANA 等，解决多轮请求、验证预算和 RL 生成成本。
- **动作／工具／轨迹级推测**：SpecRoute、DualSpec、ProSpect-MAS、LEAP、ObsSpec 等，验证的是未来动作、观察或轨迹；需分别核查回滚、外部副作用和保证。

DLite 附录的 BFCL 统计不计工具执行时间；其 acceptance length 也不是端到端 speedup。不要把 token 或模型调用加速直接等同完整 Agent 任务提速。

## 3. 新增分类

| 目录 | 适用内容 |
| --- | --- |
'''
 for d,n,description in NEW_CATEGORIES:intro+=f'| [{d}]({d}/README.md) | {description} |\n'
 intro+='\n## 4. 按主要贡献浏览\n'
 section=0
 for category in cats.values():
  group=[p for p in papers if p['primary_category']==category['name']]
  if not group:continue
  section+=1
  intro+=f"\n### 4.{section} {category['name']}（{len(group)} 条）\n\n| 论文 | 本地 PDF | 初步定位 |\n| --- | --- | --- |\n"
  for p in group:intro+=f"| [{p['title']}]({p['directory_path']}/README.md) | {pdfcell(p)} | {p['summary_zh']} |\n"
 intro+='\n## 5. PDF 待补与排除记录\n\n待补条目已经建立 README，正文记录当前下载限制；不是已完成 PDF 收集的条目。\n\n| 投稿编号 | 论文 | OpenReview |\n| --- | --- | --- |\n'
 for p in papers:
  if p['status']!='downloaded':intro+=f"| {p['number']} | [{p['title']}]({p['directory_path']}/README.md) | [链接]({p['source_url']}) |\n"
 intro+='\n完整初筛：[search_candidates.json](sources_2027/search_candidates.json)。逐条排除：[excluded.json](sources_2027/excluded.json)。保留清单与下载记录：[conference_2027_manifest.json](conference_2027_manifest.json)。快照出处：[upstream_provenance.json](sources_2027/upstream_provenance.json)。\n\n补充 PDF 检索：[完整题名检索](sources_2027/pdf_search_2026-10-19.json)、[方法名与辨识词补搜](sources_2027/pdf_search_short_2026-10-19.json)。待补表示本地没有取得文件，不表示该公开投稿没有 PDF。\n\n## 6. 后续维护\n\n`discover_2027.py` 复现固定快照与 arXiv 发现过程；`collect_2027.py` 复用已有 PDF 并补下载；`render_2027.py` 合并记录和更新分类。重新访问的快照日期与实时状态必须分别记录。当前分类为初筛导航，并非论文性能排序。\n'
 (ROOT/'ICLR2027.md').write_text(intro)
 # Rebuild category indexes from authoritative layout while keeping individual older notes.
 for c in cats.values():
  d=ROOT/c['directory'];d.mkdir(exist_ok=True);rows=[p for p in records.values() if p['primary_category']==c['name']]
  text=f"# {c['name']}\n\n{c['description']}\n\n[全部分类](../CLASSIFICATION.md) · [ICLR2027 扩展](../ICLR2027.md)\n\n| 论文 | PDF | 分类依据 |\n| --- | --- | --- |\n"
  for p in rows:
   mp=merged.get(p['folder'],{});pdf=mp.get('pdf_file')
   if not pdf:pdf=next((x.get('pdf_file') for x in papers if x['folder']==p['folder']),None)
   cell=f"[PDF]({pathlib.Path(pdf).relative_to(c['directory'])})" if pdf else '博客' if p['kind']=='blog' else '待补'
   text+=f"| [{p['title']}]({pathlib.Path(p['directory_path']).name}/README.md) | {cell} | {p['basis']} |\n"
  if c['directory'].startswith('15_'):
   text+='\n## 交叉阅读：Agentic token 级推测解码\n\n以下论文主目录按算法贡献组织，服务 Agentic 负载，不重复存 PDF：\n\n'
   for p in papers:
    if 'Agentic' in p['secondary_topics'] and p['primary_category']!=c['name']:text+=f"- [{p['title']}](../{p['directory_path']}/README.md)，主分类：{p['primary_category']}。\n"
  (d/'README.md').write_text(text)
 totalpaper=sum(p['kind']=='paper' for p in records.values());totalpdf=sum(bool(p.get('pdf_file')) and p.get('status')=='downloaded' for p in merged.values())
 text='# 推测解码文献研究方向分类\n\n按主要贡献分配唯一物理目录，交叉主题在逐篇记录和各类索引说明。ICLR2027 新条目来自公开投稿快照，不表示录用；检索边界见 [ICLR2027.md](ICLR2027.md)。\n\n| 类别 | 论文 | 已有 PDF | 待补 PDF | 博客 |\n| --- | ---: | ---: | ---: | ---: |\n'
 for c in cats.values():
  group=[p for p in records.values() if p['primary_category']==c['name']];paper=[p for p in group if p['kind']=='paper'];yes=sum(merged.get(p['folder'],{}).get('status')=='downloaded' for p in paper)
  text+=f"| [{c['name']}]({c['directory']}/README.md) | {len(paper)} | {yes} | {len(paper)-yes} | {len(group)-len(paper)} |\n"
 text+=f'\n合计 {totalpaper} 篇论文，{totalpdf} 篇有 PDF，{totalpaper-totalpdf} 篇待补；另有 1 项官方博客。分类是研究导航，不是逐篇全文评审。\n\n`folder` 为稳定标识，`directory_path` 为物理路径。详见 [classification_manifest.json](classification_manifest.json)、[papers_manifest.json](papers_manifest.json)、[papers.csv](papers.csv)。\n'
 (ROOT/'CLASSIFICATION.md').write_text(text)
 fields=['folder','title','primary_category','category','directory_path','scope','venue_status','source_url','venue_evidence_url','pdf_file','status','pages','sha256','summary_zh','relation']
 with (ROOT/'papers.csv').open('w',newline='') as f:
  w=csv.DictWriter(f,fieldnames=fields,extrasaction='ignore');w.writeheader();w.writerows(merged.values())
 path=ROOT/'README.md';s=path.read_text();start='<!-- ICLR2027 START -->';end='<!-- ICLR2027 END -->'
 banner=f'{start}\n\nICLR2027 扩展：[分类检索索引](ICLR2027.md)。本批保留 {len(papers)} 条，{downloaded} 篇已有 PDF；当前文献库 {totalpaper} 篇论文、{totalpdf} 篇已有 PDF。投稿状态与覆盖范围以索引中的快照说明为准。\n\n{end}\n'
 if start in s:s=re.sub(re.escape(start)+'.*?'+re.escape(end)+'\n?',lambda m:banner,s,flags=re.S)
 else:s=s.replace('\n','\n\n'+banner,1)
 s=s.replace('合并文献库共 122 篇，106 篇已有 PDF。','当时合并文献库为 122 篇、106 篇 PDF（历史统计；最新总数见上方 ICLR2027 扩展）。')
 path.write_text(s)
 print('Integrated',len(papers),'records;',downloaded,'PDFs;',totalpaper,'total papers;',totalpdf,'total PDFs')
