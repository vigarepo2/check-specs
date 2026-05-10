# check-specs

A professional Flask application for viewing server status from a clean web interface and JSON API.

## Features

- Modern landing page
- Server statistics dashboard
- System health endpoint
- JSON API for server metrics
- Hosting information page
- Safe error responses
- Configurable port and debug mode through environment variables

## Endpoints

| Endpoint | Type | Description |
| --- | --- | --- |
| `/` | Page | Main dashboard |
| `/health` | JSON | Service health status |
| `/stats` | Page | Server statistics dashboard |
| `/ip` | Page | Hosting information dashboard |
| `/api/stats` | JSON | CPU, memory, disk, boot time, and uptime data |
| `/api/ip` | JSON | Hosting information data |

## Stack

- Python
- Flask
- psutil
- requests
- gunicorn

## Install

```bash
pip install -r requirements.txt
```

## Run

```bash
python app.py
```

Default local URL:

```text
http://127.0.0.1:5000
```

## Environment

| Variable | Default | Description |
| --- | --- | --- |
| `PORT` | `5000` | App port |
| `FLASK_DEBUG` | `false` | Debug mode |

## Production

```bash
gunicorn app:app
```
