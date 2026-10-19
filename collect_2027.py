#!/usr/bin/env python3
"""Curate the pinned public ICLR 2027 metadata snapshot; retrieve verifiable PDFs."""
import concurrent.futures, datetime, hashlib, json, pathlib, re, subprocess, urllib.request

ROOT=pathlib.Path(__file__).resolve().parent
SRC=ROOT/'sources_2027'
def read(name):return json.loads((ROOT/name).read_text())
def write(name,value):(ROOT/name).write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n')
def norm(title):return re.sub('[^a-z0-9]','',title.lower())

# Explicitly reviewed keyword false positives, and adjacent topics not about verification.
EXCLUDED={
 'UGc6uujZga':'时间序列分解与预测，同名 DrafTS；不是 token SD。',
 '61HXPpMUbe':'节点起草的稀疏注意力求解器，不是语言模型候选验证。',
 'x23LuMrBJo':'kernel runtime 搜索中的性能代理，不是 SD 解码。',
 'gqKba6Tu8o':'EagleDepth 为深度估计，与 EAGLE 草稿无关。',
 'XsjVbnJrSb':'潜在通信研究，题名 Draft-KV 不代表推测解码。',
 'Et89lO3Lc2':'多模态持续训练的修订策略，不是推测解码。',
 'DBtNko6b1g':'时间序列滚动预测；本批不扩展到预测任务。',
 'ZoVv8NH8sp':'视频扩散注意力加速，不是 token draft-verify。',
 'LYN8fCpi7x':'临床试验方案的修订审核，不是解码。',
 'YeAi9Rg38D':'机械工程图生成，同名 DraftCoder。',
 'amQcxOqzIY':'事实检索与拒答训练，同名 DRAFT。',
 'Ec6B7E1neG':'专利文稿起草，不是推测解码。',
 'dtN2B8UsPq':'fMRI 三维场景重建，同名 DRAFT。',
 'mGSMbbW7pH':'多边形监督定位，同名 EAGLE。',
 'Y5ado2U5C3':'全景主动探索，同名 EAGLE。',
 'Qask3lw679':'图像评估，同名 EAGLE。',
 'VoJ8FflwBk':'提示注入的指令搜索，不是解码加速。',
 'sehaQUasEF':'专家预取而非多 token 起草验证，另列排除理由。',
 'LOHzPGrcTQ':'科学发现的多模型进化搜索，非解码或 Agent 未来动作验证。',
 'hWV7TkZ7dW':'评测预算分配中的推测执行，不是解码。',
 'SbFIIt33md':'学习离散扩散噪声过程，re-draft 指去噪修订。',
 'XzlNiYoA7t':'图像编辑的计算复用和长度控制，未构成 SD 验证流程。',
 '1jtNAI8NRC':'并行答案修订的独立生成模型，未以 SD 为主要贡献。',
}
EXTRA_KEEP=set('M4lxTHfZHj mQIHtKbJrZ TKYYT98LKw qZ176Ev65f eg1MphIBtj YRpiRnJeC8 lL6IKLZdCX G5Ax2k2mjo Cgc1uAuMYB S3CaLwxU71 8bCJW8E9CL IgVNSa3MMg I1Sut8QpwJ T88NIhdQ1C CiGvIrGXUa iMoFWHnnRd FSBDGqCv9R K41WlEJtX8 R1TOtlmjpw WpiyhmR6zw'.split())
ALIASES={'UwMYxYHQSG':'DLite','NcnAlaUt76':'DLoop','YMW2yV59lg':'D-Loop','UkPe6Ut18a':'LongSpark','lL6IKLZdCX':'AS2D','G5Ax2k2mjo':'SMC-SD','rWgGD1hBwD':'TreeSpark-Control','43QYHpZo5A':'ProSpect-MAS','jTkVGBz5LX':'ProSpect-Self','FdEDds2GWP':'EAGLE3-Training','B0oyr1Zdjv':'OnPolicyEAL','zZTxv5Sv9h':'ExpectedRounds','iMoFWHnnRd':'APD-GR','e9RG7RBDSX':'Cadence','6LPQVnHdF5':'FactorizationGuided','V295SYnVAe':'PC-VOT','EunYNl4pfs':'ShortContextDrafters','kPogpAbOGS':'EntropyDraftVerify','t8Np0RnNQh':'SpecFlow','cLL6ddjWCC':'BlockVerificationSCD'}
ARXIV_OVERRIDES={'UwMYxYHQSG':'2610.23787','UkPe6Ut18a':'2609.37029','lL6IKLZdCX':'2609.37617','BnqJcRBl9D':'2602.16052'}
OVERRIDES={'UwMYxYHQSG':'03','NcnAlaUt76':'07','YMW2yV59lg':'07','oh483ijJht':'20','Dn1SZLx0Bh':'20','t7ryJLliBv':'20','QBdP6DyGVr':'09','5ayx4zhVDh':'09','K41WlEJtX8':'15','FkzxNKRNI0':'08','t8Np0RnNQh':'21','kPogpAbOGS':'21','S3CaLwxU71':'21','FdEDds2GWP':'02','mgQmqz3bom':'10','IuKihTs9rn':'09','iMoFWHnnRd':'22','R1TOtlmjpw':'13','mQIHtKbJrZ':'18','cKG5DrtVDm':'10','rZc9uOU2OO':'16','UbyKrDh0jN':'16','TKYYT98LKw':'16','HEZO4VeU6W':'17','96mkAG7gh1':'17','VHD7PibsBE':'15','PkRfbBnIf4':'15'}
NEW_CATEGORIES=[
 ('18_MoE与混合架构','MoE与混合架构','专家路由、专家加载、混合注意力／递归状态及其推测验证；区别于单纯专家预取。'),
 ('19_安全隐私与水印','安全隐私与水印','推测解码攻击面、放宽验证的安全影响、工具调用隐私与采样水印。'),
 ('20_检索与复用草稿','检索与复用草稿','n-gram、上下文复制、轨迹检索、历史后缀复用和参数／检索混合草稿。'),
 ('21_连续生成与熵解码','连续生成与熵解码','相邻方向：连续 flow/diffusion 的推测积分和压缩熵解码；不混同离散 LLM token SD。'),
 ('22_生成式推荐','生成式推荐','在生成式推荐语义标识符、候选验证或 beam 解码中的推测加速。'),
]
OVERRIDES.update({
 'CeYnTqMlWL':'13','I5CQFZWM7f':'13','2Ql5mfYaVv':'19','G5Ax2k2mjo':'08',
 'tfUX1UoIAX':'15','3rRLnNk2BP':'02','5IQp6EOHry':'02','mXaSfeDwq2':'02',
 'LTnds9XemH':'03','Cgc1uAuMYB':'05','6lDsDQnFPa':'03','6WsGHOtGMQ':'03',
 'pqPZjf4pqE':'02','yon1mWbqC5':'04','sO6appZlV6':'04','vcjhJyxMes':'04',
 'KdJAQNozHX':'17','ZOZCV5K6hs':'17','YRpiRnJeC8':'17','SXB8VD2tdY':'17',
 'Ty1kT3NAss':'16','SPM8WSZyeY':'16','ki673uxHST':'16','T0dAyKIH7J':'09',
 'KolakFzUpK':'04','Ahc6GUSVu3':'03','JmFYQ7GRSr':'06','3EoH49TYLt':'06',
 '4skcCpqFmE':'05','WLStKyK5Qp':'16',
 'FYP80cTIdc':'03','mQO2CZs8Xq':'03','XTxvmGn75Z':'13',
})
WHY={'02':'主要问题是草稿表征、训练目标、蒸馏或在线适配。','03':'主要问题是块内并行预测、半自回归依赖或并行草稿结构。','04':'主要问题是候选树、多路径组织、采样耦合或验证机制。','05':'主要问题是复用目标模型、跳层或自推测。','06':'主要问题是起草长度、预算控制、执行重叠或回滚调度。','07':'主要问题是跨块起草或一次验证前的循环／多轮起草。','08':'涉及语义接受、近似验证、修改目标或质量与速度权衡，不能直接视为分布保持。','09':'主要问题是吞吐、请求调度、系统执行或 RL rollout。','10':'主要贡献是理论、误差分析、基准或性能机理。','11':'目标本身是扩散语言模型，应区别于用扩散模型起草自回归目标。','12':'用于图像／视频生成的推测解码。','13':'用于多模态理解、视觉语言动作或机器人模型。','14':'用于语音／音频理解或生成。','15':'涉及动作、工具、轨迹、检索链或多 Agent 的推测执行；不保证属于 token SD。','16':'相邻训练／蒸馏或 MTP 背景，应分别核查是否提出推测推理算法。','17':'主要问题是长上下文、KV 历史、缓存恢复或近似计算。','18':'涉及 MoE 专家成本、专家路由或混合递归架构的验证状态。','19':'主要问题是安全、隐私、公平性或水印。','20':'主要问题是从上下文、历史或检索库复用候选。','21':'相邻连续生成或熵解码；不能直接套用离散 SD 的定义和保证。','22':'目标任务为生成式推荐，而非通用文本生成。'}
def classify(p):
 if p['id'] in OVERRIDES:return OVERRIDES[p['id']]
 t=p['title'].lower();a=p['abstract'].lower()
 rules=[('19',r'watermark|security|attack|privacy|injection|mistletoe|disparate'),('18',r'\bmoe\b|mixture.of.expert|gdn|hybrid language|hybrid gdn|replayssm'),('22',r'generative recommendation'),('14',r'speech|audio'),('13',r'\bvla\b|vision.language|multimodal|wam\b|world.action|document ocr|video language'),('12',r'image generation|video generation|visual generation|visual token'),('15',r'agent|tool.using|tool.augmented|retrieval.augmented|multi.hop.*retrieval'),('11',r'diffusion (?:language|llm)|diffusion large language|diffusion decoding|speculative diffusions|speculative diffusion\b|diffusion sampling'),('20',r'retriev|context reuse|suffix|trajectory.*history|unigram|bigram|extractive|lempel|drafter.free'),('17',r'long.context|kv.cache|draft kv|long.horizon|history'),('07',r'cross.block|looped diffusion|loopdraft|recurrent speculative|block.*beyond'),('10',r'\btheory\b|floor|ceiling|gap between|not identical|numerical|audit|measurement|evaluating|mechanisms|revisiting|training reshapes|marginal error|when adaptivity'),('08',r'lossy|relax|semantic|plausibility|beyond exact|beyond the target|collaborat|freeze the target'),('02',r'train|distill|supervision|adaptation|calibration|align|loss\b|learning.*draft'),('09',r'serving|throughput|batched|rollout|cloud|edge|compile|inference.system'),('06',r'asynchron|concurrent|pipeline|overlap|budget|adaptive|allocation|cost.aware|orchestrat|when to|predict.*cost'),('05',r'self.spec|looped transformer|looped language|target.integrat'),('04',r'tree|multi.draft|verification|verify|coupling|optimal transport|multi.path'),('03',r'parallel|diffusion draft|block draft|one.pass|semi.autoregressive|draft.edit')]
 for key,pattern in rules:
  if re.search(pattern,t):return key
 return '02' if re.search(r'train|distill',a[:600]) else '06'

