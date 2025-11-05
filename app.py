from flask import Flask, render_template, jsonify
from tracker import Tracker
import threading
import os
import time
import traceback

# === Environment configuration ===
API_URL = os.getenv("API_URL", "https://api.runonflux.io/apps/location/kaspanodekat")
APP_NAME = os.getenv("APP_NAME", "Kaspa")

app = Flask(__name__)
tracker = Tracker(API_URL)

# === Background poller (auto every 4 hours) ===
def poller():
    """Background poller that updates IPs every 4 hours."""
    while True:
        try:
            tracker.update_ips()
            print("[Poller] Automatic update complete.")
        except Exception as e:
            print(f"[Poller Error] {e}")
            traceback.print_exc()
        time.sleep(4 * 3600)  # every 4 hours


# Start the poller thread in background
threading.Thread(target=poller, daemon=True).start()


# === Flask Routes ===

@app.route("/")
def index():
    """Render dashboard with app name from environment."""
    return render_template("index.html", app_name=APP_NAME)


@app.route("/api/history")
def history():
    """Return IP change history (for chart + table)."""
    try:
        return jsonify(tracker.get_history())
    except Exception as e:
        print(f"[Error /api/history] {e}")
        traceback.print_exc()
        return jsonify([]), 500


@app.route("/api/stats")
def stats():
    """Return the current stats."""
    try:
        return jsonify(tracker.get_stats())
    except Exception as e:
        print(f"[Error /api/stats] {e}")
        traceback.print_exc()
        # Return fallback safe values so frontend doesn’t crash
        return jsonify({
            "last_poll": "Error",
            "new_ips": 0,
            "avg_per_day": 0,
            "total_ip_changes": 0,
            "total_api_calls": tracker.total_api_calls
        }), 500


@app.route("/api/fetch-now", methods=["POST"])
def fetch_now():
    """Manual API fetch — called from the dashboard button."""
    try:
        tracker.update_ips()
        stats = tracker.get_stats()
        return jsonify({
            "status": "success",
            "message": f"API called successfully ({API_URL})",
            "stats": stats
        })
    except Exception as e:
        print(f"[Error /api/fetch-now] {e}")
        traceback.print_exc()
        return jsonify({
            "status": "error",
            "message": "Backend error during fetch.",
            "error": str(e)
        }), 500


# === Start Flask server ===
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
