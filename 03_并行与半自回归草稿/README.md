# 并行与半自回归草稿

一次预测多个 token，含块扩散草稿、多预测头和半自回归草稿。这里的扩散模型用于给自回归目标模型起草，与扩散语言模型自身的加速分开。

[全部分类](../CLASSIFICATION.md) · [ICLR2027 扩展](../ICLR2027.md)

| 论文 | PDF | 分类依据 |
| --- | --- | --- |
| [Medusa: Simple LLM Inference Acceleration Framework with Multiple Decoding Heads](ICML2024-Medusa/README.md) | [PDF](ICML2024-Medusa/Medusa.pdf) | 沿用已有分类、摘要与阅读记录，以主要贡献确定唯一物理目录。 |
| [DFlash: Block Diffusion for Flash Speculative Decoding](ICML2026-DFlash/README.md) | [PDF](ICML2026-DFlash/DFlash.pdf) | 沿用已有分类、摘要与阅读记录，以主要贡献确定唯一物理目录。 |
| [Domino: Decoupling Causal Modeling from Autoregressive Drafting in Speculative Decoding](arXiv2026-Domino/README.md) | [PDF](arXiv2026-Domino/Domino.pdf) | 沿用已有分类、摘要与阅读记录，以主要贡献确定唯一物理目录。 |
| [DSpark: Confidence-Scheduled Speculative Decoding with Semi-Autoregressive Generation](arXiv2026-DSpark/README.md) | [PDF](arXiv2026-DSpark/DSpark.pdf) | 沿用已有分类、摘要与阅读记录，以主要贡献确定唯一物理目录。 |
| [PARD: Accelerating LLM Inference with Low‑Cost PARallel Draft Model Adaptation](ICLR2026-PARD/README.md) | [PDF](ICLR2026-PARD/PARD.pdf) | 主要关注低成本并行草稿适配。 |
| [P-EAGLE: Parallel-Drafting EAGLE with Scalable Training](NeurIPS2026-P-EAGLE/README.md) | [PDF](NeurIPS2026-P-EAGLE/P-EAGLE.pdf) | 沿用已有分类、摘要与阅读记录，以主要贡献确定唯一物理目录。 |
| [DLite: History-Free Speculative Decoding for Agentic AI](ICLR2027-DLite/README.md) | [PDF](ICLR2027-DLite/DLite.pdf) | 主要问题是块内并行预测、半自回归依赖或并行草稿结构。 |
| [Efficient speculative decoding with a fixed-cost parallel drafter](ICLR2027-LongSpark/README.md) | [PDF](ICLR2027-LongSpark/LongSpark.pdf) | 主要问题是块内并行预测、半自回归依赖或并行草稿结构。 |
| [BagDraft: Next-Bag-of-Tokens Drafting for Lossless Speculative Decoding](ICLR2027-BagDraft/README.md) | 待补 | 主要问题是块内并行预测、半自回归依赖或并行草稿结构。 |
| [LiLiCorr: Lightweight Likelihood Correlation of Parallel Drafts for Speculative Decoding](ICLR2027-LiLiCorr/README.md) | [PDF](ICLR2027-LiLiCorr/LiLiCorr.pdf) | 主要问题是块内并行预测、半自回归依赖或并行草稿结构。 |
| [Give the Drafter a Second Chance to Guess: Parallel Reconsideration for Speculative Decoding](ICLR2027-GivetheDrafteraSecondChancetoGuess/README.md) | 待补 | 主要问题是块内并行预测、半自回归依赖或并行草稿结构。 |
| [Branch-Jacobi: Prefix-Conditioned Multi-Pass Drafting for Speculative Decoding](ICLR2027-Branch-Jacobi/README.md) | 待补 | 主要问题是块内并行预测、半自回归依赖或并行草稿结构。 |
| [DFlow: Enabling Verifier Information Flow in Block Diffusion Speculative Decoding](ICLR2027-DFlow/README.md) | [PDF](ICLR2027-DFlow/DFlow.pdf) | 主要问题是块内并行预测、半自回归依赖或并行草稿结构。 |
| [Caduceus: Parallel Speculative Decoding with Two Simple Drafters Intertwined](ICLR2027-Caduceus/README.md) | 待补 | 主要问题是块内并行预测、半自回归依赖或并行草稿结构。 |
| [XPress: Parallel Refinement for Diffusion Drafters in Speculative Decoding](ICLR2027-XPress/README.md) | [PDF](ICLR2027-XPress/XPress.pdf) | 主要问题是块内并行预测、半自回归依赖或并行草稿结构。 |
| [DEdit: Iterative Draft Editing for Speculative Decoding](ICLR2027-DEdit/README.md) | [PDF](ICLR2027-DEdit/DEdit.pdf) | 主要问题是块内并行预测、半自回归依赖或并行草稿结构。 |
| [Contextual Correction of Parallel Drafts for Speculative Decoding](ICLR2027-ContextualCorrectionofParallelDraftsfor/README.md) | [PDF](ICLR2027-ContextualCorrectionofParallelDraftsfor/ContextualCorrectionofParallelDraftsfor.pdf) | 主要问题是块内并行预测、半自回归依赖或并行草稿结构。 |
| [DRelay: Global Draft Context for Prefix-Aware Parallel Speculative Decoding Repair](ICLR2027-DRelay/README.md) | [PDF](ICLR2027-DRelay/DRelay.pdf) | 主要问题是块内并行预测、半自回归依赖或并行草稿结构。 |
| [D2-SD: Accelerating Speculative Decoding with Dual Diffusion Draft Models](ICLR2027-D2-SD/README.md) | [PDF](ICLR2027-D2-SD/D2-SD.pdf) | 主要问题是块内并行预测、半自回归依赖或并行草稿结构。 |
| [Compass: Repairing When Target-Model Guidance Hurts in Parallel Speculative Decoding](ICLR2027-Compass/README.md) | 待补 | 主要问题是块内并行预测、半自回归依赖或并行草稿结构。 |
| [JetSpec++: Foresight Parallel Drafting with Self Refinements](ICLR2027-JetSpec++/README.md) | [PDF](ICLR2027-JetSpec++/JetSpec++.pdf) | 主要问题是块内并行预测、半自回归依赖或并行草稿结构。 |
| [LatentSpec: Two-Stage Thinker–Drafter Parallel Drafting with Shared Latent Reasoning for Speculative Decoding](ICLR2027-LatentSpec/README.md) | 待补 | 主要问题是块内并行预测、半自回归依赖或并行草稿结构。 |
| [SchemaFill: Efficient LLM Tool Calling via Slot-Parallel Speculative Decoding](ICLR2027-SchemaFill/README.md) | [PDF](ICLR2027-SchemaFill/SchemaFill.pdf) | 主要问题是块内并行预测、半自回归依赖或并行草稿结构。 |
