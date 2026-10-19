#!/usr/bin/env python3
"""Render the local reading index from validated download metadata."""
from library_layout import paper_dir, refresh_layout
import csv, json, pathlib
ROOT = pathlib.Path(__file__).resolve().parent
manifest = json.loads((ROOT/'papers_manifest.json').read_text())
if manifest.get('conference_expansion_index'):
    raise SystemExit('文献库已包含 2026 扩展。请运行 python3 render_2026.py，以保留新分类和会议状态。')
papers = manifest['papers']
evidence = {
 'ICML2023-SD':'https://proceedings.mlr.press/v202/leviathan23a.html',
 'NeurIPS2018-BPD':'https://papers.nips.cc/paper/8212-blockwise-parallel-decoding-for-deep-autoregressive-models',
 'ICML2024-Medusa':'https://openreview.net/forum?id=PEpbUobfJv',
 'ICML2024-EAGLE':'https://openreview.net/forum?id=1NdN7eXyb4',
 'NeurIPS2025-EAGLE-3':'https://proceedings.neurips.cc/paper_files/paper/2025/hash/c7b5a35ea98b62512a869c19ea7b03cb-Abstract-Conference.html',
 'ASPLOS2024-SpecInfer':'https://arxiv.org/abs/2305.09781',
 'COLM2026-DDTree':'https://colm.eventhosts.cc/Conferences/2026/AcceptedPapers',
 'COLM2025-SpecDecPP':'https://openreview.net/forum?id=Y131N9fUbU',
 'NeurIPS-ENLSP2024-DISCO':'https://proceedings.mlr.press/v262/mamou24a.html',
 'NeurIPS-ENLSP2024-AdaEDL':'https://proceedings.mlr.press/v262/agrawal24a.html',
 'TASLP2026-PACER':'https://situozhang.github.io/',
 'MLSys2023-ScalingInference':'https://proceedings.mlsys.org/paper_files/paper/2023',
}
for p in papers:
    if p['folder']=='arXiv2024-AdaEDL':
        p['folder']='NeurIPS-ENLSP2024-AdaEDL'
        p['pdf_file']=p['pdf_file'].replace('arXiv2024-AdaEDL/','NeurIPS-ENLSP2024-AdaEDL/')
    p['venue_evidence_url']=evidence.get(p['folder'],p['source_url'])
    p['scope']='supplement' if p['category'].startswith('补充') else 'DLoop section 2'
    p['venue_status']='正式发表会议未确认；以 arXiv 首发年份命名' if p['folder'].startswith('arXiv') else '会议或期刊；见发表依据'
    if 'ENLSP' in p['folder']: p['venue_status']='NeurIPS 2024 ENLSP workshop，非主会'
    if p['folder']=='TASLP2026-PACER': p['venue_status']='作者主页确认 2026 年 6 月获 TASLP 接收；下载的是 arXiv 预印本'
    if p['folder']=='COLM2026-DDTree': p['venue_status']='COLM 2026 官方 Accepted Papers 确认；下载的是 arXiv 版本'
    p['title_checked']='人工核对首页标题' if p['status']=='downloaded' else '下载尚未完成'
    txt = f"# {p['title']}\n\n- 分类：{p['category']}\n- 目录：`{p['folder']}`\n- 发表状态：{p['venue_status']}\n- 来源：[原始来源]({p['source_url']})\n- 发表依据：[链接]({p['venue_evidence_url']})\n- PDF 下载来源：{p.get('download_url',p['pdf_url'])}\n- 下载状态：{p['status']}\n\n## 与 DLoop 的关系\n\n{p['relation']}\n\n说明：这段关系整理主要依据用户提供的 DLoop 第 2 节（PDF 第 2–3 页）、参考文献及相关正文；不表示已独立复核本论文全部实验。\n"
    if p['status']=='downloaded': txt += f"\n## 本地文件\n\n[阅读 PDF]({pathlib.Path(p['pdf_file']).name})，{p['pages']} 页，{p['bytes']:,} 字节。首页标题已核对，`pdfinfo` 解析成功。\n\nSHA-256：`{p['sha256']}`\n"
    (paper_dir(ROOT,p['folder'])/'README.md').write_text(txt)
(ROOT/'papers_manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')

