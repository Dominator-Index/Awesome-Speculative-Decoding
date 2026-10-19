#!/usr/bin/env python3
"""Merge the conference expansion and render Chinese reading notes; no downloads."""
from library_layout import paper_dir, refresh_layout
import collections, csv, datetime, json, pathlib
ROOT = pathlib.Path(__file__).resolve().parent
# Notes are short Chinese paraphrases of the official abstracts, not experiment replications.
NOTES = '''AdaHC|相邻：MTP 训练|通过预测头分块和调度提高多 token 预测训练效率，主要贡献在训练流水线。
BubbleSpec|服务与 RL 系统|利用 RL rollout 长尾造成的空闲计算起草下一轮候选，再同步验证。
ConFu|草稿架构与训练|用面向未来的辅助信息改善草稿模型预测，缓解多步起草的误差累积。
CSD|扩展：视觉生成|按图像内容与预测熵调整接受条件和重采样；不能直接套用标准 SD 的分布保持结论。
DC-Leap|扩展：扩散语言模型|利用中等置信度位置的连续验证加速扩散语言模型；质量相近不等于严格保持采样分布。
DFlash|并行草稿|目标特征条件的块扩散模型并行起草，是 DLoop 的核心实验基线。
DREAM-R|扩展：多模态推理|以推理步骤为起草单元，并用强化学习对齐草稿模型；需区分步骤接受与标准逐 token SD。
Dustin|长上下文与近似计算|结合草稿前瞻和历史注意力选择 KV，降低长上下文验证开销；需单独核查稀疏验证的精度保证。
ECHO|服务与 RL 系统|用批量超级树和置信度预算分配候选深度、宽度，面向高并发服务。
ESP|草稿架构与训练|在嵌入空间探测多个未来位置，构建和裁剪候选树，减少专门训练草稿模型的需要。
FAFO|自推测与跳层|在同一次执行中结合压缩 KV 的近似候选与完整验证，减少单独起草的开销。
KnapSpec|自推测与跳层|把注意力和 MLP 层的选择建模为受硬件延迟约束的组合优化。
LEAP|自推测与跳层|通过分区层分组和搜索选择自推测的计算路径。
LKLosses|草稿架构与训练|直接优化接受率相关损失，而不是只用 token 似然或 KL 作为训练代理。
MineDraft|服务与 RL 系统|交错两个批次的起草与验证，提高执行重叠和系统利用率。
NanoSpec|草稿架构与训练|利用上下文相关小词表及输出投影优化，降低轻量草稿模型的输出开销。
PipeSD|服务与 RL 系统|在端云环境流水化 token 生成与通信，并自适应决定通信、验证时机。
SelfJudge|放宽验证与推理加速|用目标模型提供语义判断来接受候选，需区别语义质量保持与严格采样分布保持。
SJD-SV|扩展：视觉生成|把语义层验证引入视觉 Jacobi 解码，需要同时检查生成质量与加速收益。
SpecExit|放宽验证与推理加速|草稿模型同时预测未来 token 和提前结束推理的信号；包含输出长度变化。
SpecForge|服务与 RL 系统|提供草稿模型训练基础设施，支持 EAGLE-3 等方法，重点是训练流程与工程。
SpecPrune-VLA|相邻：VLA 剪枝|根据时空一致性进行视觉 token 的动作级、层级剪枝；官方摘要描述的是剪枝方法，并非典型 draft-verify SD。
SpeculativeCoupledDecoding|扩展：视觉生成|通过耦合采样加速自回归视觉生成，论文强调其分布保持条件。
SPEED-Bench|基准与分析|评测不同任务、模型和负载下的推测解码延迟与吞吐，适合检查单点加速能否泛化。
DraftConditionedDecoding|基准与分析|研究结构化生成约束与草稿条件化之间的相互影响，分析接受率和实际速度的变化。
TrajectorySD|扩展：扩散语言模型|在扩散语言模型的生成轨迹层面开展推测；不同于 DFlash 用扩散草稿服务自回归目标模型。
VSD|草稿架构与训练|从序列接受概率出发设计变分训练目标，改善仅优化逐 token 似然的局限。
Vegas|自推测与跳层|以稀疏注意力构造自身草稿，再由完整目标模型验证。
VIA-SD|放宽验证与推理加速|在直接接受、精简验证器和完整模型之间路由；不能仅凭质量指标推定等同标准 SD 输出分布。
WhenDraftsEvolve|草稿架构与训练|把不断变化的草稿模型与在线学习结合，研究动态适应与解码行为。
AdaptiveSpecTraining|服务与 RL 系统|把 RL 更新和自适应推测训练、服务结合，处理策略持续变化时的起草效率。
XSpecMesh|扩展：视觉生成|将多头推测解码用于自回归三维网格生成。
FSP|相邻：MTP 训练|通过未来内容摘要改进预训练中的多 token 预测，属于草稿能力的训练背景。
GTO|草稿架构与训练|用组树优化对齐草稿策略与候选树的期望收益，而非仅拟合单一路径。
Cactus|放宽验证与推理加速|在受控分布偏移约束下提高接受效率；与严格无损 SD 的保证不同。
DraftApproxInference|长上下文与近似计算|利用草稿前瞻估计重要 KV，主要研究近似推理计算的分配。
DynamicSpecPlanning|扩展：Agent|动态组织 Agent 的推测规划，关注规划延迟与执行行为。
FastGRPO|服务与 RL 系统|将并发感知解码与在线草稿更新用于 GRPO rollout。
SFDD|草稿架构与训练|发现目标分布较平坦的 token 对草稿训练更有价值，据此进行训练样本选择。
GlobalResolution|候选树与采样验证|把多候选最优接受问题转成凸优化，减少直接求解最优传输的复杂度。
GSI|放宽验证与推理加速|以奖励引导推测生成实现测试时对齐；目标是受奖励调整的策略，需要明确参考分布。
WatermarkSD|基准与分析|研究文本水印强度与推测采样效率之间的权衡。
LTD|调度与执行重叠|用强化学习共同调整起草和验证策略，优化实际解码周期吞吐。
Not-a-Bandit|调度与执行重叠|利用目标模型反馈评估多个草稿器，研究具有无遗憾保证的在线草稿选择。
HSD|候选树与采样验证|通过层级验证处理联合候选分布，重点是分布保持与多候选计算的平衡。
PARD|草稿架构与训练|构造独立于目标模型内部状态的并行草稿，并以轻量适应改善兼容性。
RepSpec|草稿架构与训练|训练时使用额外可重参数化结构，推理时合并结构以控制起草成本。
ScalingUpSpeedingUp|基准与分析|面向推理与测试时扩展评测 SD，区分单条生成加速与多轨迹推理整体成本。
ASSD|扩展：任意顺序模型|研究任意顺序、任意子集自回归模型中的并行自推测及正确联合采样。
SSMD|扩展：扩散语言模型|将自推测用于掩码扩散模型，考虑并行预测之间的依赖。
SpeculativeVerdict|扩展：多模态推理|轻量专家提出视觉推理候选，大模型给出判断；不宜直接视为普通 token 级 SD。
SpecBranch|调度与执行重叠|预先准备可能被拒绝位置的后续分支，使起草和验证重叠，并处理回滚。
SpeculativeActions|扩展：Agent|并行推测后续动作，再按验证结果选择或回滚；比较对象是 Agent 执行轨迹。
SSD-Saguaro|调度与执行重叠|预测当前验证的可能结果并提前起草下一轮，以重叠起草和验证；与 DLoop 延后验证的组织方式不同。
FLy|放宽验证与推理加速|接受语义正确但不完全匹配的草稿，因此质量保证应与严格目标分布保持区分。
AdaTree|候选树与采样验证|依据预计验证时间、接受长度及服务负载自适应选择候选树配置。
AttentionDrift|基准与分析|分析连续起草中注意力逐渐从输入转向自身 token 的漂移及其缓解方法，关联 DLoop 的跨轮误差问题。
BASTION|候选树与采样验证|为块扩散草稿构造动态树，结合置信度、预计接受收益和硬件验证成本分配节点。
BitMTP|相邻：MTP 训练|结合低比特模型和多 token 预测，考虑接受前缀对齐以及算法与系统配合。
CATS|扩展：多模态推理|针对多模态草稿训练中的难接受位置与关键视觉信息进行对齐。
D-PACE|草稿架构与训练|根据期望接受长度对各预测位置的训练损失动态加权。
DelayedTreeExpansion|候选树与采样验证|把多路径分支推迟到更可能分歧的深度，减少浅层无效扩张。
EDA|草稿架构与训练|通过参数高效与数据高效适应对齐草稿，处理目标模型变化。
EfficientRollout|服务与 RL 系统|结合量化自推测和自适应长度，提升持续更新策略的 RL rollout 效率。
EfficientTreeDraft|候选树与采样验证|论文方法名 FastDraft：优化共享前缀、树起草和长上下文访存开销。
FreeDave|扩展：扩散语言模型|复用扩散生成计算执行起草与验证；其无损参照是特定静态扩散解码器。
Gumbo|候选树与采样验证|以 Gumbel 分数扩展和重排候选树，并通过耦合采样处理高温下的正确性问题。
InSTeP|服务与 RL 系统|让 CPU 与 GPU 上的嵌套草稿、目标计算并行执行，结合显著 FFN 通道选择。
KeepOrPreempt|服务与 RL 系统|论文方法名 AlmostDone：把接受效率与请求即将结束的概率纳入抢占调度。
LADDERS|服务与 RL 系统|结合响应长度预测、GPU 分配和前轮 rollout 后缀复用，减少 RL 生成长尾。
MTPInformationLoss|相邻：MTP 训练|论文方法名 Dual-MTP：分析多 token 预测的信息损失，以双向与随机掩码训练改善位置依赖。
P-EAGLE|并行草稿|学习共享隐藏表示并并行预测多个位置，避免逐 token 自回归起草。
PPOW|草稿架构与训练|以窗口为单位优化成本感知策略，并用适应性窗口和课程训练改善起草。
PSD|扩展：扩散语言模型|从一次扩散预测构造多深度候选并分层验证，结合自适应解掩码。
RealtimeVLA-FLASH|扩展：VLA|由轻量动作草稿与动作专家验证配合，并按执行阶段调整回退策略。
RheoSampling|候选树与采样验证|解耦随机采样分布与动态候选树构造，处理非零温度的多候选生成。
SEED|草稿架构与训练|缓存已验证的深层特征，利用轻量末层起草，形成隐式编码器—解码器结构。
SimSD|扩展：扩散语言模型|把参考 token 放入合法的扩散时间上下文，实现单次执行中的候选验证。
SP2ec|扩展：多模态推理|面向视觉语言模型自适应跳层，依据实际时间反馈选择自推测配置。
SpecSpeak|扩展：语音|在 LLM 验证文本草稿期间提前合成语音，降低首段语音延迟。
SpecBlock|跨块起草|训练跨块迭代草稿与排序头，是比较 DLoop 连续多轮起草机制的直接近邻。
SpecHop|扩展：Agent|用快速工具异步推测后续执行，依据真实工具观察验证并回滚。
SPECS|放宽验证与推理加速|在推理过程中动态切换奖励引导的草稿，关注速度与推理质量的权衡。
PerTokenNotPath|基准与分析|分析逐 token 接受率与整条路径重叠的区别；理论结论需限定在论文讨论的验证协议内。
SpeculativeSelfDistillation|相邻：蒸馏训练|学生生成时只在高偏差位置请求教师干预，以推测思想降低知识蒸馏成本。
SPIRIT|自推测与跳层|按窗口运行时间反馈调整跳层配置，直接优化自推测吞吐。
TALON|候选树与采样验证|在固定节点预算内自适应选择深窄或浅宽候选树。
TTS|草稿架构与训练|利用验证反馈在线进行测试时蒸馏，缓解长输出中的草稿分布失配。
SwitchSD|调度与执行重叠|通过目标表示中的内部信号，在神经草稿与上下文复制之间切换。
TreeGraft|候选树与采样验证|把强弱草稿的候选树重评分并嫁接，恢复单一草稿未覆盖的路径。
TriSpec|放宽验证与推理加速|引入轻量代理验证减少完整目标模型调用；精度接近不能自动等同严格无损。
UniVer|候选树与采样验证|以条件最优传输统一多步、多草稿验证，并明确分布保持条件。
ValuSpec|候选树与采样验证|在目标验证前剔除低价值分支；论文摘要强调与贪心输出一致，需要区别随机采样保证。
VAT|草稿架构与训练|训练时模拟验证行为并调整监督权重，与 DLoop 的 loop-aware training 可对照。
MoESDSpeedup|基准与分析|分析稀疏 MoE 的跨 token 专家重叠与动态 GPU 执行对验证延迟的影响。'''

