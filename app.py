# app.py

from flask import Flask
import psutil

app = Flask(__name__)

@app.route('/')
def index():
    # Get system memory (RAM) usage
    mem = psutil.virtual_memory()
    total_memory = mem.total // (1024 * 1024)  # Convert to MB
    available_memory = mem.available // (1024 * 1024)  # Convert to MB

    # Get disk usage
    disk = psutil.disk_usage('/')
    total_disk = disk.total // (2**30)  # Convert to GB
    free_disk = disk.free // (2**30)  # Convert to GB

    return """
    <h1>Server Resource Information</h1>
    <h2>Memory:</h2>
    <p>Total Memory: {} MB</p>
    <p>Available Memory: {} MB</p>

    <h2>Disk:</h2>
    <p>Total Disk Space: {} GB</p>
    <p>Free Disk Space: {} GB</p>
    """.format(total_memory, available_memory, total_disk, free_disk)

if __name__ == '__main__':
    app.run(debug=True)
