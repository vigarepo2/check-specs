from flask import Flask
import psutil
import datetime

app = Flask(__name__)

def get_boot_time():
    boot_timestamp = psutil.boot_time()
    boot_time = datetime.datetime.fromtimestamp(boot_timestamp).strftime("%Y-%m-%d %H:%M:%S")
    return boot_time

def get_cpu_info():
    cpu_info = {
        "cores": psutil.cpu_count(logical=True),
        "usage": psutil.cpu_percent(interval=1)
    }
    return cpu_info

def get_memory_info():
    mem = psutil.virtual_memory()
    memory_info = {
        "total": mem.total / (1024 ** 3),  # Convert to GB
        "available": mem.available / (1024 ** 3),  # Convert to GB
        "used": mem.used / (1024 ** 3),  # Convert to GB
        "percentage": mem.percent
    }
    return memory_info

def get_disk_info():
    disk = psutil.disk_usage('/')
    disk_info = {
        "total": disk.total / (1024 ** 3),  # Convert to GB
        "used": disk.used / (1024 ** 3),  # Convert to GB
        "free": disk.free / (1024 ** 3),  # Convert to GB
        "percentage": disk.percent
    }
    return disk_info

def get_network_info():
    net_io = psutil.net_if_addrs()
    network_info = {
        "ip": net_io['eth0'][0].address,  # Adjust 'eth0' as needed
        "isp": "Your ISP Name"  # Replace with actual ISP lookup if needed
    }
    return network_info

@app.route('/')
def index():
    return "<h1>Hello, World!</h1>"

@app.route('/stats')
def stats():
    boot_time = get_boot_time()
    cpu_info = get_cpu_info()
    memory_info = get_memory_info()
    disk_info = get_disk_info()
    network_info = get_network_info()

    return f"""
    <html>
    <head>
        <title>Server Statistics Report</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                margin: 40px;
                padding: 20px;
                background-color: #f4f4f4;
            }}
            h1 {{
                text-align: center;
                color: #333;
            }}
            .stat {{
                margin-bottom: 20px;
            }}
            .stat h2 {{
                margin-bottom: 10px;
                color: #555;
            }}
            .stat p {{
                margin: 5px 0;
                color: #777;
            }}
        </style>
    </head>
    <body>
        <h1>Server Statistics Report</h1>
        <div class="stat">
            <h2>Boot Time</h2>
            <p>Boot Time: {boot_time}</p>
        </div>
        <div class="stat">
            <h2>CPU</h2>
            <p>Cores: {cpu_info['cores']}</p>
            <p>Usage: {cpu_info['usage']}%</p>
        </div>
        <div class="stat">
            <h2>Memory</h2>
            <p>Total: {memory_info['total']:.2f} GB</p>
            <p>Available: {memory_info['available']:.2f} GB</p>
            <p>Used: {memory_info['used']:.2f} GB</p>
            <p>Percentage: {memory_info['percentage']}%</p>
        </div>
        <div class="stat">
            <h2>Disk</h2>
            <p>Total: {disk_info['total']:.2f} GB</p>
            <p>Used: {disk_info['used']:.2f} GB</p>
            <p>Free: {disk_info['free']:.2f} GB</p>
            <p>Percentage: {disk_info['percentage']}%</p>
        </div>
        <div class="stat">
            <h2>Network</h2>
            <p>IP Address: {network_info['ip']}</p>
            <p>ISP: {network_info['isp']}</p>
        </div>
    </body>
    </html>
    """

if __name__ == '__main__':
    app.run(debug=True)
