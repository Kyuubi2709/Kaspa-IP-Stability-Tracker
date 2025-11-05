from flask import Flask, render_template, jsonify
from tracker import Tracker
import threading
import os
import time

# ✅ Read from environment variables
API_URL = os.getenv("API_URL", "https://api.runonflux.io/apps/location/kaspanodekat")
APP_NAME = os.getenv("APP_NAME", "Kaspa")  # ✅ new configurable app name

app = Flask(__name__)
tracker = Tracker(API_URL)


def poller():
    """Background poller that updates every 4 hours."""
    while True:
        tracker.update_ips()
        time.sleep(4 * 3600)  # every 4 hours


# Start background thread
threading.Thread(target=poller, daemon=True).start()


@app.route("/")
def index():
    # Pass APP_NAME to the HTML template
    return render_template("index.html", app_name=APP_NAME)


@app.route("/api/history")
def history():
    return jsonify(tracker.get_history())


@app.route("/api/stats")
def stats():
    return jsonify(tracker.get_stats())


@app.route("/api/fetch-now", methods=["POST"])
def fetch_now():
    """Manual fetch — updates and returns new stats immediately."""
    tracker.update_ips()
    stats = tracker.get_stats()
    return jsonify({
        "status": "success",
        "message": f"API called successfully ({API_URL})",
        "stats": stats
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
