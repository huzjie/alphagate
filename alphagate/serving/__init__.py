"""推理服务层：FastAPI REST + OpenAI 兼容端点。"""
from alphagate.serving.app import create_app

__all__ = ["create_app"]