def retrieve(p):
 d=ROOT/p['directory_path'];d.mkdir(exist_ok=True,parents=True)
 pdf=d/(p['acronym']+'.pdf')
 if p.get('pdf_file'):pdf=ROOT/p['pdf_file']
 valid=pdf.exists() and subprocess.run(['pdfinfo',str(pdf)],capture_output=True).returncode==0
 errors=[]
 for url in ([] if valid else p['pdf_candidates']):
  tmp=pdf.with_suffix('.part')
  r=subprocess.run(['curl','-L','--fail','--max-time','35','-sS',url,'-o',str(tmp)],capture_output=True,text=True)
  if r.returncode==0 and tmp.exists() and tmp.read_bytes().startswith(b'%PDF-') and subprocess.run(['pdfinfo',str(tmp)],capture_output=True).returncode==0:
   tmp.replace(pdf);valid=True;p['download_url']=url;break
  errors.append({'url':url,'error':r.stderr[-180:]});tmp.unlink(missing_ok=True)
 p['status']='downloaded' if valid else 'pdf_unavailable';p['download_errors']=errors
 if valid:
  p['pdf_file']=str(pdf.relative_to(ROOT));p['sha256']=hashlib.sha256(pdf.read_bytes()).hexdigest();p['bytes']=pdf.stat().st_size
  info=subprocess.check_output(['pdfinfo',str(pdf)],stderr=subprocess.DEVNULL,text=True)
  p['pages']=int(re.search(r'Pages:\s+(\d+)',info)[1])
  first=subprocess.run(['pdftotext','-f','1','-l','1',str(pdf),'-'],capture_output=True,text=True).stdout
  p['pdf_title_preview']=first[:1200];p['title_token_coverage']=round(len(set(re.findall('[a-z0-9]+',p['title'].lower()))&set(re.findall('[a-z0-9]+',first.lower())))/max(1,len(set(re.findall('[a-z0-9]+',p['title'].lower())))),3)
  p.setdefault('download_url','https://arxiv.org/pdf/'+p['arxiv_id'] if p.get('arxiv_id') else p['source_url'].replace('/forum?','/pdf?'))
 print(p['acronym'],p['status'],flush=True)
 return p

