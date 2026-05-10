# check-specs

A lightweight Flask app for checking basic server and hosting information from a web browser.

## Features

- `/` shows a simple Hello World page.
- `/stats` displays server statistics, including boot time, CPU cores, CPU usage, memory usage, and disk usage.
- `/ip` displays hosting information, including public IP address, ISP, country, latitude, and longitude.

## Tech Stack

- Python
- Flask
- psutil
- requests
- gunicorn

## Installation

```bash
pip install -r requirements.txt
```

## Run Locally

```bash
python app.py
```

By default, Flask runs the app at:

```text
http://127.0.0.1:5000
```

## Endpoints

| Endpoint | Description |
| --- | --- |
| `/` | Basic homepage |
| `/stats` | Server statistics report |
| `/ip` | Public IP and hosting information |

## Notes

The `/ip` endpoint uses an external IP lookup API, so it requires internet access from the server.
