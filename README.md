# DLoop 的 Related Work 整理

<!-- ICLR2027 START -->

ICLR2027 扩展：[分类检索索引](ICLR2027.md)。本批保留 269 条，95 篇已有 PDF；当前文献库 391 篇论文、201 篇已有 PDF。投稿状态与覆盖范围以索引中的快照说明为准。

<!-- ICLR2027 END -->

按研究方向浏览：[研究方向分类索引](CLASSIFICATION.md)。

<!-- CONFERENCE2026 START -->

2026 年扩展已整理：**ICML 32 篇、ICLR 23 篇、NeurIPS 40 篇**；下载状态、分类与待补名单见 [2026 会议索引](CONFERENCES2026.md)。当时合并文献库为 122 篇、106 篇 PDF（历史统计；最新总数见上方 ICLR2027 扩展）。DFlash 的目录更新为 `ICML2026-DFlash`，SpecBlock 与 VAT 更新为 `NeurIPS2026-*`，复用原 PDF。

<!-- CONFERENCE2026 END -->
整理日期：2026-10-11。主文：[DLoop: Looped Speculative Decoding](07_跨块与多轮起草/ICLR2027-DLoop/3897_DLoop_Looped_Speculative_.pdf)。该 PDF 标注 **ICLR 2027 在审**，保留原有目录，不代表已录用。

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

### 基础

| 论文 | 本地 PDF | 与 DLoop 的关系 |
| --- | --- | --- |
| [Fast Inference from Transformers via Speculative Decoding](01_基础与早期工作/ICML2023-SD/README.md) | [PDF](01_基础与早期工作/ICML2023-SD/SD.pdf) | 独立小模型起草，大模型并行验证；DLoop 保留原有接受规则，改变验证前的起草轮数。 |
| [Accelerating Large Language Model Decoding with Speculative Sampling](01_基础与早期工作/arXiv2023-SpeculativeSampling/README.md) | [PDF](01_基础与早期工作/arXiv2023-SpeculativeSampling/SpeculativeSampling.pdf) | 与 Leviathan 等并列的分布保持 speculative sampling 基础论文。 |

### 并行预测

| 论文 | 本地 PDF | 与 DLoop 的关系 |
| --- | --- | --- |
| [Blockwise Parallel Decoding for Deep Autoregressive Models](01_基础与早期工作/NeurIPS2018-BPD/README.md) | [PDF](01_基础与早期工作/NeurIPS2018-BPD/BPD.pdf) | 并行预测未来多个位置，再验证最长前缀；早期块解码工作。 |
| [Medusa: Simple LLM Inference Acceleration Framework with Multiple Decoding Heads](03_并行与半自回归草稿/ICML2024-Medusa/README.md) | [PDF](03_并行与半自回归草稿/ICML2024-Medusa/Medusa.pdf) | 在目标模型上附加多个预测头；DLoop 用它说明草稿生成架构的发展。 |

### 自回归草稿

| 论文 | 本地 PDF | 与 DLoop 的关系 |
| --- | --- | --- |
| [EAGLE: Speculative Sampling Requires Rethinking Feature Uncertainty](02_草稿架构与训练/ICML2024-EAGLE/README.md) | [PDF](02_草稿架构与训练/ICML2024-EAGLE/EAGLE.pdf) | 利用目标模型特征的轻量自回归草稿模型。 |
| [EAGLE-3: Scaling up Inference Acceleration of Large Language Models via Training-Time Test](02_草稿架构与训练/NeurIPS2025-EAGLE-3/README.md) | [PDF](02_草稿架构与训练/NeurIPS2025-EAGLE-3/EAGLE-3.pdf) | training-time test 在一轮起草内展开自身特征；DLoop 的 loop-aware training 将展开扩展到多轮起草。 |

### 自回归草稿与树

| 论文 | 本地 PDF | 与 DLoop 的关系 |
| --- | --- | --- |
| [EAGLE-2: Faster Inference of Language Models with Dynamic Draft Trees](04_候选树与采样验证/EMNLP2024-EAGLE-2/README.md) | [PDF](04_候选树与采样验证/EMNLP2024-EAGLE-2/EAGLE-2.pdf) | 利用置信度构造上下文相关的动态草稿树。 |

### 训练

| 论文 | 本地 PDF | 与 DLoop 的关系 |
| --- | --- | --- |
| [Verification-Aware Training for Speculative Decoding](02_草稿架构与训练/NeurIPS2026-VAT/README.md) | [PDF](02_草稿架构与训练/NeurIPS2026-VAT/VAT.pdf) | 按模拟验证中各位置能否存活重加权监督；与 DLoop 的多轮输入分布训练关注点不同。 |

### 并行草稿