if __name__=='__main__':
 raw=read('sources_2027/search_candidates.json')['candidates'];arxiv={norm(x['title']):x for x in read('sources_2027/arxiv_candidates.json')}
 previous_batch={p['id']:p for p in read('conference_2027_manifest.json')['papers']} if (ROOT/'conference_2027_manifest.json').exists() else {}
 layout=read('classification_manifest.json');cats={c['directory'][:2]:c for c in layout['categories']}
 for directory,name,description in NEW_CATEGORIES:cats[directory[:2]]=dict(directory=directory,name=name,description=description)
 old=read('papers_manifest.json')['papers'];oldbytitle={norm(x['title']):x for x in old};layouttitles={norm(x['title']):x for x in layout['papers']};used=set();selected=[];excluded=[]
 for x in raw:
  reason=EXCLUDED.get(x['id'])
  if not reason and x['match_basis']!='title' and x['id'] not in EXTRA_KEEP:reason='已检查候选摘要：以其他任务为主要贡献，SD 仅为背景、基线或关键词；不纳入本批方法目录。'
  if reason:excluded.append({'id':x['id'],'title':x['title'],'source_url':x['source_url'],'reason':reason});continue
  p=dict(x);key=classify(p);cat=cats[key];am=arxiv.get(norm(p['title']))
  if am:p.update(arxiv_id=am['arxiv_id'],arxiv_title=am['title'])
  if p['id'] in ARXIV_OVERRIDES:p['arxiv_id']=ARXIV_OVERRIDES[p['id']]
  previous=oldbytitle.get(norm(p['title']));record=layouttitles.get(norm(p['title']))
  alias=ALIASES.get(p['id']) or re.sub(r'[^A-Za-z0-9+_-]','',p['title'].split(':')[0])
  if ':' not in p['title'] and p['id'] not in ALIASES:alias=''.join(re.findall(r'[A-Za-z0-9]+',p['title'])[:6])[:55]
  alias=alias or 'Submission'+str(p['number']);folder='ICLR2027-'+alias
  if folder in used:folder+='-'+str(p['number']);alias+='-'+str(p['number'])
  used.add(folder)
  if record:folder=record['folder'];directory=record['directory_path'];cat=next(c for c in cats.values() if c['directory']==directory.split('/')[0]);key=cat['directory'][:2]
  else:directory=cat['directory']+'/'+folder
  p.update(folder=folder,directory_path=directory,acronym=alias,primary_category=cat['name'],category=cat['name'],classification_basis=WHY[key],scope='ICLR 2027 public submission snapshot',venue_status='ICLR 2027 投稿快照记录；非录用，当前状态未由官方 API 实时复核',venue_evidence_url=p['source_url'],venue_evidence_kind='OpenReview public metadata mirrored by iclr2027-explorer, built 2026-10-07',checked_at='2026-10-19',notes_basis='题名与摘要初筛；分类可交叉，非逐篇全文评审',secondary_topics=[],relation=WHY[key])
  if re.search(r'agent|tool|multi.turn',p['title']+' '+p['keywords'],re.I):p['secondary_topics'].append('Agentic')
  if key=='15':p['secondary_topics'].append('action/tool/trajectory-level speculation; distinguish from token SD')
  if key in ['16','21']:p['secondary_topics'].append('相邻背景／扩展，不计为标准 LLM token SD')
  p['summary_zh']=WHY[key]
  p['existing_in_library']=previous_batch.get(p['id'],{}).get('existing_in_library',bool(record or previous))
  if previous:
   for k in ['pdf_file','sha256','download_url','pages','bytes']: 
    if previous.get(k):p[k]=previous[k]
  if record and not p.get('pdf_file'):
   existingpdf=next((ROOT/directory).glob('*.pdf'),None)
   if existingpdf:p['pdf_file']=str(existingpdf.relative_to(ROOT))
  if p['id']=='UwMYxYHQSG':p['summary_zh']='复用目标上下文隐藏状态，以无历史并行骨干和轻量顺序头起草，减少 Agent 多轮长上下文中的草稿历史 KV 开销；不是工具动作级推测。'
  p['pdf_candidates']=(['https://arxiv.org/pdf/'+p['arxiv_id']] if p.get('arxiv_id') else [])+['https://openreview.net/pdf?id='+p['id']]
  selected.append(p)
 write('sources_2027/excluded.json',excluded)
 with concurrent.futures.ThreadPoolExecutor(max_workers=4) as ex:results=list(ex.map(retrieve,selected))
 write('conference_2027_manifest.json',dict(collected_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),snapshot_date='2026-10-07',official_live_status_verified=False,source_total=43013,candidates=len(raw),excluded=len(excluded),papers=results))
 print('DONE',len(results),'downloaded',sum(p['status']=='downloaded' for p in results),flush=True)
