# H-Spec: Parallel Speculative Decoding Without a Drafter-Side KV Cache

## 1. 来源与状态

- OpenReview ID：`85djEhybB3`，投稿编号：8158。
- [投稿页面](https://openreview.net/forum?id=85djEhybB3)；ICLR 2027 投稿快照记录；非录用，当前状态未由官方 API 实时复核。
- 发现依据：[公开元数据镜像](https://github.com/yzc-666/iclr2027-explorer)，2026-10-07 快照；当前官方 API 返回 HTTP 403。
- 快照状态：`active`；它不表示今天的实时状态。
- [作者预印本](https://arxiv.org/abs/2609.24197)；arXiv 与投稿版本可能不同。

## 2. 分类与定位

主分类：**长上下文与近似计算**。

研究不维护草稿端历史 KV 的并行推测起草，与 DLite 的历史依赖问题可以对照。

分类依据：主要问题是长上下文、KV 历史、缓存恢复或近似计算。

交叉主题：未单独标注。这是题名与摘要的初筛分类，尚未逐篇重新精读全文；目录采用主要贡献，其余主题交叉标记。描述性目录简称不一定是作者给定的方法缩写。

## 3. 本地文件与证据边界

[阅读 PDF](H-Spec.pdf)，22 页。文件头、`pdfinfo` 与 SHA-256 已核查。标题核对采用元数据匹配与首页词项覆盖检查，不表示独立复现全部论文实验。

SHA-256：`bde0727044cb594d0e80a2b5d1ac4dbc37b894da3c33cbdd5832b0beea98654d`。

[文件下载来源](https://arxiv.org/pdf/2609.24197)。

输出保证：尚未逐篇独立核查；须区别目标采样分布、贪心输出一致、语义质量及工具轨迹保证。
