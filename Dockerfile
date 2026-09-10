# AlphaGate 多阶段构建
FROM python:3.11-slim AS builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

FROM python:3.11-slim
WORKDIR /app
ENV PYTHONUNBUFFERED=1
COPY --from=builder /install /usr/local
COPY . .
RUN pip install --no-cache-dir -e .
EXPOSE 8000
ENTRYPOINT ["alphagate"]
CMD ["serve", "--host", "0.0.0.0", "--port", "8000"]
