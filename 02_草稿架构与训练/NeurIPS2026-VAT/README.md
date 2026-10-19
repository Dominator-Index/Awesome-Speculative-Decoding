# Verification-Aware Training for Speculative Decoding

- 目录：`NeurIPS2026-VAT`
- 分类：草稿架构与训练（推测解码方法、系统或分析）
- 发表依据：2026 主会官方 Poster 目录确认，[官方页面](https://neurips.cc/virtual/2026/poster/149396)
- 论文来源：[链接](https://neurips.cc/virtual/2026/poster/149396)
- 核查日期：2026-10-11

## 内容与定位

训练时模拟验证行为并调整监督权重，与 DLoop 的 loop-aware training 可对照。

与 DLoop 的已有关系记录：按模拟验证中各位置能否存活重加权监督；与 DLoop 的多轮输入分布训练关注点不同。

说明：这是依据官方摘要形成的阅读导航，尚未逐篇精读实验。不同论文可能保持目标采样分布、仅保持贪心输出、保持特定解码器行为，或允许质量权衡，不能统一称为无损。

## 本地 PDF

[阅读 PDF](VAT.pdf)，14 页，1,396,698 字节。`pdfinfo` 解析成功。

版本：公开预印本；会议信息另按官方目录核实。

[PDF 来源地址](https://arxiv.org/pdf/2608.30135)

下载成功时记录来源地址。

SHA-256：`cdb4549e959a9ffead0ffcb29167054ae2df42347e642b4beab149c6ea3ffd90`
