# REST API 参考

Base URL: `http://localhost:8000`

| 方法 | 路径 | 说明 |
|---|---|---|
| GET | `/health` | 健康检查 |
| POST | `/gate` | 语义门控配置决策 |
| POST | `/regime` | 市场状态建模 |
| POST | `/backtest` | 回测 |
| POST | `/v1/chat/completions` | OpenAI 兼容端点 |

## POST /gate

```json
{
  "symbols": ["600000.SH", "000001.SZ"],
  "indicators": null,
  "news": null
}
```

返回：

```json
{
  "regime": "bull",
  "ideas": [
    {"name": "动量", "allowed": true, "score": 0.62, "weight": 0.34, "reason": "..."}
  ],
  "weights": {"动量": 0.34, "质量": 0.28},
  "rationale": "..."
}
```

## 交互文档

启动服务后访问 `http://localhost:8000/docs` 查看 Swagger UI。