intro = '''# DLoop 的 Related Work 整理

整理日期：2026-10-11。主文：[DLoop: Looped Speculative Decoding](ICLR2027-DLoop/3897_DLoop_Looped_Speculative_.pdf)。该 PDF 标注 **ICLR 2027 在审**，保留原有目录，不代表已录用。

## 范围与命名

完整覆盖 DLoop 第 2 节 Related Work（PDF 第 2–3 页）的论文型引用；另外补充最早期 SpecDec、服务控制、batching 和推理扩展背景。没有把所有数据集与通用 LLM 报告都混入方法论文列表。Qwen3.5 在第 2 节引用的是官方博客，独立记录于 `Blog2026-Qwen3.5`，不是有 PDF 的会议论文。

已确认正式发表的论文按 `会议年份-缩写` 命名；未确认正式发表会议的论文按 `arXiv首发年份-缩写` 命名。期刊使用 `TASLP2026-PACER`。`NeurIPS-ENLSP2024-*` 明确指 workshop，`EMNLP-Findings2023-SpecDec` 明确指 Findings。目录的发表年份可以与下载 PDF 的预印本首发年份不同。

## DLoop 在整体工作中的位置

DLoop 研究的是：**一次目标模型验证之前，是否可以连续执行多轮完整起草？** 标准流程是一轮起草接一次验证；DLoop 按草稿置信度决定是否再起草一轮，然后一次验证所有累积 token。由于新一轮起草缺少未验证 token 的目标模型隐藏状态，它引入 loop-aware training，让草稿模型在训练时接触自身隐藏状态。DLoop 保留原来的接受规则；“无损”指保留目标模型输出分布，不是接受所有草稿。

| 工作方向 | 代表工作 | 与 DLoop 的关系 |
| --- | --- | --- |
| SD / speculative sampling 基础 | Leviathan SD、Chen Speculative Sampling | 提供 draft-then-verify 和分布保持接受机制 |
| 并行预测头与早期块解码 | BPD、Medusa | 改进一次起草产生哪些候选 |
| 目标特征条件的自回归草稿 | EAGLE、EAGLE-2、EAGLE-3 | 改进草稿质量、候选树和训练；EAGLE-3 是 DLoop 训练思想的直接来源 |
| 并行或半自回归草稿 | DFlash、Domino、DSpark | 降低完整草稿块的生成成本，是 DLoop 的核心实验底座 |
| 树验证 | SpecInfer、EAGLE-2、DDTree、DARTree | 一次验证多条候选路径；DLoop 在此基础上增加起草轮数 |
| 自适应草稿长度 | BiLD、Draft & Verify、SVIP、AdaEDL、DDD、LLMCad、SpecDec++、DISCO、AdaEAGLE | 决定何时停止起草或验证多长；与 DLoop 的调度目标接近 |
| 跨块起草 | PACER、SpecBlock | 与 DLoop 最直接的近邻，需要重点比较额外模块、训练和适用草稿架构 |
| 验证感知训练 | VAT | 调整监督权重；DLoop 关注跨轮起草的输入分布偏移 |
| 原生 MTP | Gemma 4、Qwen3.5 | DLoop 验证其可叠加到模型自身多 token 预测模块 |
| 服务系统背景 | TurboSpec、SD + Batching | 区分单请求延迟与服务吞吐、goodput 和负载约束 |

## 最早的 SD 怎么读

需要区分早期 draft-then-verify 谱系和保持随机采样分布的经典 SD。BPD 是 2018 年的早期块并行解码；Xia 等 SpecDec 的预印本首发于 2022 年 3 月，正式版本为 EMNLP Findings 2023，DLoop 本文没有引用它，所以标记为补充。[SpecDec 正式论文](https://aclanthology.org/2023.findings-emnlp.257/)。

DLoop 明确并列引用 Leviathan 等的 ICML 2023 SD（预印本 2022 年 11 月）和 Chen 等 2023 年 speculative sampling，作为经典分布保持基础。[SD 正式论文](https://proceedings.mlr.press/v202/leviathan23a.html)、[Speculative Sampling](https://arxiv.org/abs/2302.01318)。不能把这些工作与早期块解码的质量保证混为一谈。

## 重点阅读与比较

建议阅读顺序：SD / Speculative Sampling → EAGLE-3 → DFlash → Domino / DSpark → PACER / SpecBlock → DLoop → DDTree / DARTree。

- **EAGLE-3 → DLoop**：前者在一次起草内部展开自身预测特征；后者将这种训练扩展到连续起草轮次。EAGLE-3 的正式会议是 NeurIPS 2025。[正式论文](https://proceedings.neurips.cc/paper_files/paper/2025/hash/c7b5a35ea98b62512a869c19ea7b03cb-Abstract-Conference.html)。
- **DFlash / Domino / DSpark → DLoop**：前三者主要改进块内生成，DLoop 在块间控制何时验证。Domino 和 DSpark 有轻量串行因果模块，不能把整套执行理解为完全没有串行依赖。
- **PACER ↔ DLoop**：都可以在验证之前追加草稿块。PACER 使用额外训练的预验证层；DLoop 根据草稿模型自身置信度 gating，并进行 loop-aware training。[PACER](https://arxiv.org/abs/2602.01274)。
- **SpecBlock ↔ DLoop**：SpecBlock 训练跨块迭代草稿模型与 rank head；DLoop 的论述强调在现有草稿模型上增加循环及相应训练。[SpecBlock](https://arxiv.org/abs/2605.07243)。
- **DDTree / DARTree ↔ DLoop**：关注一次验证的候选结构与路径；DLoop 关注验证之前的起草轮数，可以组合。[DDTree](https://arxiv.org/abs/2604.12989)、[DARTree](https://arxiv.org/abs/2608.13524)。

上述机制比较以 DLoop 的描述为主，并核对了来源和下载文件标题；不是各论文实验的独立复现。尤其是 DLoop 所称“已有自适应长度方法只提升自回归草稿速度”，应理解为其第 4.2 节评测设置中的结果，不应外推成所有模型和负载下的普遍结论。

## 逐篇目录

每个子目录含 PDF 和简短 README；PDF 校验、页数、下载地址、SHA-256 保存在 `papers_manifest.json`，便于筛选的列表在 `papers.csv`。

'''
for kind in dict.fromkeys(p['category'] for p in papers):
    intro += f'### {kind}\n\n| 论文 | 本地 PDF | 与 DLoop 的关系 |\n| --- | --- | --- |\n'
    for p in papers:
        if p['category']==kind:
            link = f"[PDF]({p['pdf_file']})" if p['status']=='downloaded' else '尚未下载成功'
            intro += f"| [{p['title']}]({p['folder']}/README.md) | {link} | {p['relation']} |\n"
    intro += '\n'
