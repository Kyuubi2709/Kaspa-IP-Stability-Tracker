from flask import Flask, jsonify, render_template
from threading import Thread
import time
from tracker import IPTracker

app = Flask(__name__)
tracker = IPTracker()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/fetch-now", methods=["POST"])
def fetch_now():
    # Trigger an immediate API call
    tracker.update_ips()
    stats = tracker.get_stats()
    return jsonify({
        "status": "success",
        "message": "API called successfully",
        "stats": stats
    })

@app.route("/api/stats")
def get_stats():
    stats = tracker.get_stats()
    return jsonify(stats)

@app.route("/api/history")
def get_history():
    history = tracker.get_history()
    return jsonify(history)

def poller():
    """Background thread to fetch API data every hour"""
    while True:
        tracker.update_ips()
        time.sleep(3600)  # Every 1 hour

if __name__ == "__main__":
    # Start background polling thread
    Thread(target=poller, daemon=True).start()
    # Run Flask app
    app.run(host="0.0.0.0", port=5000)
