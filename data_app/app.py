from flask import Flask, jsonify, request
import datetime
import os

app = Flask(__name__)

# Define the path where the volume will be mounted inside the container
# Docker will automatically create this directory if it doesn't exist
DATA_DIR = "/app/data"
LOG_FILE = os.path.join(DATA_DIR, "log.txt")

# Ensure the data directory exists when the app starts
# This is crucial for the app to be able to write to it
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

@app.route('/')
def hello_data_app():
    return "Hello from Data App! Use /write to log data or /read to view logs."

@app.route('/write')
def write_log():
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    message = f"[{timestamp}] Data written successfully!\n"
    try:
        with open(LOG_FILE, 'a') as f: # 'a' for append mode
            f.write(message)
        return jsonify({"status": "success", "message": "Log entry added.", "log_entry": message.strip()})
    except Exception as e:
        return jsonify({"status": "error", "message": f"Failed to write log: {e}"}), 500

@app.route('/read')
def read_log():
    try:
        if not os.path.exists(LOG_FILE):
            return jsonify({"status": "info", "message": "Log file does not exist yet."})
        with open(LOG_FILE, 'r') as f:
            content = f.read()
        return jsonify({"status": "success", "log_content": content})
    except Exception as e:
        return jsonify({"status": "error", "message": f"Failed to read log: {e}"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)