intro += '### 官方博客引用\n\n[Qwen3.5: Towards Native Multimodal Agents](Blog2026-Qwen3.5/README.md)：DLoop 引用的 MTP 来源之一；原始引用是网页，未找到与该引用完全对应的独立论文 PDF。\n'
(ROOT/'README.md').write_text(intro)
with (ROOT/'papers.csv').open('w',newline='') as f:
    fields=['folder','title','category','scope','venue_status','source_url','venue_evidence_url','pdf_file','status','pages','sha256','relation']
    writer=csv.DictWriter(f,fieldnames=fields,extrasaction='ignore'); writer.writeheader(); writer.writerows(papers)
blog=paper_dir(ROOT,'Blog2026-Qwen3.5'); blog.mkdir(parents=True,exist_ok=True)
(blog/'README.md').write_text('''# Qwen3.5: Towards Native Multimodal Agents

- 来源：[Qwen 官方博客](https://qwen.ai/blog?id=qwen3.5)
- DLoop 引用：Qwen Team, February 2026a。
- 分类：DLoop 第 2 节的原生 MTP 模块来源。
- 状态：原始引用是博客，未找到与此引用完全对应的独立论文 PDF。目录使用 `Blog2026-Qwen3.5`，不虚构会议。

Qwen3.5-Omni Technical Report（arXiv:2604.15804）是不同条目，DLoop 参考文献列为 2026b，不能代替此处的 2026a 博客引用。没有将网页或其他模型报告冒充原论文 PDF。
''')
print('Indexed:',len(papers),'PDF entries;',sum(p['status']=='downloaded' for p in papers),'downloaded; 1 blog entry')

refresh_layout(ROOT)