| 论文 | 本地 PDF | 与 DLoop 的关系 |
| --- | --- | --- |
| [DFlash: Block Diffusion for Flash Speculative Decoding](03_并行与半自回归草稿/ICML2026-DFlash/README.md) | [PDF](03_并行与半自回归草稿/ICML2026-DFlash/DFlash.pdf) | 块扩散草稿模型一次前向生成整块；DLoop 的核心叠加基线之一。 |
| [Domino: Decoupling Causal Modeling from Autoregressive Drafting in Speculative Decoding](03_并行与半自回归草稿/arXiv2026-Domino/README.md) | [PDF](03_并行与半自回归草稿/arXiv2026-Domino/Domino.pdf) | 并行骨干加轻量因果修正；属于 DLoop 评估基线。 |

### 并行草稿与调度

| 论文 | 本地 PDF | 与 DLoop 的关系 |
| --- | --- | --- |
| [DSpark: Confidence-Scheduled Speculative Decoding with Semi-Autoregressive Generation](03_并行与半自回归草稿/arXiv2026-DSpark/README.md) | [PDF](03_并行与半自回归草稿/arXiv2026-DSpark/DSpark.pdf) | 半自回归生成和负载感知验证长度；DLoop 在完整起草轮次之间决定是否继续。 |

### 树验证

| 论文 | 本地 PDF | 与 DLoop 的关系 |
| --- | --- | --- |
| [SpecInfer: Accelerating Generative Large Language Model Serving with Tree-based Speculative Inference and Verification](04_候选树与采样验证/ASPLOS2024-SpecInfer/README.md) | [PDF](04_候选树与采样验证/ASPLOS2024-SpecInfer/SpecInfer.pdf) | 将候选组织为 token tree 并行验证；DLoop 将树验证视为可组合的机制。 |
| [Accelerating Speculative Decoding with Block Diffusion Draft Trees](04_候选树与采样验证/COLM2026-DDTree/README.md) | [PDF](04_候选树与采样验证/COLM2026-DDTree/DDTree.pdf) | 从块扩散各位置分布构建候选树；DLoop 实验用于 DFlash。 |
| [DARTree: Speculative Diffusion Decoding with Autoregressive Draft Trees](04_候选树与采样验证/arXiv2026-DARTree/README.md) | [PDF](04_候选树与采样验证/arXiv2026-DARTree/DARTree.pdf) | 扩散草稿结合自回归候选树；DLoop 实验用于 Domino 和 DSpark。 |

### 自适应长度

| 论文 | 本地 PDF | 与 DLoop 的关系 |
| --- | --- | --- |
| [Speculative Decoding with Big Little Decoder](06_自适应调度与执行重叠/NeurIPS2023-BiLD/README.md) | [PDF](06_自适应调度与执行重叠/NeurIPS2023-BiLD/BiLD.pdf) | fallback 与 rollback 策略协作大小模型；DLoop 对比其中的置信度停止规则。原文方法不应一概视为严格分布保持。 |
| [Draft & Verify: Lossless Large Language Model Acceleration via Self-Speculative Decoding](05_自推测与计算裁剪/ACL2024-DraftVerify/README.md) | [PDF](05_自推测与计算裁剪/ACL2024-DraftVerify/DraftVerify.pdf) | 跳过部分目标模型层进行自起草，并使用置信度控制停止。 |
| [Draft Model Knows When to Stop: Self-Verification Speculative Decoding for Long-Form Generation](06_自适应调度与执行重叠/EMNLP2025-SVIP/README.md) | [PDF](06_自适应调度与执行重叠/EMNLP2025-SVIP/SVIP.pdf) | DLoop 描述其使用熵决定停止起草。 |
| [AdaEDL: Early Draft Stopping for Speculative Decoding of Large Language Models via an Entropy-based Lower Bound on Token Acceptance Probability](06_自适应调度与执行重叠/NeurIPS-ENLSP2024-AdaEDL/README.md) | [PDF](06_自适应调度与执行重叠/NeurIPS-ENLSP2024-AdaEDL/AdaEDL.pdf) | 用熵相关的接受概率下界控制 early draft stopping。 |
| [Dynamic Depth Decoding: Faster Speculative Decoding for LLMs](06_自适应调度与执行重叠/arXiv2024-DDD/README.md) | [PDF](06_自适应调度与执行重叠/arXiv2024-DDD/DDD.pdf) | 根据 beam 内序列的概率和继续扩展草稿树深度。 |
| [LLMCad: Fast and Scalable On-device Large Language Model Inference](06_自适应调度与执行重叠/arXiv2023-LLMCad/README.md) | [PDF](06_自适应调度与执行重叠/arXiv2023-LLMCad/LLMCad.pdf) | 累计置信度触发大模型验证，同时考虑端侧模型协作与流水线。 |
| [SpecDec++: Boosting Speculative Decoding via Adaptive Candidate Lengths](06_自适应调度与执行重叠/COLM2025-SpecDecPP/README.md) | [PDF](06_自适应调度与执行重叠/COLM2025-SpecDecPP/SpecDecPP.pdf) | 额外训练接受概率预测头，按拒绝风险动态停止起草。 |
| [Dynamic Speculation Lookahead Accelerates Speculative Decoding of Large Language Models](06_自适应调度与执行重叠/NeurIPS-ENLSP2024-DISCO/README.md) | [PDF](06_自适应调度与执行重叠/NeurIPS-ENLSP2024-DISCO/ENLSP2024-DISCO.pdf) | 训练分类器决定继续或停止；发表在 NeurIPS ENLSP workshop，非主会。 |
| [AdaEAGLE: Optimizing Speculative Decoding via Explicit Modeling of Adaptive Draft Structures](06_自适应调度与执行重叠/arXiv2024-AdaEAGLE/README.md) | [PDF](06_自适应调度与执行重叠/arXiv2024-AdaEAGLE/AdaEAGLE.pdf) | 起草之前由轻量预测器一次预测草稿长度。 |

