# tracker.py
import requests
from datetime import datetime, timedelta

class Tracker:
    def __init__(self, api_url):
        self.api_url = api_url
        self.history = []  # Store IP history in memory
        self.last_poll_time = None

    def update_ips(self):
        """
        Fetch latest IP data from API and append to history.
        Avoid duplicates for the same IP at the same timestamp.
        """
        try:
            resp = requests.get(self.api_url)
            resp.raise_for_status()
            data = resp.json().get("data", [])
        except Exception as e:
            print(f"Error fetching API data: {e}")
            return

        new_entries = []
        for row in data:
            entry = {
                "ip": row.get("ip"),
                "name": row.get("name"),
                "broadcastedAt": row.get("broadcastedAt")
            }

            # Only add if this broadcastedAt for this IP doesn't exist yet
            if not any(h['ip'] == entry['ip'] and h['broadcastedAt'] == entry['broadcastedAt'] for h in self.history):
                new_entries.append(entry)

        self.history.extend(new_entries)
        self.last_poll_time = datetime.utcnow()
        if new_entries:
            print(f"Added {len(new_entries)} new IP entries.")

    def get_history(self):
        """Return raw history for charting if needed."""
        return self.history

    def get_stats(self):
        """Return stats for dashboard."""
        if not self.history:
            return {
                "last_poll": None,
                "new_ips": 0,
                "avg_per_4h": 0
            }

        # Calculate IP changes since last poll
        new_ips = 0
        if self.last_poll_time:
            new_ips = len([h for h in self.history 
                           if datetime.strptime(h['broadcastedAt'], "%Y-%m-%dT%H:%M:%SZ") >= self.last_poll_time - timedelta(hours=1)])

        # Average IP changes per 4h
        changes_per_4h = []
        now = datetime.utcnow()
        for i in range(0, len(self.history), 4):
            changes_per_4h.append(len(self.history[i:i+4]))
        avg_4h = sum(changes_per_4h)/len(changes_per_4h) if changes_per_4h else 0

        return {
            "last_poll": self.last_poll_time.strftime("%Y-%m-%d %H:%M:%S") if self.last_poll_time else "Never",
            "new_ips": new_ips,
            "avg_per_4h": round(avg_4h, 2)
        }
