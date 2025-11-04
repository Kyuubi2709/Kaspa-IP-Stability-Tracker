from flask import Flask, jsonify, render_template
from threading import Thread
import time
from tracker import Tracker  # ✅ fixed import

# Initialize Flask and Tracker
app = Flask(__name__)
tracker = Tracker(api_url="https://api.kaspa.org/peers")  # 👈 change this URL if your API differs

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/fetch-now", methods=["POST"])
def fetch_now():
    """Manual API trigger — updates data and returns stats immediately"""
    tracker.update_ips()
    stats = tracker.get_stats()
    return jsonify({
        "status": "success",
        "message": "API called successfully",
        "stats": stats
    })

@app.route("/api/stats")
def get_stats():
    """Return latest stats for dashboard"""
    stats = tracker.get_stats()
    return jsonify(stats)

@app.route("/api/history")
def get_history():
    """Return IP history data"""
    history = tracker.get_history()
    return jsonify(history)

def poller():
    """Background thread: automatically call API every 1 hour"""
    while True:
        tracker.update_ips()
        time.sleep(3600)  # every hour

if __name__ == "__main__":
    # Start background job
    Thread(target=poller, daemon=True).start()
    # Run Flask app
    app.run(host="0.0.0.0", port=5000)