### 跨块起草

| 论文 | 本地 PDF | 与 DLoop 的关系 |
| --- | --- | --- |
| [PACER: Blockwise Pre-verification for Speculative Decoding with Adaptive Length](07_跨块与多轮起草/TASLP2026-PACER/README.md) | [PDF](07_跨块与多轮起草/TASLP2026-PACER/PACER.pdf) | 与 DLoop 最直接的调度近邻之一：训练预验证层，按块预测接受情况决定继续起草。 |
| [SpecBlock: Block-Iterative Speculative Decoding with Dynamic Tree Drafting](07_跨块与多轮起草/NeurIPS2026-SpecBlock/README.md) | [PDF](07_跨块与多轮起草/NeurIPS2026-SpecBlock/SpecBlock.pdf) | 与 DLoop 最直接的模型近邻之一：新训练的草稿模型跨块迭代，配合 rank head。 |

### MTP模型报告

| 论文 | 本地 PDF | 与 DLoop 的关系 |
| --- | --- | --- |
| [Gemma 4 Technical Report](16_MTP与蒸馏背景/arXiv2026-Gemma4/README.md) | [PDF](16_MTP与蒸馏背景/arXiv2026-Gemma4/Gemma4.pdf) | DLoop 第 2 节引用的原生 MTP 模块来源之一。 |

### 补充早期工作

| 论文 | 本地 PDF | 与 DLoop 的关系 |
| --- | --- | --- |
| [Speculative Decoding: Exploiting Speculative Execution for Accelerating Seq2seq Generation](01_基础与早期工作/EMNLP-Findings2023-SpecDec/README.md) | [PDF](01_基础与早期工作/EMNLP-Findings2023-SpecDec/Findings2023-SpecDec.pdf) | DLoop 未引用；补充早期 seq2seq draft-then-verify 谱系，预印本最初发布于 2022 年 3 月。 |

### 补充服务系统

| 论文 | 本地 PDF | 与 DLoop 的关系 |
| --- | --- | --- |
| [TurboSpec: Closed-loop Speculation Control System for Optimizing LLM Serving Goodput](09_服务系统与RL流程/arXiv2024-TurboSpec/README.md) | [PDF](09_服务系统与RL流程/arXiv2024-TurboSpec/TurboSpec.pdf) | DLoop 参考文献及服务讨论涉及的闭环控制工作，不属于第 2 节核心列表。 |
| [The Synergy of Speculative Decoding and Batching in Serving Large Language Models](09_服务系统与RL流程/arXiv2023-SDBatching/README.md) | [PDF](09_服务系统与RL流程/arXiv2023-SDBatching/SDBatching.pdf) | DLoop 服务讨论涉及的 batching 与 speculative decoding 交互。 |

### 补充推理背景

| 论文 | 本地 PDF | 与 DLoop 的关系 |
| --- | --- | --- |
| [Efficiently Scaling Transformer Inference](17_长上下文与近似计算/MLSys2023-ScalingInference/README.md) | [PDF](17_长上下文与近似计算/MLSys2023-ScalingInference/ScalingInference.pdf) | DLoop 引言引用其解释目标模型验证延迟随 token 数增长较缓的背景。 |

### 官方博客引用

[Qwen3.5: Towards Native Multimodal Agents](16_MTP与蒸馏背景/Blog2026-Qwen3.5/README.md)：DLoop 引用的 MTP 来源之一；原始引用是网页，未找到与该引用完全对应的独立论文 PDF。
