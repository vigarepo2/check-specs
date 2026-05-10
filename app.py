import datetime as dt
import os
from typing import Any

import psutil
import requests
from flask import Flask, jsonify, render_template_string
from requests import RequestException

app = Flask(__name__)
app.config["JSON_SORT_KEYS"] = False

IP_LOOKUP_URL = "https://api.my-ip.io/v2/ip.json"
REQUEST_TIMEOUT = 5
BYTES_IN_GIB = 1024 ** 3

PAGE_TEMPLATE = """
<!doctype html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>{{ title }}</title>
    <style>
        :root {
            color-scheme: dark;
            font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
            background: #09090b;
            color: #f8fafc;
        }
        * { box-sizing: border-box; }
        body {
            margin: 0;
            min-height: 100vh;
            background: radial-gradient(circle at top left, #1e293b 0, transparent 32rem), #09090b;
        }
        main {
            width: min(1100px, calc(100% - 32px));
            margin: 0 auto;
            padding: 56px 0;
        }
        .hero {
            display: grid;
            gap: 16px;
            margin-bottom: 28px;
        }
        .eyebrow {
            color: #38bdf8;
            font-size: 13px;
            font-weight: 700;
            letter-spacing: .14em;
            text-transform: uppercase;
        }
        h1 {
            margin: 0;
            font-size: clamp(32px, 6vw, 64px);
            line-height: .95;
            letter-spacing: -.05em;
        }
        p {
            margin: 0;
            color: #cbd5e1;
            font-size: 17px;
            line-height: 1.7;
        }
        .grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
            gap: 16px;
        }
        .card {
            border: 1px solid rgba(148, 163, 184, .18);
            border-radius: 24px;
            padding: 22px;
            background: rgba(15, 23, 42, .72);
            box-shadow: 0 24px 80px rgba(0, 0, 0, .28);
            backdrop-filter: blur(16px);
        }
        .label {
            color: #94a3b8;
            font-size: 13px;
            font-weight: 700;
            letter-spacing: .08em;
            text-transform: uppercase;
        }
        .value {
            margin-top: 10px;
            color: #f8fafc;
            font-size: 28px;
            font-weight: 800;
            word-break: break-word;
        }
        .muted {
            margin-top: 6px;
            color: #94a3b8;
            font-size: 14px;
        }
        .actions {
            display: flex;
            flex-wrap: wrap;
            gap: 12px;
            margin-top: 24px;
        }
        a {
            color: #0f172a;
            border-radius: 999px;
            background: #f8fafc;
            padding: 10px 15px;
            font-size: 14px;
            font-weight: 800;
            text-decoration: none;
        }
        a.secondary {
            color: #f8fafc;
            border: 1px solid rgba(148, 163, 184, .25);
            background: rgba(15, 23, 42, .7);
        }
    </style>
</head>
<body>
    <main>
        <section class="hero">
            <div class="eyebrow">{{ eyebrow }}</div>
            <h1>{{ heading }}</h1>
            <p>{{ description }}</p>
        </section>
        <section class="grid">
            {% for item in items %}
            <article class="card">
                <div class="label">{{ item.label }}</div>
                <div class="value">{{ item.value }}</div>
                {% if item.meta %}<div class="muted">{{ item.meta }}</div>{% endif %}
            </article>
            {% endfor %}
        </section>
        <nav class="actions">
            <a href="/stats">Stats</a>
            <a href="/ip" class="secondary">IP Info</a>
            <a href="/api/stats" class="secondary">Stats API</a>
            <a href="/api/ip" class="secondary">IP API</a>
        </nav>
    </main>
</body>
</html>
"""


def gib(value: int) -> float:
    return round(value / BYTES_IN_GIB, 2)


def now_utc() -> str:
    return dt.datetime.now(dt.UTC).isoformat()


def boot_time() -> str:
    return dt.datetime.fromtimestamp(psutil.boot_time(), dt.UTC).isoformat()


def uptime_seconds() -> int:
    return int(dt.datetime.now(dt.UTC).timestamp() - psutil.boot_time())


def percentage(value: float) -> str:
    return f"{value:.1f}%"


def system_stats() -> dict[str, Any]:
    memory = psutil.virtual_memory()
    disk = psutil.disk_usage("/")
    cpu_frequency = psutil.cpu_freq()

    return {
        "status": "ok",
        "generated_at": now_utc(),
        "boot_time": boot_time(),
        "uptime_seconds": uptime_seconds(),
        "cpu": {
            "physical_cores": psutil.cpu_count(logical=False) or 0,
            "logical_cores": psutil.cpu_count(logical=True) or 0,
            "usage_percent": psutil.cpu_percent(interval=0.25),
            "frequency_mhz": round(cpu_frequency.current, 2) if cpu_frequency else None,
        },
        "memory": {
            "total_gb": gib(memory.total),
            "available_gb": gib(memory.available),
            "used_gb": gib(memory.used),
            "usage_percent": memory.percent,
        },
        "disk": {
            "total_gb": gib(disk.total),
            "used_gb": gib(disk.used),
            "free_gb": gib(disk.free),
            "usage_percent": disk.percent,
        },
    }


