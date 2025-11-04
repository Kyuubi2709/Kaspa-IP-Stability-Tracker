import requests
from datetime import datetime, timedelta

class Tracker:
    def __init__(self, api_url):
        self.api_url = api_url
        self.history = []  # Store IP history in memory
        self.last_poll_time = None
        self.prev_poll_time = None  # New: track previous poll time

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

        # Move previous poll time tracking before we update
        self.prev_poll_time = self.last_poll_time
        self.last_poll_time = datetime.utcnow()

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

        if new_entries:
            print(f"Added {len(new_entries)} new IP entries.")
            self.history.extend(new_entries)
        else:
            print("No new IP entries found.")

    def get_history(self):
        """Return raw history for charting if needed."""
        return self.history

    def get_stats(self):
        """Return stats for dashboard."""
        if not self.history:
            return {
                "last_poll": "Never",
                "new_ips": 0,
                "avg_per_4h": 0
            }

        # Calculate new IPs since last call (between prev_poll_time and last_poll_time)
        new_ips = 0
        if self.prev_poll_time and self.last_poll_time:
            new_ips = len([
                h for h in self.history
                if self.prev_poll_time <= datetime.strptime(h['broadcastedAt'], "%Y-%m-%dT%H:%M:%SZ") <= self.last_poll_time
            ])

        # Average IP changes per 4h (optional smoothing)
        times = [datetime.strptime(h['broadcastedAt'], "%Y-%m-%dT%H:%M:%SZ") for h in self.history]
        times.sort()

        changes_per_4h = []
        if times:
            start = times[0]
            end = times[-1]
            current = start
            while current < end:
                next_window = current + timedelta(hours=4)
                changes = len([t for t in times if current <= t < next_window])
                changes_per_4h.append(changes)
                current = next_window

        avg_4h = sum(changes_per_4h) / len(changes_per_4h) if changes_per_4h else 0

        return {
            "last_poll": self.last_poll_time.strftime("%Y-%m-%d %H:%M:%S") if self.last_poll_time else "Never",
            "new_ips": new_ips,
            "avg_per_4h": round(avg_4h, 2)
        }
