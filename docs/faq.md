# 常见问题

**Q: 需要 GPU 吗？**
不需要。mock 数据源 + hash 嵌入完全离线可跑。

**Q: 如何接入真实 A 股数据？**
`pip install akshare`，config 里 `data.source=akshare`。或 `tushare`/`wind`/`yfinance`。

**Q: 语义门控阈值怎么调？**
阈值越低放行越多（组合越分散）。默认 0.20，建议 0.15~0.35。

**Q: 可以接真实 LLM 做推理吗？**
`serving` 提供 OpenAI 兼容端点，`model.backend=openai` 可接外部模型。

**Q: 训练是做什么？**
两阶段：Stage1 把「状态→思路」规则对齐，Stage2 GRPO 优化门控阈值。
