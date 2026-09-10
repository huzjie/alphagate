"""示例：调用 REST 服务（先 `alphagate serve`）。"""
import json
import urllib.request

req = urllib.request.Request(
    "http://localhost:8000/gate",
    data=json.dumps({"symbols": ["600000.SH", "000001.SZ"]}).encode(),
    headers={"Content-Type": "application/json"},
)
with urllib.request.urlopen(req, timeout=30) as resp:
    print(json.dumps(json.loads(resp.read()), ensure_ascii=False, indent=2))
