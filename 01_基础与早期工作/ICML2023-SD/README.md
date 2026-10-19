# Fast Inference from Transformers via Speculative Decoding

- 分类：基础
- 目录：`ICML2023-SD`
- 发表状态：会议或期刊；见发表依据
- 来源：[原始来源](https://proceedings.mlr.press/v202/leviathan23a/leviathan23a.pdf)
- 发表依据：[链接](https://proceedings.mlr.press/v202/leviathan23a.html)
- PDF 下载来源：https://proceedings.mlr.press/v202/leviathan23a/leviathan23a.pdf
- 下载状态：downloaded

## 与 DLoop 的关系

独立小模型起草，大模型并行验证；DLoop 保留原有接受规则，改变验证前的起草轮数。

说明：这段关系整理主要依据用户提供的 DLoop 第 2 节（PDF 第 2–3 页）、参考文献及相关正文；不表示已独立复核本论文全部实验。

## 本地文件

[阅读 PDF](SD.pdf)，13 页，479,566 字节。首页标题已核对，`pdfinfo` 解析成功。

SHA-256：`b287adca11d8126e86dfd6facf162f74f2f6dcfefdef9130af7dde35b08e1d1d`

## 中文学习材料

- [论文与核心代码讲解](论文与核心代码讲解.md)：接受机制、数学证明、性能公式与第三方 PyTorch 源码对照。
- [无需模型的教学脚本](sampling_demo.py)：可运行的概率机制与联合分布检查。
- [已克隆的第三方代码](code/Speculative-Decoding)，来源与 commit 见 [provenance.json](code/provenance.json)。
