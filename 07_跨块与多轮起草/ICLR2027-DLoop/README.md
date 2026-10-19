# DLoop: Looped Speculative Decoding

用户提供的论文：[原始 PDF](3897_DLoop_Looped_Speculative_.pdf)。首页标注 ICLR 2027 在审，尚不能视为已录用。

论文将多轮完整起草合并到一次目标模型验证之前，通过草稿自身置信度决定是否继续，并用 loop-aware training 处理未验证 token 缺少目标隐藏状态的问题。原有接受规则保持不变。

Related Work 位于 PDF 第 2–3 页，参考文献位于第 10–13 页。[完整整理与本地论文索引](../../README.md)。

阅读时重点比较 EAGLE-3 的 training-time test、PACER 的块级预验证、SpecBlock 的跨块起草，以及 DFlash、Domino、DSpark 的块内生成方式。
