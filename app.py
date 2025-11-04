from flask import Flask, render_template, jsonify
from tracker import Tracker
import threading

app = Flask(__name__)
tracker = Tracker('https://api.runonflux.io/apps/location/kaspanodekat')


def poller():
    import time
    while True:
        tracker.update_ips()
        time.sleep(3600)  # Poll every hour


# Start background polling thread
threading.Thread(target=poller, daemon=True).start()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/history")
def history():
    return jsonify(tracker.get_history())


@app.route("/api/stats")
def stats():
    return jsonify(tracker.get_stats())


@app.route("/api/fetch-now", methods=["POST"])
def fetch_now():
    """Manual API trigger — updates data and returns stats immediately"""
    tracker.update_ips()
    stats = tracker.get_stats()  # ✅ get updated stats
    return jsonify({
        "status": "success",
        "message": "API called successfully",
        "stats": stats  # ✅ send updated stats
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
