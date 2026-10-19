#!/usr/bin/env python3
"""Append the verified 2026 conference collection, preserving existing files."""
from library_layout import paper_dir, refresh_layout
import concurrent.futures, datetime, hashlib, json, pathlib, re, subprocess
from urllib.parse import urlsplit,parse_qs
ROOT=pathlib.Path(__file__).resolve().parent
ALIASES={
 'Efficient Training-Free Multi-Token Prediction via Embedding-Space Probing':'ESP',
 'Speculative Coupled Decoding for Training-Free Lossless Acceleration of Autoregressive Visual Generation':'SpeculativeCoupledDecoding',
 'The Hidden Cost of Structured Generation in LLMs: Draft-Conditioned Constrained Decoding':'DraftConditionedDecoding',
 'Trajectory-Level Speculative Decoding for Diffusion Language Models':'TrajectorySD',
 'Variational Speculative Decoding: Rethinking Draft Training from Token Likelihood to Sequence Acceptance':'VSD',
 'When Drafts Evolve: Speculative Decoding Meets Online Learning':'WhenDraftsEvolve',
 'When RL Meets Adaptive Speculative Training: A Unified Training-Serving System':'AdaptiveSpecTraining',
 'Beyond Multi-Token Prediction: Pretraining LLMs with Future Summaries':'FSP',
 'Bridging Draft Policy Misalignment: Group Tree Optimization for Speculative Decoding':'GTO',
 'Draft-based Approximate Inference for LLMs':'DraftApproxInference',
 'Dynamic Speculative Agent Planning':'DynamicSpecPlanning',
 'Flatter Tokens are More Valuable for Speculative Draft Model Training':'SFDD',
 'Global Resolution: Optimal Multi-Draft Speculative Sampling via Convex Optimization':'GlobalResolution',
 'Guided Speculative Inference for Efficient Test-Time Alignment of LLMs':'GSI',
 'Improving the Trade-off Between Watermark Strength and Speculative Sampling Efficiency for Language Models':'WatermarkSD',
 'Learning To Draft: Adaptive Speculative Decoding with Reinforcement Learning':'LTD',
 'Overcoming Joint Intractability with Lossless Hierarchical Speculative Decoding':'HSD',
 'Scaling Up, Speeding Up: A Benchmark of Speculative Decoding for Efficient LLM Test-Time Scaling':'ScalingUpSpeedingUp',
 'Self-Speculative Decoding Accelerates Lossless Inference in Any-Order and Any-Subset Autoregressive Models':'ASSD',
 'Self-Speculative Masked Diffusions':'SSMD',
 'Small Drafts, Big Verdict: Information-Intensive Visual Reasoning via Speculation':'SpeculativeVerdict',
 'Speculative Actions: A Lossless Framework for Faster AI Agents':'SpeculativeActions',
 'Speculative Speculative Decoding':'SSD-Saguaro',
 'Training-Free Loosely Speculative Decoding: Accepting Semantically Correct Drafts Beyond Exact Match':'FLy',
 'Attention Drift: What Auto-Regressive Speculative Decoding Models Learn':'AttentionDrift',
 'Dynamic Delayed Tree Expansion For Improved Multi-Path Speculative Decoding':'DelayedTreeExpansion',
 'Efficiently Aligning Draft Models via Parameter- and Data-Efficient Adaptation':'EDA',
 'Efficient Tree Draft for Long-Context Speculative Decoding':'EfficientTreeDraft',
 'Free Draft-and-Verification: Toward Lossless Parallel Decoding for Diffusion Large Language Models':'FreeDave',
 'In STeP: Speculative Tensor Parallelism for Concurrent Heterogeneous Inference of LLMs':'InSTeP',
 'Keep or Preempt? Termination-Aware Scheduling for LLM Serving with Speculative Decoding':'KeepOrPreempt',
 'On the Information Loss of Multi-Token Prediction: Origin and Solution':'MTPInformationLoss',
 'Performance-Driven Policy Optimization for Speculative Decoding with Adaptive Windowing':'PPOW',
 'Realtime-VLA FLASH: Speculative Inference Framework for Diffusion-based VLAs':'RealtimeVLA-FLASH',
 'SP$^2$ec: Adaptive Self-Speculative Decoding for Vision-Language Models':'SP2ec',
 'Speak Early: Speculative Speech Generation for Low-Latency SpeechLLMs':'SpecSpeak',
 'Speculative Decoding Is Per-Token, Not Path':'PerTokenNotPath',
 'Speculative Self-Distillation enables Efficient Knowledge Internalization':'SpeculativeSelfDistillation',
 'Test-Time Speculation':'TTS',
 'To Copy or Not to Copy: Controlling Speculative Decoding via Intrinsic Model Signals':'SwitchSD',
 'Verification-Aware Training for Speculative Decoding':'VAT',
 'Why Speculative Decoding Works Better Than Predicted on Sparse MoE Models':'MoESDSpeedup',
 'LK Losses: Direct Acceptance Rate Optimization for Speculative Decoding':'LKLosses',
}
ARXIV={
 'P-EAGLE':'2602.01469','D-PACE':'2605.18810','BASTION':'2605.29727',
 'AttentionDrift':'2605.09992','EDA':'2603.09527','EfficientRollout':'2606.18967',
 'DelayedTreeExpansion':'2602.16994','FreeDave':'2510.00294','PSD':'2605.15609',
 'PPOW':'2605.14978','SEED':'2609.36590','RealtimeVLA-FLASH':'2605.13778',
 'SimSD':'2606.02544','RheoSampling':'2609.21827','SPECS':'2506.15733',
 'SpecHop':'2605.21965','VAT':'2608.30135','SpecBlock':'2605.07243',
 'TALON':'2601.07353','TTS':'2605.09329','SwitchSD':'2609.20186',
 'TreeGraft':'2608.26112','TriSpec':'2601.23180','UniVer':'2605.04543',
}
def norm(s):return re.sub(r'[^a-z0-9]','',s.lower())
def download(p):
    dest=paper_dir(ROOT,p['folder']);dest.mkdir(parents=True,exist_ok=True)
    pdf=ROOT/p['pdf_file'] if p.get('pdf_file') else dest/(p['acronym']+'.pdf')
    if pdf.exists() and subprocess.run(['pdfinfo',str(pdf)],capture_output=True).returncode==0:
        p['status']='downloaded';p['reused_existing_pdf']=True
        if not p.get('download_url') and p.get('pdf_candidates'):
            p['download_url']=p['pdf_candidates'][0]
            p['download_url_basis']='复用已有文件；来源依据本条唯一候选恢复'
    else:
        errors=[]
        for url in p.get('pdf_candidates',[]):
            tmp=pdf.with_suffix('.part')
            run=subprocess.run(['curl','-L','--fail','--retry','1','--max-time','60','-sS',url,'-o',str(tmp)],capture_output=True,text=True)
            if run.returncode==0 and tmp.read_bytes().startswith(b'%PDF-') and subprocess.run(['pdfinfo',str(tmp)],capture_output=True).returncode==0:
                tmp.replace(pdf);p['status']='downloaded';p['download_url']=url;break
            errors.append(dict(url=url,error=run.stderr[-250:]));tmp.unlink(missing_ok=True)
        else:p['status']='pdf_unavailable';p['download_errors']=errors
    if p['status']=='downloaded':
        p['pdf_file']=str(pdf.relative_to(ROOT));p['sha256']=hashlib.sha256(pdf.read_bytes()).hexdigest();p['bytes']=pdf.stat().st_size
        info=subprocess.run(['pdfinfo',str(pdf)],capture_output=True,text=True).stdout
        p['pages']=next((int(x.split(':')[1]) for x in info.splitlines() if x.startswith('Pages:')),None)
        p['first_page_text']=subprocess.run(['pdftotext','-f','1','-l','1',str(pdf),'-'],capture_output=True,text=True).stdout[:5000]
        p['title_check_score']=round(len(set(re.findall('[a-z0-9]+',p['title'].lower())) & set(re.findall('[a-z0-9]+',p['first_page_text'].lower())))/max(1,len(set(re.findall('[a-z0-9]+',p['title'].lower())))),3)
    print(p['folder'],p['status'],p.get('pages',''),flush=True)
    return p

