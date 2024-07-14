from flask import Flask
import psutil
import datetime
import speedtest

app = Flask(__name__)

def get_boot_time():
    boot_timestamp = psutil.boot_time()
    boot_time = datetime.datetime.fromtimestamp(boot_timestamp).strftime("%Y-%m-%d %H:%M:%S")
    return boot_time

def get_cpu_info():
    cpu_info = {
        "cores": psutil.cpu_count(logical=True),
        "frequency": psutil.cpu_freq().current,
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

def get_swap_info():
    swap = psutil.swap_memory()
    swap_info = {
        "total": swap.total / (1024 ** 3),  # Convert to GB
        "used": swap.used / (1024 ** 3),  # Convert to GB
        "free": swap.free / (1024 ** 3),  # Convert to GB
        "percentage": swap.percent
    }
    return swap_info

def get_disk_info():
    disk = psutil.disk_usage('/')
    disk_info = {
        "total": disk.total / (1024 ** 3),  # Convert to GB
        "used": disk.used / (1024 ** 3),  # Convert to GB
        "free": disk.free / (1024 ** 3),  # Convert to GB
        "percentage": disk.percent
    }
    return disk_info

def get_network_io():
    net_io = psutil.net_io_counters()
    network_io = {
        "bytes_sent": net_io.bytes_sent / (1024 ** 2),  # Convert to MB
        "bytes_received": net_io.bytes_recv / (1024 ** 2)  # Convert to MB
