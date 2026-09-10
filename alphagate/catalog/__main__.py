"""python -m alphagate.catalog 列出所有模型/策略卡。"""
from alphagate.catalog import list_models, list_strategies


def main() -> int:
    print("模型卡：", list_models())
    print("策略卡：", list_strategies())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