notes = {a: (g, s) for a, g, s in (line.split('|', 2) for line in NOTES.splitlines())}
expansion = json.loads((ROOT/'conference_2026_manifest.json').read_text())
base = json.loads((ROOT/'papers_manifest.json').read_text())
existing = {p['folder']: p for p in base['papers']}
rows = []
for p in expansion['papers']:
    category, summary = notes[p['acronym']]
    p['category'] = category
    if p['status']=='downloaded' and not p.get('download_url') and p.get('pdf_candidates'):
        p['download_url']=p['pdf_candidates'][0]
        p['download_url_basis']='复用已有文件；来源依据本条唯一候选恢复'
    p['summary_zh'] = summary
    p['notes_basis'] = '官方会议摘要的初步分类与概述；PDF 首页、格式和页数校验；未独立复核全部实验'
    p['relationship_type'] = '相邻背景' if category.startswith('相邻') else ('扩展应用或模型' if category.startswith('扩展') else '推测解码方法、系统或分析')
    old = existing.get(p['folder'], {})
    if old.get('relation'):
        p['relation'] = old['relation']
    p['title_checked'] = '首页词项自动匹配；低匹配项已检查标题断词或版本差异' if p['status']=='downloaded' else '未取得 PDF；标题来自官方目录'
    p['pdf_version'] = ('公开预印本；会议信息另按官方目录核实' if 'arxiv.org' in p.get('download_url', '') else '会议论文集 PDF') if p['status']=='downloaded' else '未取得'
    txt = f"# {p['title']}\n\n- 目录：`{p['folder']}`\n- 分类：{category}（{p['relationship_type']}）\n- 发表依据：{p['venue_status']}，[官方页面]({p['venue_evidence_url']})\n- 论文来源：[链接]({p['source_url']})\n- 核查日期：2026-10-11\n\n## 内容与定位\n\n{summary}\n\n"
    if p.get('relation'):
        txt += f"与 DLoop 的已有关系记录：{p['relation']}\n\n"
    if p.get('title_version_note'):
        txt += f"标题版本说明：{p['title_version_note']}\n\n"
    txt += "说明：这是依据官方摘要形成的阅读导航，尚未逐篇精读实验。不同论文可能保持目标采样分布、仅保持贪心输出、保持特定解码器行为，或允许质量权衡，不能统一称为无损。\n\n"
    if p['status']=='downloaded':
        txt += f"## 本地 PDF\n\n[阅读 PDF]({pathlib.Path(p['pdf_file']).name})，{p['pages']} 页，{p['bytes']:,} 字节。`pdfinfo` 解析成功。\n\n版本：{p['pdf_version']}。\n\n[PDF 来源地址]({p.get('download_url') or p.get('pdf_url')})\n\n{p.get('download_url_basis','下载成功时记录来源地址')}。\n\nSHA-256：`{p['sha256']}`\n"
    else:
        txt += "## PDF 待补\n\n此次未取得可校验 PDF。官方页面提供的 OpenReview 下载地址在当前网络返回 HTTP 403；检索 arXiv 和作者公开页面后仍未取得可下载替代文件。该状态只描述此次检索，不代表论文不存在公开版本。\n\n"
        if p.get('openreview_url'):
            txt += f"[OpenReview 论文页面]({p['openreview_url']})\n"
    (paper_dir(ROOT,p['folder'])/'README.md').write_text(txt)
    existing[p['folder']] = p
    rows.append(p)
