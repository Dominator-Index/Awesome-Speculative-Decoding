# DLite: History-Free Speculative Decoding for Agentic AI

## 1. 来源与状态

- OpenReview ID：`UwMYxYHQSG`，投稿编号：5178。
- [投稿页面](https://openreview.net/forum?id=UwMYxYHQSG)；ICLR 2027 投稿快照记录；非录用，当前状态未由官方 API 实时复核。
- 发现依据：[公开元数据镜像](https://github.com/yzc-666/iclr2027-explorer)，2026-10-07 快照；当前官方 API 返回 HTTP 403。
- 快照状态：`active`；它不表示今天的实时状态。
- [作者预印本](https://arxiv.org/abs/2610.23787)；arXiv 与投稿版本可能不同。

## 2. 分类与定位

主分类：**并行与半自回归草稿**。

复用目标上下文隐藏状态，以无历史并行骨干和轻量顺序头起草，减少 Agent 多轮长上下文中的草稿历史 KV 开销；不是工具动作级推测。

分类依据：主要问题是块内并行预测、半自回归依赖或并行草稿结构。

交叉主题：history-free, 长上下文, 草稿历史 KV, Agentic。这是题名与摘要的初筛分类，尚未逐篇重新精读全文；目录采用主要贡献，其余主题交叉标记。描述性目录简称不一定是作者给定的方法缩写。

## 3. 本地文件与证据边界

[阅读 PDF](DLite.pdf)，14 页。文件头、`pdfinfo` 与 SHA-256 已核查。标题核对采用元数据匹配与首页词项覆盖检查，不表示独立复现全部论文实验。

SHA-256：`0c0906929baf8182f11692ebe8a3916c95df8a9fff9d49c56e2864ea8ef244f8`。

[文件下载来源](https://arxiv.org/pdf/2610.23787)。

输出保证：尚未逐篇独立核查；须区别目标采样分布、贪心输出一致、语义质量及工具轨迹保证。

## 4. 进一步阅读

[定位与阅读笔记](定位与阅读笔记.md)：token 级与动作级区别、历史 KV、训练方式，以及 Agentic 评测的时间口径。
