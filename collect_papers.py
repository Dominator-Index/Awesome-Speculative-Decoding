#!/usr/bin/env python3
"""Download the source-matched DLoop related-work collection; preserve valid PDFs."""
from library_layout import paper_dir, refresh_layout
import concurrent.futures, hashlib, json, pathlib, subprocess, datetime

ROOT = pathlib.Path(__file__).resolve().parent
# directory | title | arXiv ID or PDF URL | category | relation to DLoop
DATA = '''ICML2023-SD|Fast Inference from Transformers via Speculative Decoding|https://proceedings.mlr.press/v202/leviathan23a/leviathan23a.pdf|基础|独立小模型起草，大模型并行验证；DLoop 保留原有接受规则，改变验证前的起草轮数。
arXiv2023-SpeculativeSampling|Accelerating Large Language Model Decoding with Speculative Sampling|2302.01318|基础|与 Leviathan 等并列的分布保持 speculative sampling 基础论文。
NeurIPS2018-BPD|Blockwise Parallel Decoding for Deep Autoregressive Models|1811.03115|并行预测|并行预测未来多个位置，再验证最长前缀；早期块解码工作。
ICML2024-Medusa|Medusa: Simple LLM Inference Acceleration Framework with Multiple Decoding Heads|2401.10774|并行预测|在目标模型上附加多个预测头；DLoop 用它说明草稿生成架构的发展。
ICML2024-EAGLE|EAGLE: Speculative Sampling Requires Rethinking Feature Uncertainty|2401.15077|自回归草稿|利用目标模型特征的轻量自回归草稿模型。
EMNLP2024-EAGLE-2|EAGLE-2: Faster Inference of Language Models with Dynamic Draft Trees|https://aclanthology.org/2024.emnlp-main.422.pdf|自回归草稿与树|利用置信度构造上下文相关的动态草稿树。
NeurIPS2025-EAGLE-3|EAGLE-3: Scaling up Inference Acceleration of Large Language Models via Training-Time Test|https://proceedings.neurips.cc/paper_files/paper/2025/file/c7b5a35ea98b62512a869c19ea7b03cb-Paper-Conference.pdf|自回归草稿|training-time test 在一轮起草内展开自身特征；DLoop 的 loop-aware training 将展开扩展到多轮起草。
NeurIPS2026-VAT|Verification-Aware Training for Speculative Decoding|2608.30135|训练|按模拟验证中各位置能否存活重加权监督；与 DLoop 的多轮输入分布训练关注点不同。
ICML2026-DFlash|DFlash: Block Diffusion for Flash Speculative Decoding|2602.06036|并行草稿|块扩散草稿模型一次前向生成整块；DLoop 的核心叠加基线之一。
arXiv2026-Domino|Domino: Decoupling Causal Modeling from Autoregressive Drafting in Speculative Decoding|2605.29707|并行草稿|并行骨干加轻量因果修正；属于 DLoop 评估基线。
arXiv2026-DSpark|DSpark: Confidence-Scheduled Speculative Decoding with Semi-Autoregressive Generation|2607.05147|并行草稿与调度|半自回归生成和负载感知验证长度；DLoop 在完整起草轮次之间决定是否继续。
ASPLOS2024-SpecInfer|SpecInfer: Accelerating Generative Large Language Model Serving with Tree-based Speculative Inference and Verification|2305.09781|树验证|将候选组织为 token tree 并行验证；DLoop 将树验证视为可组合的机制。
COLM2026-DDTree|Accelerating Speculative Decoding with Block Diffusion Draft Trees|2604.12989|树验证|从块扩散各位置分布构建候选树；DLoop 实验用于 DFlash。
arXiv2026-DARTree|DARTree: Speculative Diffusion Decoding with Autoregressive Draft Trees|2608.13524|树验证|扩散草稿结合自回归候选树；DLoop 实验用于 Domino 和 DSpark。
NeurIPS2023-BiLD|Speculative Decoding with Big Little Decoder|https://proceedings.neurips.cc/paper_files/paper/2023/file/7b97adeafa1c51cf65263459ca9d0d7c-Paper-Conference.pdf|自适应长度|fallback 与 rollback 策略协作大小模型；DLoop 对比其中的置信度停止规则。原文方法不应一概视为严格分布保持。
ACL2024-DraftVerify|Draft & Verify: Lossless Large Language Model Acceleration via Self-Speculative Decoding|https://aclanthology.org/2024.acl-long.607.pdf|自适应长度|跳过部分目标模型层进行自起草，并使用置信度控制停止。
EMNLP2025-SVIP|Draft Model Knows When to Stop: Self-Verification Speculative Decoding for Long-Form Generation|https://aclanthology.org/2025.emnlp-main.844.pdf|自适应长度|DLoop 描述其使用熵决定停止起草。
NeurIPS-ENLSP2024-AdaEDL|AdaEDL: Early Draft Stopping for Speculative Decoding of Large Language Models via an Entropy-based Lower Bound on Token Acceptance Probability|2410.18351|自适应长度|用熵相关的接受概率下界控制 early draft stopping；NeurIPS ENLSP workshop 论文，非主会。
arXiv2024-DDD|Dynamic Depth Decoding: Faster Speculative Decoding for LLMs|2409.00142|自适应长度|根据 beam 内序列的概率和继续扩展草稿树深度。
arXiv2023-LLMCad|LLMCad: Fast and Scalable On-device Large Language Model Inference|2309.04255|自适应长度|累计置信度触发大模型验证，同时考虑端侧模型协作与流水线。
COLM2025-SpecDecPP|SpecDec++: Boosting Speculative Decoding via Adaptive Candidate Lengths|2405.19715|自适应长度|额外训练接受概率预测头，按拒绝风险动态停止起草。
NeurIPS-ENLSP2024-DISCO|Dynamic Speculation Lookahead Accelerates Speculative Decoding of Large Language Models|https://raw.githubusercontent.com/mlresearch/v262/main/assets/mamou24a/mamou24a.pdf|自适应长度|训练分类器决定继续或停止；发表在 NeurIPS ENLSP workshop，非主会。
arXiv2024-AdaEAGLE|AdaEAGLE: Optimizing Speculative Decoding via Explicit Modeling of Adaptive Draft Structures|2412.18910|自适应长度|起草之前由轻量预测器一次预测草稿长度。
TASLP2026-PACER|PACER: Blockwise Pre-verification for Speculative Decoding with Adaptive Length|2602.01274|跨块起草|与 DLoop 最直接的调度近邻之一：训练预验证层，按块预测接受情况决定继续起草。
NeurIPS2026-SpecBlock|SpecBlock: Block-Iterative Speculative Decoding with Dynamic Tree Drafting|2605.07243|跨块起草|与 DLoop 最直接的模型近邻之一：新训练的草稿模型跨块迭代，配合 rank head。
arXiv2026-Gemma4|Gemma 4 Technical Report|2607.02770|MTP模型报告|DLoop 第 2 节引用的原生 MTP 模块来源之一。
EMNLP-Findings2023-SpecDec|Speculative Decoding: Exploiting Speculative Execution for Accelerating Seq2seq Generation|https://aclanthology.org/2023.findings-emnlp.257.pdf|补充早期工作|DLoop 未引用；补充早期 seq2seq draft-then-verify 谱系，预印本最初发布于 2022 年 3 月。
arXiv2024-TurboSpec|TurboSpec: Closed-loop Speculation Control System for Optimizing LLM Serving Goodput|2406.14066|补充服务系统|DLoop 参考文献及服务讨论涉及的闭环控制工作，不属于第 2 节核心列表。
arXiv2023-SDBatching|The Synergy of Speculative Decoding and Batching in Serving Large Language Models|2310.18813|补充服务系统|DLoop 服务讨论涉及的 batching 与 speculative decoding 交互。
MLSys2023-ScalingInference|Efficiently Scaling Transformer Inference|2211.05102|补充推理背景|DLoop 引言引用其解释目标模型验证延迟随 token 数增长较缓的背景。'''

