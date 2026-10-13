import os
import socket
from datetime import datetime, timezone

from flask import Flask, jsonify

app = Flask(__name__)

APP_VERSION = os.getenv("APP_VERSION", "dev")


@app.route("/")
def index():
    pod = socket.gethostname()
    return f"""<!doctype html>
<html><head><title>CI/CD Demo</title>
<style>
 body{{font-family:system-ui,sans-serif;background:#0f172a;color:#e2e8f0;
      display:grid;place-items:center;height:100vh;margin:0}}
 .card{{background:#1e293b;padding:2rem 3rem;border-radius:12px;text-align:center}}
 code{{background:#0f172a;padding:2px 8px;border-radius:6px;color:#38bdf8}}
</style></head>
<body><div class="card">
 <h1>🚀 Deployed by Jenkins</h1>
 <p>Version: <code>{APP_VERSION}</code></p>
 <p>Served by pod: <code>{pod}</code></p>
 <p>Jenkins &rarr; Docker &rarr; Registry &rarr; Kubernetes</p>
</div></body></html>"""


@app.route("/health")
def health():
    return jsonify(status="ok"), 200


@app.route("/version")
def version():
    return jsonify(
        version=APP_VERSION,
        pod=socket.gethostname(),
        time=datetime.now(timezone.utc).isoformat(),
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
