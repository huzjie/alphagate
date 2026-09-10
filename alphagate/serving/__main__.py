"""python -m alphagate.serving 启动服务。"""
import uvicorn

from alphagate.serving.app import create_app


def main() -> int:
    app = create_app()
    uvicorn.run(app, host="0.0.0.0", port=8000)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
