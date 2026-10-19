# 2026 年三大会议：推测解码论文扩展目录

核查日期：2026-10-11。本批筛选 **95 篇**，其中 **79 篇已有 PDF**，**16 篇 PDF 待补**。与原 DLoop 文献库重复的 DFlash、SpecBlock、VAT 共 3 篇复用已有 PDF，没有重复收录。合并后共 122 篇方法、系统或相关背景论文，106 篇已有 PDF；DLoop 原文和 Qwen 博客单独保留。

## 来源与覆盖范围

从官方主会目录按 `speculat`、`draft`、`eagle`、多 token 预测等标题关键词筛选，再检查官方摘要，排除明显无关结果。本批是可核查的扩展检索，不保证穷尽所有未在标题出现关键词的论文。包括核心语言模型 SD、系统/训练/分析，以及扩散、视觉、语音、Agent 等扩展；相邻 MTP、蒸馏或剪枝工作明确标注。

- ICML：[官方目录](https://icml.cc/Downloads/2026)，并核对 [PMLR 正式论文集](https://proceedings.mlr.press/v306/)。
- ICLR：[官方目录](https://iclr.cc/Downloads/2026)，并核对 [正式论文集](https://proceedings.iclr.cc/paper_files/paper/2026)。
- NeurIPS：[官方目录](https://neurips.cc/Downloads/2026) 的主会 Poster 条目确认录用信息；此次检索未取得 2026 正式论文集，已下载的 PDF 为作者公开预印本。不要把目录中的会议年份误作 PDF 版本年份。

| 会议 | 收录条目 | 已有 PDF | PDF 待补 |
| --- | ---: | ---: | ---: |
| ICML 2026 | 32 | 32 | 0 |
| ICLR 2026 | 23 | 23 | 0 |
| NeurIPS 2026 | 40 | 24 | 16 |

## 围绕 DLoop 的优先阅读顺序

1. **并行与跨块起草**：DFlash → P-EAGLE → SpecBlock。比较块内并行、跨块迭代与 DLoop 多轮完整起草的区别。
2. **训练偏移与接受率**：AttentionDrift → VAT → D-PACE → LKLosses → TTS。比较漂移原因、监督权重、接受率目标与在线适应。
3. **起草和验证的组织方式**：SSD-Saguaro → SpecBranch → LTD → SwitchSD。比较重叠执行、拒绝分支准备、动态控制与延后验证。
4. **树结构与验证保证**：BASTION → TALON → DelayedTreeExpansion → TreeGraft → UniVer / GlobalResolution / HSD。区分候选覆盖与验证正确性。
5. **系统收益的边界**：ECHO → MineDraft → BubbleSpec / FastGRPO / EfficientRollout → SPEED-Bench。检查负载、并发、RL 策略变化和端到端吞吐。

以上是按研究问题组织的阅读建议，不是实验性能排名。各条摘要仅作初步导航，正文里的保证和实验仍需精读。

## ICML 2026

### 相邻：MTP 训练

| 论文 / 子目录 | PDF | 内容与定位 |
| --- | --- | --- |
| [AdaHC](16_MTP与蒸馏背景/ICML2026-AdaHC/README.md) | [PDF](16_MTP与蒸馏背景/ICML2026-AdaHC/AdaHC.pdf) | 通过预测头分块和调度提高多 token 预测训练效率，主要贡献在训练流水线。 |

### 服务与 RL 系统

| 论文 / 子目录 | PDF | 内容与定位 |
| --- | --- | --- |
| [BubbleSpec](09_服务系统与RL流程/ICML2026-BubbleSpec/README.md) | [PDF](09_服务系统与RL流程/ICML2026-BubbleSpec/BubbleSpec.pdf) | 利用 RL rollout 长尾造成的空闲计算起草下一轮候选，再同步验证。 |
| [ECHO](09_服务系统与RL流程/ICML2026-ECHO/README.md) | [PDF](09_服务系统与RL流程/ICML2026-ECHO/ECHO.pdf) | 用批量超级树和置信度预算分配候选深度、宽度，面向高并发服务。 |
| [MineDraft](09_服务系统与RL流程/ICML2026-MineDraft/README.md) | [PDF](09_服务系统与RL流程/ICML2026-MineDraft/MineDraft.pdf) | 交错两个批次的起草与验证，提高执行重叠和系统利用率。 |
| [PipeSD](09_服务系统与RL流程/ICML2026-PipeSD/README.md) | [PDF](09_服务系统与RL流程/ICML2026-PipeSD/PipeSD.pdf) | 在端云环境流水化 token 生成与通信，并自适应决定通信、验证时机。 |
| [SpecForge](09_服务系统与RL流程/ICML2026-SpecForge/README.md) | [PDF](09_服务系统与RL流程/ICML2026-SpecForge/SpecForge.pdf) | 提供草稿模型训练基础设施，支持 EAGLE-3 等方法，重点是训练流程与工程。 |
| [AdaptiveSpecTraining](09_服务系统与RL流程/ICML2026-AdaptiveSpecTraining/README.md) | [PDF](09_服务系统与RL流程/ICML2026-AdaptiveSpecTraining/AdaptiveSpecTraining.pdf) | 把 RL 更新和自适应推测训练、服务结合，处理策略持续变化时的起草效率。 |

### 草稿架构与训练

| 论文 / 子目录 | PDF | 内容与定位 |
| --- | --- | --- |
| [ConFu](02_草稿架构与训练/ICML2026-ConFu/README.md) | [PDF](02_草稿架构与训练/ICML2026-ConFu/ConFu.pdf) | 用面向未来的辅助信息改善草稿模型预测，缓解多步起草的误差累积。 |
| [ESP](02_草稿架构与训练/ICML2026-ESP/README.md) | [PDF](02_草稿架构与训练/ICML2026-ESP/ESP.pdf) | 在嵌入空间探测多个未来位置，构建和裁剪候选树，减少专门训练草稿模型的需要。 |
| [LKLosses](02_草稿架构与训练/ICML2026-LKLosses/README.md) | [PDF](02_草稿架构与训练/ICML2026-LKLosses/LKLosses.pdf) | 直接优化接受率相关损失，而不是只用 token 似然或 KL 作为训练代理。 |
| [NanoSpec](02_草稿架构与训练/ICML2026-NanoSpec/README.md) | [PDF](02_草稿架构与训练/ICML2026-NanoSpec/NanoSpec.pdf) | 利用上下文相关小词表及输出投影优化，降低轻量草稿模型的输出开销。 |
| [VSD](02_草稿架构与训练/ICML2026-VSD/README.md) | [PDF](02_草稿架构与训练/ICML2026-VSD/VSD.pdf) | 从序列接受概率出发设计变分训练目标，改善仅优化逐 token 似然的局限。 |
| [WhenDraftsEvolve](02_草稿架构与训练/ICML2026-WhenDraftsEvolve/README.md) | [PDF](02_草稿架构与训练/ICML2026-WhenDraftsEvolve/WhenDraftsEvolve.pdf) | 把不断变化的草稿模型与在线学习结合，研究动态适应与解码行为。 |

### 扩展：视觉生成

| 论文 / 子目录 | PDF | 内容与定位 |
| --- | --- | --- |
| [CSD](12_图像与三维生成/ICML2026-CSD/README.md) | [PDF](12_图像与三维生成/ICML2026-CSD/CSD.pdf) | 按图像内容与预测熵调整接受条件和重采样；不能直接套用标准 SD 的分布保持结论。 |
| [SJD-SV](12_图像与三维生成/ICML2026-SJD-SV/README.md) | [PDF](12_图像与三维生成/ICML2026-SJD-SV/SJD-SV.pdf) | 把语义层验证引入视觉 Jacobi 解码，需要同时检查生成质量与加速收益。 |
| [SpeculativeCoupledDecoding](12_图像与三维生成/ICML2026-SpeculativeCoupledDecoding/README.md) | [PDF](12_图像与三维生成/ICML2026-SpeculativeCoupledDecoding/SpeculativeCoupledDecoding.pdf) | 通过耦合采样加速自回归视觉生成，论文强调其分布保持条件。 |
| [XSpecMesh](12_图像与三维生成/ICML2026-XSpecMesh/README.md) | [PDF](12_图像与三维生成/ICML2026-XSpecMesh/XSpecMesh.pdf) | 将多头推测解码用于自回归三维网格生成。 |

### 扩展：扩散语言模型

| 论文 / 子目录 | PDF | 内容与定位 |
| --- | --- | --- |
| [DC-Leap](11_扩散语言模型/ICML2026-DC-Leap/README.md) | [PDF](11_扩散语言模型/ICML2026-DC-Leap/DC-Leap.pdf) | 利用中等置信度位置的连续验证加速扩散语言模型；质量相近不等于严格保持采样分布。 |
| [TrajectorySD](11_扩散语言模型/ICML2026-TrajectorySD/README.md) | [PDF](11_扩散语言模型/ICML2026-TrajectorySD/TrajectorySD.pdf) | 在扩散语言模型的生成轨迹层面开展推测；不同于 DFlash 用扩散草稿服务自回归目标模型。 |

### 并行草稿

| 论文 / 子目录 | PDF | 内容与定位 |
| --- | --- | --- |
| [DFlash](03_并行与半自回归草稿/ICML2026-DFlash/README.md) | [PDF](03_并行与半自回归草稿/ICML2026-DFlash/DFlash.pdf) | 目标特征条件的块扩散模型并行起草，是 DLoop 的核心实验基线。 |

### 扩展：多模态推理

| 论文 / 子目录 | PDF | 内容与定位 |
| --- | --- | --- |
| [DREAM-R](13_多模态与VLA/ICML2026-DREAM-R/README.md) | [PDF](13_多模态与VLA/ICML2026-DREAM-R/DREAM-R.pdf) | 以推理步骤为起草单元，并用强化学习对齐草稿模型；需区分步骤接受与标准逐 token SD。 |

### 长上下文与近似计算

| 论文 / 子目录 | PDF | 内容与定位 |
| --- | --- | --- |
| [Dustin](17_长上下文与近似计算/ICML2026-Dustin/README.md) | [PDF](17_长上下文与近似计算/ICML2026-Dustin/Dustin.pdf) | 结合草稿前瞻和历史注意力选择 KV，降低长上下文验证开销；需单独核查稀疏验证的精度保证。 |

### 自推测与跳层

| 论文 / 子目录 | PDF | 内容与定位 |
| --- | --- | --- |
| [FAFO](05_自推测与计算裁剪/ICML2026-FAFO/README.md) | [PDF](05_自推测与计算裁剪/ICML2026-FAFO/FAFO.pdf) | 在同一次执行中结合压缩 KV 的近似候选与完整验证，减少单独起草的开销。 |
| [KnapSpec](05_自推测与计算裁剪/ICML2026-KnapSpec/README.md) | [PDF](05_自推测与计算裁剪/ICML2026-KnapSpec/KnapSpec.pdf) | 把注意力和 MLP 层的选择建模为受硬件延迟约束的组合优化。 |
| [LEAP](05_自推测与计算裁剪/ICML2026-LEAP/README.md) | [PDF](05_自推测与计算裁剪/ICML2026-LEAP/LEAP.pdf) | 通过分区层分组和搜索选择自推测的计算路径。 |
| [Vegas](05_自推测与计算裁剪/ICML2026-Vegas/README.md) | [PDF](05_自推测与计算裁剪/ICML2026-Vegas/Vegas.pdf) | 以稀疏注意力构造自身草稿，再由完整目标模型验证。 |

### 放宽验证与推理加速

| 论文 / 子目录 | PDF | 内容与定位 |
| --- | --- | --- |
| [SelfJudge](08_放宽验证与推理加速/ICML2026-SelfJudge/README.md) | [PDF](08_放宽验证与推理加速/ICML2026-SelfJudge/SelfJudge.pdf) | 用目标模型提供语义判断来接受候选，需区别语义质量保持与严格采样分布保持。 |
| [SpecExit](08_放宽验证与推理加速/ICML2026-SpecExit/README.md) | [PDF](08_放宽验证与推理加速/ICML2026-SpecExit/SpecExit.pdf) | 草稿模型同时预测未来 token 和提前结束推理的信号；包含输出长度变化。 |
| [VIA-SD](08_放宽验证与推理加速/ICML2026-VIA-SD/README.md) | [PDF](08_放宽验证与推理加速/ICML2026-VIA-SD/VIA-SD.pdf) | 在直接接受、精简验证器和完整模型之间路由；不能仅凭质量指标推定等同标准 SD 输出分布。 |

### 相邻：VLA 剪枝

| 论文 / 子目录 | PDF | 内容与定位 |
| --- | --- | --- |
| [SpecPrune-VLA](13_多模态与VLA/ICML2026-SpecPrune-VLA/README.md) | [PDF](13_多模态与VLA/ICML2026-SpecPrune-VLA/SpecPrune-VLA.pdf) | 根据时空一致性进行视觉 token 的动作级、层级剪枝；官方摘要描述的是剪枝方法，并非典型 draft-verify SD。 |

### 基准与分析

| 论文 / 子目录 | PDF | 内容与定位 |
| --- | --- | --- |
| [SPEED-Bench](10_基准与机制分析/ICML2026-SPEED-Bench/README.md) | [PDF](10_基准与机制分析/ICML2026-SPEED-Bench/SPEED-Bench.pdf) | 评测不同任务、模型和负载下的推测解码延迟与吞吐，适合检查单点加速能否泛化。 |
| [DraftConditionedDecoding](10_基准与机制分析/ICML2026-DraftConditionedDecoding/README.md) | [PDF](10_基准与机制分析/ICML2026-DraftConditionedDecoding/DraftConditionedDecoding.pdf) | 研究结构化生成约束与草稿条件化之间的相互影响，分析接受率和实际速度的变化。 |

## ICLR 2026

### 相邻：MTP 训练

| 论文 / 子目录 | PDF | 内容与定位 |
| --- | --- | --- |
| [FSP](16_MTP与蒸馏背景/ICLR2026-FSP/README.md) | [PDF](16_MTP与蒸馏背景/ICLR2026-FSP/FSP.pdf) | 通过未来内容摘要改进预训练中的多 token 预测，属于草稿能力的训练背景。 |

### 草稿架构与训练

| 论文 / 子目录 | PDF | 内容与定位 |
| --- | --- | --- |
| [GTO](02_草稿架构与训练/ICLR2026-GTO/README.md) | [PDF](02_草稿架构与训练/ICLR2026-GTO/GTO.pdf) | 用组树优化对齐草稿策略与候选树的期望收益，而非仅拟合单一路径。 |
| [SFDD](02_草稿架构与训练/ICLR2026-SFDD/README.md) | [PDF](02_草稿架构与训练/ICLR2026-SFDD/SFDD.pdf) | 发现目标分布较平坦的 token 对草稿训练更有价值，据此进行训练样本选择。 |
| [PARD](03_并行与半自回归草稿/ICLR2026-PARD/README.md) | [PDF](03_并行与半自回归草稿/ICLR2026-PARD/PARD.pdf) | 构造独立于目标模型内部状态的并行草稿，并以轻量适应改善兼容性。 |
| [RepSpec](02_草稿架构与训练/ICLR2026-RepSpec/README.md) | [PDF](02_草稿架构与训练/ICLR2026-RepSpec/RepSpec.pdf) | 训练时使用额外可重参数化结构，推理时合并结构以控制起草成本。 |

### 放宽验证与推理加速

| 论文 / 子目录 | PDF | 内容与定位 |
| --- | --- | --- |
| [Cactus](08_放宽验证与推理加速/ICLR2026-Cactus/README.md) | [PDF](08_放宽验证与推理加速/ICLR2026-Cactus/Cactus.pdf) | 在受控分布偏移约束下提高接受效率；与严格无损 SD 的保证不同。 |
| [GSI](08_放宽验证与推理加速/ICLR2026-GSI/README.md) | [PDF](08_放宽验证与推理加速/ICLR2026-GSI/GSI.pdf) | 以奖励引导推测生成实现测试时对齐；目标是受奖励调整的策略，需要明确参考分布。 |
| [FLy](08_放宽验证与推理加速/ICLR2026-FLy/README.md) | [PDF](08_放宽验证与推理加速/ICLR2026-FLy/FLy.pdf) | 接受语义正确但不完全匹配的草稿，因此质量保证应与严格目标分布保持区分。 |

### 长上下文与近似计算

| 论文 / 子目录 | PDF | 内容与定位 |
| --- | --- | --- |
| [DraftApproxInference](17_长上下文与近似计算/ICLR2026-DraftApproxInference/README.md) | [PDF](17_长上下文与近似计算/ICLR2026-DraftApproxInference/DraftApproxInference.pdf) | 利用草稿前瞻估计重要 KV，主要研究近似推理计算的分配。 |

### 扩展：Agent

| 论文 / 子目录 | PDF | 内容与定位 |
| --- | --- | --- |
| [DynamicSpecPlanning](15_Agent与检索规划/ICLR2026-DynamicSpecPlanning/README.md) | [PDF](15_Agent与检索规划/ICLR2026-DynamicSpecPlanning/DynamicSpecPlanning.pdf) | 动态组织 Agent 的推测规划，关注规划延迟与执行行为。 |
| [SpeculativeActions](15_Agent与检索规划/ICLR2026-SpeculativeActions/README.md) | [PDF](15_Agent与检索规划/ICLR2026-SpeculativeActions/SpeculativeActions.pdf) | 并行推测后续动作，再按验证结果选择或回滚；比较对象是 Agent 执行轨迹。 |

### 服务与 RL 系统

| 论文 / 子目录 | PDF | 内容与定位 |
| --- | --- | --- |
| [FastGRPO](09_服务系统与RL流程/ICLR2026-FastGRPO/README.md) | [PDF](09_服务系统与RL流程/ICLR2026-FastGRPO/FastGRPO.pdf) | 将并发感知解码与在线草稿更新用于 GRPO rollout。 |

### 候选树与采样验证

| 论文 / 子目录 | PDF | 内容与定位 |
| --- | --- | --- |
| [GlobalResolution](04_候选树与采样验证/ICLR2026-GlobalResolution/README.md) | [PDF](04_候选树与采样验证/ICLR2026-GlobalResolution/GlobalResolution.pdf) | 把多候选最优接受问题转成凸优化，减少直接求解最优传输的复杂度。 |
| [HSD](04_候选树与采样验证/ICLR2026-HSD/README.md) | [PDF](04_候选树与采样验证/ICLR2026-HSD/HSD.pdf) | 通过层级验证处理联合候选分布，重点是分布保持与多候选计算的平衡。 |

### 基准与分析

| 论文 / 子目录 | PDF | 内容与定位 |
| --- | --- | --- |
| [WatermarkSD](10_基准与机制分析/ICLR2026-WatermarkSD/README.md) | [PDF](10_基准与机制分析/ICLR2026-WatermarkSD/WatermarkSD.pdf) | 研究文本水印强度与推测采样效率之间的权衡。 |
| [ScalingUpSpeedingUp](10_基准与机制分析/ICLR2026-ScalingUpSpeedingUp/README.md) | [PDF](10_基准与机制分析/ICLR2026-ScalingUpSpeedingUp/ScalingUpSpeedingUp.pdf) | 面向推理与测试时扩展评测 SD，区分单条生成加速与多轨迹推理整体成本。 |

### 调度与执行重叠

| 论文 / 子目录 | PDF | 内容与定位 |
| --- | --- | --- |
| [LTD](06_自适应调度与执行重叠/ICLR2026-LTD/README.md) | [PDF](06_自适应调度与执行重叠/ICLR2026-LTD/LTD.pdf) | 用强化学习共同调整起草和验证策略，优化实际解码周期吞吐。 |
| [Not-a-Bandit](06_自适应调度与执行重叠/ICLR2026-Not-a-Bandit/README.md) | [PDF](06_自适应调度与执行重叠/ICLR2026-Not-a-Bandit/Not-a-Bandit.pdf) | 利用目标模型反馈评估多个草稿器，研究具有无遗憾保证的在线草稿选择。 |
| [SpecBranch](06_自适应调度与执行重叠/ICLR2026-SpecBranch/README.md) | [PDF](06_自适应调度与执行重叠/ICLR2026-SpecBranch/SpecBranch.pdf) | 预先准备可能被拒绝位置的后续分支，使起草和验证重叠，并处理回滚。 |
| [SSD-Saguaro](06_自适应调度与执行重叠/ICLR2026-SSD-Saguaro/README.md) | [PDF](06_自适应调度与执行重叠/ICLR2026-SSD-Saguaro/SSD-Saguaro.pdf) | 预测当前验证的可能结果并提前起草下一轮，以重叠起草和验证；与 DLoop 延后验证的组织方式不同。 |

### 扩展：任意顺序模型

| 论文 / 子目录 | PDF | 内容与定位 |
| --- | --- | --- |
| [ASSD](05_自推测与计算裁剪/ICLR2026-ASSD/README.md) | [PDF](05_自推测与计算裁剪/ICLR2026-ASSD/ASSD.pdf) | 研究任意顺序、任意子集自回归模型中的并行自推测及正确联合采样。 |

### 扩展：扩散语言模型

| 论文 / 子目录 | PDF | 内容与定位 |
| --- | --- | --- |
| [SSMD](11_扩散语言模型/ICLR2026-SSMD/README.md) | [PDF](11_扩散语言模型/ICLR2026-SSMD/SSMD.pdf) | 将自推测用于掩码扩散模型，考虑并行预测之间的依赖。 |

### 扩展：多模态推理

| 论文 / 子目录 | PDF | 内容与定位 |
| --- | --- | --- |
| [SpeculativeVerdict](13_多模态与VLA/ICLR2026-SpeculativeVerdict/README.md) | [PDF](13_多模态与VLA/ICLR2026-SpeculativeVerdict/SpeculativeVerdict.pdf) | 轻量专家提出视觉推理候选，大模型给出判断；不宜直接视为普通 token 级 SD。 |

## NeurIPS 2026

### 候选树与采样验证

| 论文 / 子目录 | PDF | 内容与定位 |
| --- | --- | --- |
| [AdaTree](04_候选树与采样验证/NeurIPS2026-AdaTree/README.md) | 待补 | 依据预计验证时间、接受长度及服务负载自适应选择候选树配置。 |
| [BASTION](04_候选树与采样验证/NeurIPS2026-BASTION/README.md) | [PDF](04_候选树与采样验证/NeurIPS2026-BASTION/BASTION.pdf) | 为块扩散草稿构造动态树，结合置信度、预计接受收益和硬件验证成本分配节点。 |
| [DelayedTreeExpansion](04_候选树与采样验证/NeurIPS2026-DelayedTreeExpansion/README.md) | [PDF](04_候选树与采样验证/NeurIPS2026-DelayedTreeExpansion/DelayedTreeExpansion.pdf) | 把多路径分支推迟到更可能分歧的深度，减少浅层无效扩张。 |
| [EfficientTreeDraft](04_候选树与采样验证/NeurIPS2026-EfficientTreeDraft/README.md) | 待补 | 论文方法名 FastDraft：优化共享前缀、树起草和长上下文访存开销。 |
| [Gumbo](04_候选树与采样验证/NeurIPS2026-Gumbo/README.md) | 待补 | 以 Gumbel 分数扩展和重排候选树，并通过耦合采样处理高温下的正确性问题。 |
| [RheoSampling](04_候选树与采样验证/NeurIPS2026-RheoSampling/README.md) | [PDF](04_候选树与采样验证/NeurIPS2026-RheoSampling/RheoSampling.pdf) | 解耦随机采样分布与动态候选树构造，处理非零温度的多候选生成。 |
| [TALON](04_候选树与采样验证/NeurIPS2026-TALON/README.md) | [PDF](04_候选树与采样验证/NeurIPS2026-TALON/TALON.pdf) | 在固定节点预算内自适应选择深窄或浅宽候选树。 |
| [TreeGraft](04_候选树与采样验证/NeurIPS2026-TreeGraft/README.md) | [PDF](04_候选树与采样验证/NeurIPS2026-TreeGraft/TreeGraft.pdf) | 把强弱草稿的候选树重评分并嫁接，恢复单一草稿未覆盖的路径。 |
| [UniVer](04_候选树与采样验证/NeurIPS2026-UniVer/README.md) | [PDF](04_候选树与采样验证/NeurIPS2026-UniVer/UniVer.pdf) | 以条件最优传输统一多步、多草稿验证，并明确分布保持条件。 |
| [ValuSpec](04_候选树与采样验证/NeurIPS2026-ValuSpec/README.md) | 待补 | 在目标验证前剔除低价值分支；论文摘要强调与贪心输出一致，需要区别随机采样保证。 |

### 基准与分析

| 论文 / 子目录 | PDF | 内容与定位 |
| --- | --- | --- |
| [AttentionDrift](10_基准与机制分析/NeurIPS2026-AttentionDrift/README.md) | [PDF](10_基准与机制分析/NeurIPS2026-AttentionDrift/AttentionDrift.pdf) | 分析连续起草中注意力逐渐从输入转向自身 token 的漂移及其缓解方法，关联 DLoop 的跨轮误差问题。 |
| [PerTokenNotPath](10_基准与机制分析/NeurIPS2026-PerTokenNotPath/README.md) | 待补 | 分析逐 token 接受率与整条路径重叠的区别；理论结论需限定在论文讨论的验证协议内。 |
| [MoESDSpeedup](10_基准与机制分析/NeurIPS2026-MoESDSpeedup/README.md) | 待补 | 分析稀疏 MoE 的跨 token 专家重叠与动态 GPU 执行对验证延迟的影响。 |

### 相邻：MTP 训练

| 论文 / 子目录 | PDF | 内容与定位 |
| --- | --- | --- |
| [BitMTP](16_MTP与蒸馏背景/NeurIPS2026-BitMTP/README.md) | 待补 | 结合低比特模型和多 token 预测，考虑接受前缀对齐以及算法与系统配合。 |
| [MTPInformationLoss](16_MTP与蒸馏背景/NeurIPS2026-MTPInformationLoss/README.md) | 待补 | 论文方法名 Dual-MTP：分析多 token 预测的信息损失，以双向与随机掩码训练改善位置依赖。 |

### 扩展：多模态推理

| 论文 / 子目录 | PDF | 内容与定位 |
| --- | --- | --- |
| [CATS](13_多模态与VLA/NeurIPS2026-CATS/README.md) | 待补 | 针对多模态草稿训练中的难接受位置与关键视觉信息进行对齐。 |
| [SP2ec](13_多模态与VLA/NeurIPS2026-SP2ec/README.md) | 待补 | 面向视觉语言模型自适应跳层，依据实际时间反馈选择自推测配置。 |

### 草稿架构与训练

| 论文 / 子目录 | PDF | 内容与定位 |
| --- | --- | --- |
| [D-PACE](02_草稿架构与训练/NeurIPS2026-D-PACE/README.md) | [PDF](02_草稿架构与训练/NeurIPS2026-D-PACE/D-PACE.pdf) | 根据期望接受长度对各预测位置的训练损失动态加权。 |
| [EDA](02_草稿架构与训练/NeurIPS2026-EDA/README.md) | [PDF](02_草稿架构与训练/NeurIPS2026-EDA/EDA.pdf) | 通过参数高效与数据高效适应对齐草稿，处理目标模型变化。 |
| [PPOW](02_草稿架构与训练/NeurIPS2026-PPOW/README.md) | [PDF](02_草稿架构与训练/NeurIPS2026-PPOW/PPOW.pdf) | 以窗口为单位优化成本感知策略，并用适应性窗口和课程训练改善起草。 |
| [SEED](05_自推测与计算裁剪/NeurIPS2026-SEED/README.md) | [PDF](05_自推测与计算裁剪/NeurIPS2026-SEED/SEED.pdf) | 缓存已验证的深层特征，利用轻量末层起草，形成隐式编码器—解码器结构。 |
| [TTS](02_草稿架构与训练/NeurIPS2026-TTS/README.md) | [PDF](02_草稿架构与训练/NeurIPS2026-TTS/TTS.pdf) | 利用验证反馈在线进行测试时蒸馏，缓解长输出中的草稿分布失配。 |
| [VAT](02_草稿架构与训练/NeurIPS2026-VAT/README.md) | [PDF](02_草稿架构与训练/NeurIPS2026-VAT/VAT.pdf) | 训练时模拟验证行为并调整监督权重，与 DLoop 的 loop-aware training 可对照。 |

### 服务与 RL 系统

| 论文 / 子目录 | PDF | 内容与定位 |
| --- | --- | --- |
| [EfficientRollout](09_服务系统与RL流程/NeurIPS2026-EfficientRollout/README.md) | [PDF](09_服务系统与RL流程/NeurIPS2026-EfficientRollout/EfficientRollout.pdf) | 结合量化自推测和自适应长度，提升持续更新策略的 RL rollout 效率。 |
| [InSTeP](09_服务系统与RL流程/NeurIPS2026-InSTeP/README.md) | 待补 | 让 CPU 与 GPU 上的嵌套草稿、目标计算并行执行，结合显著 FFN 通道选择。 |
| [KeepOrPreempt](09_服务系统与RL流程/NeurIPS2026-KeepOrPreempt/README.md) | 待补 | 论文方法名 AlmostDone：把接受效率与请求即将结束的概率纳入抢占调度。 |
| [LADDERS](09_服务系统与RL流程/NeurIPS2026-LADDERS/README.md) | 待补 | 结合响应长度预测、GPU 分配和前轮 rollout 后缀复用，减少 RL 生成长尾。 |

### 扩展：扩散语言模型

| 论文 / 子目录 | PDF | 内容与定位 |
| --- | --- | --- |
| [FreeDave](11_扩散语言模型/NeurIPS2026-FreeDave/README.md) | [PDF](11_扩散语言模型/NeurIPS2026-FreeDave/FreeDave.pdf) | 复用扩散生成计算执行起草与验证；其无损参照是特定静态扩散解码器。 |
| [PSD](11_扩散语言模型/NeurIPS2026-PSD/README.md) | [PDF](11_扩散语言模型/NeurIPS2026-PSD/PSD.pdf) | 从一次扩散预测构造多深度候选并分层验证，结合自适应解掩码。 |
| [SimSD](11_扩散语言模型/NeurIPS2026-SimSD/README.md) | [PDF](11_扩散语言模型/NeurIPS2026-SimSD/SimSD.pdf) | 把参考 token 放入合法的扩散时间上下文，实现单次执行中的候选验证。 |

### 并行草稿

| 论文 / 子目录 | PDF | 内容与定位 |
| --- | --- | --- |
| [P-EAGLE](03_并行与半自回归草稿/NeurIPS2026-P-EAGLE/README.md) | [PDF](03_并行与半自回归草稿/NeurIPS2026-P-EAGLE/P-EAGLE.pdf) | 学习共享隐藏表示并并行预测多个位置，避免逐 token 自回归起草。 |

### 扩展：VLA

| 论文 / 子目录 | PDF | 内容与定位 |
| --- | --- | --- |
| [RealtimeVLA-FLASH](13_多模态与VLA/NeurIPS2026-RealtimeVLA-FLASH/README.md) | [PDF](13_多模态与VLA/NeurIPS2026-RealtimeVLA-FLASH/RealtimeVLA-FLASH.pdf) | 由轻量动作草稿与动作专家验证配合，并按执行阶段调整回退策略。 |

### 扩展：语音

| 论文 / 子目录 | PDF | 内容与定位 |
| --- | --- | --- |
| [SpecSpeak](14_语音生成/NeurIPS2026-SpecSpeak/README.md) | 待补 | 在 LLM 验证文本草稿期间提前合成语音，降低首段语音延迟。 |

### 跨块起草

| 论文 / 子目录 | PDF | 内容与定位 |
| --- | --- | --- |
| [SpecBlock](07_跨块与多轮起草/NeurIPS2026-SpecBlock/README.md) | [PDF](07_跨块与多轮起草/NeurIPS2026-SpecBlock/SpecBlock.pdf) | 训练跨块迭代草稿与排序头，是比较 DLoop 连续多轮起草机制的直接近邻。 |

### 扩展：Agent

| 论文 / 子目录 | PDF | 内容与定位 |
| --- | --- | --- |
| [SpecHop](15_Agent与检索规划/NeurIPS2026-SpecHop/README.md) | [PDF](15_Agent与检索规划/NeurIPS2026-SpecHop/SpecHop.pdf) | 用快速工具异步推测后续执行，依据真实工具观察验证并回滚。 |

### 放宽验证与推理加速

| 论文 / 子目录 | PDF | 内容与定位 |
| --- | --- | --- |
| [SPECS](08_放宽验证与推理加速/NeurIPS2026-SPECS/README.md) | [PDF](08_放宽验证与推理加速/NeurIPS2026-SPECS/SPECS.pdf) | 在推理过程中动态切换奖励引导的草稿，关注速度与推理质量的权衡。 |
| [TriSpec](08_放宽验证与推理加速/NeurIPS2026-TriSpec/README.md) | [PDF](08_放宽验证与推理加速/NeurIPS2026-TriSpec/TriSpec.pdf) | 引入轻量代理验证减少完整目标模型调用；精度接近不能自动等同严格无损。 |

### 相邻：蒸馏训练

| 论文 / 子目录 | PDF | 内容与定位 |
| --- | --- | --- |
| [SpeculativeSelfDistillation](16_MTP与蒸馏背景/NeurIPS2026-SpeculativeSelfDistillation/README.md) | 待补 | 学生生成时只在高偏差位置请求教师干预，以推测思想降低知识蒸馏成本。 |

### 自推测与跳层

| 论文 / 子目录 | PDF | 内容与定位 |
| --- | --- | --- |
| [SPIRIT](05_自推测与计算裁剪/NeurIPS2026-SPIRIT/README.md) | 待补 | 按窗口运行时间反馈调整跳层配置，直接优化自推测吞吐。 |

### 调度与执行重叠

| 论文 / 子目录 | PDF | 内容与定位 |
| --- | --- | --- |
| [SwitchSD](06_自适应调度与执行重叠/NeurIPS2026-SwitchSD/README.md) | [PDF](06_自适应调度与执行重叠/NeurIPS2026-SwitchSD/SwitchSD.pdf) | 通过目标表示中的内部信号，在神经草稿与上下文复制之间切换。 |

## PDF 待补清单

这些条目已经确认官方会议来源并建立子目录，README 留有论文页面、下载失败原因；没有把网页、海报或幻灯片冒充论文 PDF。

| 目录 | 完整标题 | 官方来源 |
| --- | --- | --- |
| [NeurIPS2026-AdaTree](04_候选树与采样验证/NeurIPS2026-AdaTree/README.md) | AdaTree: Serving-Aware Adaptive Tree Construction for Speculative Decoding | [官方页面](https://neurips.cc/virtual/2026/poster/153118) |
| [NeurIPS2026-BitMTP](16_MTP与蒸馏背景/NeurIPS2026-BitMTP/README.md) | BitMTP: When Multi-Token Prediction Meets Low-Bit Large Language Models | [官方页面](https://neurips.cc/virtual/2026/poster/154757) |
| [NeurIPS2026-CATS](13_多模态与VLA/NeurIPS2026-CATS/README.md) | CATS: Acceptance-Oriented Critical Token Adaptive Selection for Multimodal Speculative Decoding | [官方页面](https://neurips.cc/virtual/2026/poster/154883) |
| [NeurIPS2026-EfficientTreeDraft](04_候选树与采样验证/NeurIPS2026-EfficientTreeDraft/README.md) | Efficient Tree Draft for Long-Context Speculative Decoding | [官方页面](https://neurips.cc/virtual/2026/poster/152500) |
| [NeurIPS2026-Gumbo](04_候选树与采样验证/NeurIPS2026-Gumbo/README.md) | Gumbo: Gumbel Optimized High-Temperature Speculative Sampling | [官方页面](https://neurips.cc/virtual/2026/poster/150279) |
| [NeurIPS2026-InSTeP](09_服务系统与RL流程/NeurIPS2026-InSTeP/README.md) | In STeP: Speculative Tensor Parallelism for Concurrent Heterogeneous Inference of LLMs | [官方页面](https://neurips.cc/virtual/2026/poster/155402) |
| [NeurIPS2026-KeepOrPreempt](09_服务系统与RL流程/NeurIPS2026-KeepOrPreempt/README.md) | Keep or Preempt? Termination-Aware Scheduling for LLM Serving with Speculative Decoding | [官方页面](https://neurips.cc/virtual/2026/poster/152245) |
| [NeurIPS2026-LADDERS](09_服务系统与RL流程/NeurIPS2026-LADDERS/README.md) | LADDERS: Length-Aware Data Distribution and Existing-Response Speculation for Fast RL Rollout Generation | [官方页面](https://neurips.cc/virtual/2026/poster/148499) |
| [NeurIPS2026-MTPInformationLoss](16_MTP与蒸馏背景/NeurIPS2026-MTPInformationLoss/README.md) | On the Information Loss of Multi-Token Prediction: Origin and Solution | [官方页面](https://neurips.cc/virtual/2026/poster/148174) |
| [NeurIPS2026-SP2ec](13_多模态与VLA/NeurIPS2026-SP2ec/README.md) | SP$^2$ec: Adaptive Self-Speculative Decoding for Vision-Language Models | [官方页面](https://neurips.cc/virtual/2026/poster/150441) |
| [NeurIPS2026-SpecSpeak](14_语音生成/NeurIPS2026-SpecSpeak/README.md) | Speak Early: Speculative Speech Generation for Low-Latency SpeechLLMs | [官方页面](https://neurips.cc/virtual/2026/poster/152241) |
| [NeurIPS2026-PerTokenNotPath](10_基准与机制分析/NeurIPS2026-PerTokenNotPath/README.md) | Speculative Decoding Is Per-Token, Not Path | [官方页面](https://neurips.cc/virtual/2026/poster/150210) |
| [NeurIPS2026-SpeculativeSelfDistillation](16_MTP与蒸馏背景/NeurIPS2026-SpeculativeSelfDistillation/README.md) | Speculative Self-Distillation enables Efficient Knowledge Internalization | [官方页面](https://neurips.cc/virtual/2026/poster/155356) |
| [NeurIPS2026-SPIRIT](05_自推测与计算裁剪/NeurIPS2026-SPIRIT/README.md) | SPIRIT: Speed-Driven Online Adaptation for Self-Speculative Decoding | [官方页面](https://neurips.cc/virtual/2026/poster/155523) |
| [NeurIPS2026-ValuSpec](04_候选树与采样验证/NeurIPS2026-ValuSpec/README.md) | ValuSpec: Plug-and-Play Candidate Valuation before Target Verification for Tree-Based Speculative Decoding | [官方页面](https://neurips.cc/virtual/2026/poster/154357) |
| [NeurIPS2026-MoESDSpeedup](10_基准与机制分析/NeurIPS2026-MoESDSpeedup/README.md) | Why Speculative Decoding Works Better Than Predicted on Sparse MoE Models | [官方页面](https://neurips.cc/virtual/2026/poster/150811) |

## 数据与复核

统一表：[papers.csv](papers.csv)。统一元数据：[papers_manifest.json](papers_manifest.json)。本批元数据：[conference_2026_manifest.json](conference_2026_manifest.json)。官方网页快照和候选名单保存于 `sources_2026/`。PDF 校验包括文件头、`pdfinfo`、页数和 SHA-256；首页标题采用词项匹配，低匹配项核查断词与版本差异。NeurIPS 的标题可能随预印本版本更新。

补下载运行 `python3 collect_2026.py`，再运行 `python3 render_2026.py` 更新索引；原 DLoop 目录见 [README](README.md)。
