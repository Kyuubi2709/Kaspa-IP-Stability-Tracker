# tracker.py
import requests
from datetime import datetime

class Tracker:
    def __init__(self, api_url):
        self.api_url = api_url
        self.history = []  # Store IP history in memory

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
        if new_entries:
            print(f"Added {len(new_entries)} new IP entries.")

    def get_history(self):
        """
        Return history in a format suitable for the frontend chart.
        You can customize this later to aggregate by IP, date, etc.
        """
        return self.history
