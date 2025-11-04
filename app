from flask import Flask, render_template, jsonify
from tracker import Tracker
import threading

app = Flask(__name__)
tracker = Tracker('https://api.runonflux.io/apps/location/kaspanodekat', data_file='data/ip_history.csv')

def poller():
    import time
    while True:
        tracker.update_ips()
        time.sleep(3600)  # Poll every hour

threading.Thread(target=poller, daemon=True).start()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/history")
def history():
    return jsonify(tracker.get_history())

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
