# 部署

## Docker

```bash
docker build -t alphagate:latest .
docker run -p 8000:8000 alphagate:latest
```

## Docker Compose

```bash
docker compose up -d
```

## Kubernetes

```bash
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml
```

## 环境变量

| 变量 | 说明 |
|---|---|
| `ALPHAGATE_DATA_SOURCE` | 数据源 mock/csv/akshare |
| `ALPHAGATE_GATE_SIMILARITY_THRESHOLD` | 门控阈值 |