PAPERS = []
for line in DATA.splitlines():
    folder, title, src, category, relation = line.split('|')
    PAPERS.append(dict(folder=folder, title=title, category=category, relation=relation,
        pdf_url=src if src.startswith('https:') else 'https://arxiv.org/pdf/' + src,
        source_url=(src.rsplit('.pdf', 1)[0] + '/' if 'aclanthology.org' in src else 'https://arxiv.org/abs/' + src) if not src.startswith('https:') or 'aclanthology.org' in src else src))

def download(p):
    dest = paper_dir(ROOT, p['folder']); dest.mkdir(parents=True, exist_ok=True)
    filename = p['folder'].split('-', 1)[1]
    if p['folder'] == 'NeurIPS-ENLSP2024-AdaEDL': filename = 'AdaEDL'
    pdf = dest / (filename + '.pdf')
    urls = [p['pdf_url']]
    if p['folder'] == 'NeurIPS2025-EAGLE-3': urls.append('https://arxiv.org/pdf/2503.01840')
    valid = pdf.exists() and subprocess.run(['pdfinfo', str(pdf)], capture_output=True).returncode == 0
    errors = []
    for url in ([] if valid else urls):
        tmp = pdf.with_suffix('.part')
        result = subprocess.run(['curl','-L','--fail','--retry','2','--max-time','100','-sS',url,'-o',str(tmp)], capture_output=True, text=True)
        if result.returncode == 0 and tmp.read_bytes().startswith(b'%PDF-'):
            check = subprocess.run(['pdfinfo',str(tmp)],capture_output=True,text=True)
            if check.returncode == 0:
                tmp.replace(pdf); p['download_url'] = url; valid = True; break
        errors.append(result.stderr[-500:]); tmp.unlink(missing_ok=True)
    p['status'] = 'downloaded' if valid else 'failed'
    if valid:
        p['pdf_file'] = str(pdf.relative_to(ROOT)); p['sha256'] = hashlib.sha256(pdf.read_bytes()).hexdigest()
        p['bytes'] = pdf.stat().st_size
        info = subprocess.run(['pdfinfo', str(pdf)],capture_output=True,text=True).stdout
        p['pages'] = next((int(x.split(':')[1]) for x in info.splitlines() if x.startswith('Pages:')), None)
        p['first_page_text'] = subprocess.run(['pdftotext','-f','1','-l','1',str(pdf),'-'],capture_output=True,text=True).stdout[:4000]
    else: p['errors'] = errors
    print(p['folder'], p['status'], p.get('pages',''), flush=True)
    return p

if __name__ == '__main__':
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
        results = list(pool.map(download, PAPERS))
    target=ROOT/'papers_manifest.json'
    manifest=json.loads(target.read_text()) if target.exists() else {}
    merged={p['folder']:p for p in manifest.get('papers',[])}
    for p in results:
        merged[p['folder']]={**merged.get(p['folder'],{}),**p}
    manifest.update(collected_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),papers=list(merged.values()))
    target.write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')

    refresh_layout(ROOT)
