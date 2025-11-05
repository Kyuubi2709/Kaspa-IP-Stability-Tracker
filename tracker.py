import requests
from datetime import datetime, timedelta
from dateutil import parser


class Tracker:
    def __init__(self, api_url):
        self.api_url = api_url
        self.history = []        # Stores past change events
        self.last_ips = set()    # Store last known IP set
        self.last_poll_time = None
        self.total_changes = 0   # Cumulative IP changes since start
        self.total_api_calls = 0 # Count all API calls (auto + manual)

    def update_ips(self):
        """Fetch API data and track how many IPs changed since last call."""
        try:
            resp = requests.get(self.api_url)
            resp.raise_for_status()
            data = resp.json().get("data", [])
        except Exception as e:
            print(f"Error fetching API data: {e}")
            return

        # ✅ Increment API call counter
        self.total_api_calls += 1

        # Current IP set from API
        current_ips = {row.get("ip") for row in data if row.get("ip")}
        change_count = 0

        # ✅ Compare to previous call (smart replacement-based logic)
        if self.last_ips:
            added = current_ips - self.last_ips
            removed = self.last_ips - current_ips

            # Count replacements only (ignore temporary adds/removes)
            if added and removed:
                change_count = min(len(added), len(removed))
            else:
                change_count = 0
        else:
            # First call, no comparison
            change_count = 0

        # ✅ Add to total change counter
        self.total_changes += change_count

        # Record entry
        entry = {
            "timestamp": datetime.utcnow(),
            "change_count": change_count,
            "total_ips": len(current_ips)
        }
        self.history.append(entry)

        # Update tracker state
        self.last_ips = current_ips
        self.last_poll_time = entry["timestamp"]

        print(
            f"[Tracker] API fetched: {len(current_ips)} IPs, {change_count} true replacements since last call. "
            f"Total changes: {self.total_changes}, Total calls: {self.total_api_calls}"
        )

    def get_history(self):
        """Return data for chart and table (with serializable timestamps)."""
        return [
            {
                "timestamp": h["timestamp"].isoformat(),
                "change_count": h["change_count"],
                "total_ips": h["total_ips"]
            }
            for h in self.history
        ]

    def get_stats(self):
        """Return stats for dashboard."""
        if not self.history:
            return {
                "last_poll": "Never",
                "new_ips": 0,
                "avg_per_day": 0,
                "total_changes": 0,
                "total_api_calls": self.total_api_calls
            }

        new_ips = self.history[-1]["change_count"]

        twentyfour_hours_ago = datetime.utcnow() - timedelta(hours=24)
        recent_entries = [h for h in self.history if h["timestamp"] >= twentyfour_hours_ago]
        avg_day = (
            sum(h["change_count"] for h in recent_entries) / len(recent_entries)
            if recent_entries else 0
        )

        return {
            "last_poll": self.last_poll_time.strftime("%Y-%m-%d %H:%M:%S"),
            "new_ips": new_ips,
            "avg_per_day": round(avg_day, 2),
            "total_changes": self.total_changes,
            "total_api_calls": self.total_api_calls
        }