if __name__=='__main__':
    existing=json.loads((ROOT/'papers_manifest.json').read_text())
    migrations={'arXiv2026-DFlash':'ICML2026-DFlash','arXiv2026-SpecBlock':'NeurIPS2026-SpecBlock','arXiv2026-VAT':'NeurIPS2026-VAT'}
    for old,new in migrations.items():
        if (ROOT/old).exists() and not (ROOT/new).exists():(ROOT/old).rename(ROOT/new)
        for p in existing['papers']:
            if p['folder']==old:
                p['folder']=new;p['pdf_file']=p['pdf_file'].replace(old+'/',new+'/')
        for f in [ROOT/'README.md',ROOT/'collect_papers.py',ROOT/'render_index.py']:
            s=f.read_text();f.write_text(s.replace(old,new))
    (ROOT/'papers_manifest.json').write_text(json.dumps(existing,ensure_ascii=False,indent=2)+'\n')
    candidates=json.loads((ROOT/'sources_2026'/'candidates.json').read_text())['papers']
    maps={'ICML':json.loads((ROOT/'sources_2026'/'pmlr306_selected.json').read_text()),'ICLR':json.loads((ROOT/'sources_2026'/'iclr2026_selected.json').read_text())}
    selected=[]
    for p in candidates:
        acronym=ALIASES.get(p['title'],p['title'].split(':',1)[0])
        p.update(acronym=acronym,folder=p['conference']+'2026-'+acronym,scope='2026 conference expansion',venue_evidence_url=p['url'],venue_status='2026 主会官方 Poster 目录确认',checked_at='2026-10-11')
        mapentry=maps.get(p['conference'],{}).get(p['title'])
        if mapentry is None:
            mapentry=next((v for t,v in maps.get(p['conference'],{}).items() if norm(t)==norm(p['title'])),None)
        pdfurls=[]
        if mapentry:
            p.update(mapentry);pdfurls.append(p['pdf_url']);p['venue_status']='2026 主会正式论文集确认'
        if acronym in ARXIV:
            p['arxiv_id']=ARXIV[acronym];pdfurls.append('https://arxiv.org/pdf/'+p['arxiv_id'])
        forum=next((x['url'] for x in p['links'] if 'openreview.net/forum?id=' in x['url']),None)
        if forum:
            p['openreview_url']=forum
            if not pdfurls:pdfurls.append(forum.replace('/forum?','/pdf?'))
        p.setdefault('source_url',p['url'])
        p['pdf_candidates']=pdfurls
        previous=next((x for x in existing['papers'] if x['folder']==p['folder']),None)
        if previous:
            for key in ['pdf_file','download_url','sha256','pages','bytes','relation','category']:
                if previous.get(key) is not None:p[key]=previous[key]
            p['original_scope']=previous.get('original_scope') or previous.get('scope')
        selected.append(p)
    with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool:
        results=list(pool.map(download,selected))
    (ROOT/'conference_2026_manifest.json').write_text(json.dumps(dict(collected_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),papers=results),ensure_ascii=False,indent=2)+'\n')

    refresh_layout(ROOT)