base['papers'] = list(existing.values())
base['updated_at'] = datetime.datetime.now(datetime.timezone.utc).isoformat()
base['conference_expansion_index'] = 'CONFERENCES2026.md'
(ROOT/'papers_manifest.json').write_text(json.dumps(base, ensure_ascii=False, indent=2)+'\n')
(ROOT/'conference_2026_manifest.json').write_text(json.dumps(expansion, ensure_ascii=False, indent=2)+'\n')
fields = ['folder','acronym','title','category','relationship_type','scope','venue_status','status','pdf_file','pages','source_url','venue_evidence_url','download_url','sha256','summary_zh','relation']
with (ROOT/'papers.csv').open('w', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=fields, extrasaction='ignore');writer.writeheader();writer.writerows(base['papers'])
counts = collections.Counter((p['conference'], p['status']) for p in rows)
totalpdf = sum(p['status']=='downloaded' for p in base['papers'])
txt = f'''# 2026 年三大会议：推测解码论文扩展目录

核查日期：2026-10-11。本批筛选 **{len(rows)} 篇**，其中 **{sum(p['status']=='downloaded' for p in rows)} 篇已有 PDF**，**{sum(p['status']!='downloaded' for p in rows)} 篇 PDF 待补**。与原 DLoop 文献库重复的 DFlash、SpecBlock、VAT 共 3 篇复用已有 PDF，没有重复收录。合并后共 {len(base['papers'])} 篇方法、系统或相关背景论文，{totalpdf} 篇已有 PDF；DLoop 原文和 Qwen 博客单独保留。

## 来源与覆盖范围

从官方主会目录按 `speculat`、`draft`、`eagle`、多 token 预测等标题关键词筛选，再检查官方摘要，排除明显无关结果。本批是可核查的扩展检索，不保证穷尽所有未在标题出现关键词的论文。包括核心语言模型 SD、系统/训练/分析，以及扩散、视觉、语音、Agent 等扩展；相邻 MTP、蒸馏或剪枝工作明确标注。

- ICML：[官方目录](https://icml.cc/Downloads/2026)，并核对 [PMLR 正式论文集](https://proceedings.mlr.press/v306/)。
- ICLR：[官方目录](https://iclr.cc/Downloads/2026)，并核对 [正式论文集](https://proceedings.iclr.cc/paper_files/paper/2026)。
- NeurIPS：[官方目录](https://neurips.cc/Downloads/2026) 的主会 Poster 条目确认录用信息；此次检索未取得 2026 正式论文集，已下载的 PDF 为作者公开预印本。不要把目录中的会议年份误作 PDF 版本年份。

| 会议 | 收录条目 | 已有 PDF | PDF 待补 |
| --- | ---: | ---: | ---: |
'''
for venue in ['ICML','ICLR','NeurIPS']:
    yes = counts[venue,'downloaded']; no = counts[venue,'pdf_unavailable']
    txt += f'| {venue} 2026 | {yes+no} | {yes} | {no} |\n'