def host_info() -> dict[str, Any]:
    try:
        response = requests.get(IP_LOOKUP_URL, timeout=REQUEST_TIMEOUT)
        response.raise_for_status()
        data = response.json()
    except (RequestException, ValueError):
        return {"status": "error", "message": "Unable to fetch hosting information"}

    if not data.get("success"):
        return {"status": "error", "message": "IP lookup service returned an unsuccessful response"}

    asn = data.get("asn") or {}
    country = data.get("country") or {}
    location = data.get("location") or {}

    return {
        "status": "ok",
        "generated_at": now_utc(),
        "ip": data.get("ip"),
        "isp": asn.get("name"),
        "country": country.get("name"),
        "latitude": location.get("lat"),
        "longitude": location.get("lon"),
    }


def stats_cards(data: dict[str, Any]) -> list[dict[str, str]]:
    return [
        {"label": "Boot Time", "value": data["boot_time"], "meta": f"Uptime: {data['uptime_seconds']} seconds"},
        {"label": "CPU Usage", "value": percentage(data["cpu"]["usage_percent"]), "meta": f"{data['cpu']['logical_cores']} logical cores"},
        {"label": "Memory Used", "value": f"{data['memory']['used_gb']} GB", "meta": f"{percentage(data['memory']['usage_percent'])} of {data['memory']['total_gb']} GB"},
        {"label": "Disk Used", "value": f"{data['disk']['used_gb']} GB", "meta": f"{percentage(data['disk']['usage_percent'])} of {data['disk']['total_gb']} GB"},
    ]


def ip_cards(data: dict[str, Any]) -> list[dict[str, Any]]:
    if data.get("status") != "ok":
        return [{"label": "Status", "value": "Unavailable", "meta": data.get("message", "Unknown error")}]

    return [
        {"label": "IP Address", "value": data.get("ip") or "Unknown", "meta": None},
        {"label": "ISP", "value": data.get("isp") or "Unknown", "meta": None},
        {"label": "Country", "value": data.get("country") or "Unknown", "meta": None},
        {"label": "Coordinates", "value": f"{data.get('latitude')}, {data.get('longitude')}", "meta": None},
    ]


@app.get("/")
def index():
    return render_template_string(
        PAGE_TEMPLATE,
        title="Check Specs",
        eyebrow="Server Monitor",
        heading="Clean server insights in one Flask app.",
        description="View system health, resource usage, and hosting information through simple web pages and JSON endpoints.",
        items=[
            {"label": "Stats Page", "value": "/stats", "meta": "CPU, memory, disk, and uptime"},
            {"label": "IP Page", "value": "/ip", "meta": "Public IP, ISP, country, and coordinates"},
            {"label": "Health Check", "value": "/health", "meta": "Lightweight service status endpoint"},
        ],
    )


@app.get("/health")
def health():
    return jsonify({"status": "ok", "service": "check-specs", "timestamp": now_utc()})


@app.get("/stats")
def stats_page():
    data = system_stats()
    return render_template_string(
        PAGE_TEMPLATE,
        title="Server Statistics",
        eyebrow="Live System Report",
        heading="Server statistics dashboard.",
        description="A real-time overview of CPU, memory, disk, boot time, and uptime.",
        items=stats_cards(data),
    )


@app.get("/ip")
def ip_page():
    data = host_info()
    return render_template_string(
        PAGE_TEMPLATE,
        title="Hosting Information",
        eyebrow="Network Report",
        heading="Public hosting information.",
        description="Public IP and ISP metadata resolved from the current server network.",
        items=ip_cards(data),
    )


@app.get("/api/stats")
def stats_api():
    return jsonify(system_stats())


@app.get("/api/ip")
def ip_api():
    data = host_info()
    status_code = 200 if data.get("status") == "ok" else 502
    return jsonify(data), status_code


@app.errorhandler(404)
def not_found(error):
    return jsonify({"status": "error", "message": "Endpoint not found"}), 404


@app.errorhandler(500)
def server_error(error):
    return jsonify({"status": "error", "message": "Internal server error"}), 500


if __name__ == "__main__":
    port = int(os.getenv("PORT", "5000"))
    debug = os.getenv("FLASK_DEBUG", "false").lower() == "true"
    app.run(host="0.0.0.0", port=port, debug=debug)
