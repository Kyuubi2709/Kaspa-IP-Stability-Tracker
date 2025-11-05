import requests
from datetime import datetime, timedelta
from dateutil import parser


class Tracker:
    def __init__(self, api_url):
        self.api_url = api_url
        self.history = []      # Stores past change events
        self.last_ips = set()  # Store last known IP set
        self.last_poll_time = None
        self.total_api_calls = 0  # ✅ Track number of API calls since start

    def update_ips(self):
        """Fetch API data and track how many IPs changed since last call."""
        try:
            resp = requests.get(self.api_url)
            resp.raise_for_status()
            data = resp.json().get("data", [])
        except Exception as e:
            print(f"Error fetching API data: {e}")
            return

        # Count this API call
        self.total_api_calls += 1

        # Current IP set from API
        current_ips = {row.get("ip") for row in data if row.get("ip")}
        change_count = 0

        # Compare to previous call
        if self.last_ips:
            changed_ips = current_ips.symmetric_difference(self.last_ips)
            change_count = len(changed_ips)
        else:
            # First call, no comparison
            change_count = 0

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

        print(f"[Tracker] API fetched: {len(current_ips)} IPs, {change_count} changes since last call. "
              f"Total calls: {self.total_api_calls}")

    def get_history(self):
        """Return data for chart."""
        return self.history

    def get_stats(self):
        """Return stats for dashboard."""
        if not self.history:
            return {
                "last_poll": "Never",
                "new_ips": 0,
                "avg_per_day": 0,
                "total_api_calls": self.total_api_calls,
                "total_ip_changes": 0
            }

        # Most recent change count
        new_ips = self.history[-1]["change_count"]

        # Total IP changes overall
        total_ip_changes = sum(h["change_count"] for h in self.history)

        # Average per 24 hours
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
            "total_api_calls": self.total_api_calls,
            "total_ip_changes": total_ip_changes
        }