txt += '''
## 围绕 DLoop 的优先阅读顺序

1. **并行与跨块起草**：DFlash → P-EAGLE → SpecBlock。比较块内并行、跨块迭代与 DLoop 多轮完整起草的区别。
2. **训练偏移与接受率**：AttentionDrift → VAT → D-PACE → LKLosses → TTS。比较漂移原因、监督权重、接受率目标与在线适应。
3. **起草和验证的组织方式**：SSD-Saguaro → SpecBranch → LTD → SwitchSD。比较重叠执行、拒绝分支准备、动态控制与延后验证。
4. **树结构与验证保证**：BASTION → TALON → DelayedTreeExpansion → TreeGraft → UniVer / GlobalResolution / HSD。区分候选覆盖与验证正确性。
5. **系统收益的边界**：ECHO → MineDraft → BubbleSpec / FastGRPO / EfficientRollout → SPEED-Bench。检查负载、并发、RL 策略变化和端到端吞吐。

以上是按研究问题组织的阅读建议，不是实验性能排名。各条摘要仅作初步导航，正文里的保证和实验仍需精读。
'''
for venue in ['ICML','ICLR','NeurIPS']:
    txt += f'\n## {venue} 2026\n'
    selected = [p for p in rows if p['conference']==venue]
    for category in dict.fromkeys(p['category'] for p in selected):
        txt += f'\n### {category}\n\n| 论文 / 子目录 | PDF | 内容与定位 |\n| --- | --- | --- |\n'
        for p in selected:
            if p['category']!=category:continue
            pdf = f"[PDF]({p['pdf_file']})" if p['status']=='downloaded' else '待补'
            txt += f"| [{p['acronym']}]({p['folder']}/README.md) | {pdf} | {p['summary_zh']} |\n"
