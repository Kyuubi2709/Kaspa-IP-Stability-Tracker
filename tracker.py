import requests
import csv
import os
from datetime import datetime

class Tracker:
    def __init__(self, api_url, data_file='ip_history.csv'):
        self.api_url = api_url
        self.data_file = data_file
        self.history = []
        os.makedirs(os.path.dirname(data_file), exist_ok=True) if os.path.dirname(data_file) else None
        if os.path.exists(data_file):
            with open(data_file, newline='') as f:
                reader = csv.DictReader(f)
                self.history = list(reader)

    def fetch_ips(self):
        try:
            r = requests.get(self.api_url, timeout=10)
            r.raise_for_status()
            data = r.json()
            return [(item['name'], item['runningSince'], item['osUptime'], item['ip']) for item in data['data']]
        except Exception as e:
            print("Error fetching IPs:", e)
            return []

    def update_ips(self):
        new_ips = self.fetch_ips()
        if not new_ips:
            return
        prev_ips = {row['key']: row['ip'] for row in self.history[-1:]} if self.history else {}
        current_row = {'timestamp': datetime.utcnow().isoformat(), 'changes': 0}
        for item in new_ips:
            key = f"{item[0]}|{item[1]}|{item[2]}"
            if key in prev_ips:
                if prev_ips[key] != item[3]:
                    current_row['changes'] += 1
            else:
                current_row['changes'] += 1
        current_row['ip_list'] = ";".join([x[3] for x in new_ips])
        self.history.append(current_row)
        self.save()

    def save(self):
        fieldnames = ['timestamp', 'changes', 'ip_list']
        with open(self.data_file, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for row in self.history:
                writer.writerow(row)

    def get_history(self):
        return self.history
