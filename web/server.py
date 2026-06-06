"""
Off-Page SEO tool — local web server (standard library only).

Run:  python3 web/server.py
Then open http://localhost:8000

Live SEO data turns on automatically when DataForSEO credentials are present in
web/.env (see web/.env.example). Without them the app runs in demo mode so the
UI is fully usable immediately.
"""

import json
import os
import sys
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import seo_clients  # noqa: E402

seo_clients.load_env(os.path.join(HERE, ".env"))

PORT = int(os.environ.get("PORT", "8000"))


class Handler(BaseHTTPRequestHandler):
    def _send(self, code, body, ctype="application/json"):
        if isinstance(body, (dict, list)):
            body = json.dumps(body).encode()
        elif isinstance(body, str):
            body = body.encode()
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, *args):  # quieter console
        pass

    def do_GET(self):
        if self.path in ("/", "/index.html"):
            with open(os.path.join(HERE, "static", "index.html"), "rb") as f:
                return self._send(200, f.read(), "text/html; charset=utf-8")
        if self.path == "/api/status":
            return self._send(200, {
                "mode": "live" if seo_clients.have_dataforseo() else "demo",
                "provider": "DataForSEO" if seo_clients.have_dataforseo() else None,
            })
        return self._send(404, {"error": "not found"})

    def do_POST(self):
        if self.path != "/api/analyze":
            return self._send(404, {"error": "not found"})
        try:
            length = int(self.headers.get("Content-Length", 0))
            data = json.loads(self.rfile.read(length) or b"{}")
        except Exception as e:  # noqa: BLE001
            return self._send(400, {"error": f"bad request: {e}"})

        site = (data.get("site") or "").strip()
        if not site:
            return self._send(400, {"error": "site is required"})
        site = site.replace("https://", "").replace("http://", "").replace("www.", "").strip("/")
        location = (data.get("location") or "us").strip()
        tasks = data.get("tasks") or []
        if not tasks:
            return self._send(400, {"error": "select at least one off-page task"})
        try:
            da_floor = int(data.get("da_floor", 30))
            spam_ceiling = int(data.get("spam_ceiling", 2))
        except (TypeError, ValueError):
            da_floor, spam_ceiling = 30, 2

        try:
            result = seo_clients.analyze(site, location, tasks, da_floor, spam_ceiling)
        except Exception as e:  # noqa: BLE001
            return self._send(500, {"error": f"analysis failed: {e}"})
        return self._send(200, result)


def main():
    srv = ThreadingHTTPServer(("0.0.0.0", PORT), Handler)
    mode = "LIVE (DataForSEO)" if seo_clients.have_dataforseo() else "DEMO (no API keys)"
    print(f"Off-Page SEO tool running in {mode} mode")
    print(f"  ->  http://localhost:{PORT}")
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        srv.shutdown()


if __name__ == "__main__":
    main()