txt += '\n## PDF 待补清单\n\n这些条目已经确认官方会议来源并建立子目录，README 留有论文页面、下载失败原因；没有把网页、海报或幻灯片冒充论文 PDF。\n\n| 目录 | 完整标题 | 官方来源 |\n| --- | --- | --- |\n'
for p in rows:
    if p['status']!='downloaded':
        txt += f"| [{p['folder']}]({p['folder']}/README.md) | {p['title']} | [官方页面]({p['venue_evidence_url']}) |\n"
txt += '\n## 数据与复核\n\n统一表：[papers.csv](papers.csv)。统一元数据：[papers_manifest.json](papers_manifest.json)。本批元数据：[conference_2026_manifest.json](conference_2026_manifest.json)。官方网页快照和候选名单保存于 `sources_2026/`。PDF 校验包括文件头、`pdfinfo`、页数和 SHA-256；首页标题采用词项匹配，低匹配项核查断词与版本差异。NeurIPS 的标题可能随预印本版本更新。\n\n补下载运行 `python3 collect_2026.py`，再运行 `python3 render_2026.py` 更新索引；原 DLoop 目录见 [README](README.md)。\n'
(ROOT/'CONFERENCES2026.md').write_text(txt)
readme = (ROOT/'README.md').read_text()
start='<!-- CONFERENCE2026 START -->'; end='<!-- CONFERENCE2026 END -->'
banner = f'{start}\n\n2026 年扩展已整理：**ICML 32 篇、ICLR 23 篇、NeurIPS 40 篇**；下载状态、分类与待补名单见 [2026 会议索引](CONFERENCES2026.md)。合并文献库共 {len(base["papers"])} 篇，{totalpdf} 篇已有 PDF。DFlash 的目录更新为 `ICML2026-DFlash`，SpecBlock 与 VAT 更新为 `NeurIPS2026-*`，复用原 PDF。\n\n{end}\n'
if start in readme:
    left, remainder = readme.split(start,1); _,right = remainder.split(end,1)
    readme = left+banner+right.lstrip('\n')
else:
    first, rest = readme.split('\n',1);readme = first+'\n\n'+banner+'\n'+rest.lstrip('\n')
(ROOT/'README.md').write_text(readme)
print(json.dumps({'papers':len(base['papers']), 'pdfs':totalpdf, 'conference_entries':len(rows), 'counts':{f'{a}/{b}':n for (a,b),n in counts.items()}},ensure_ascii=False))

refresh_layout(ROOT)
