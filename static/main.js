async function fetchStats() {
    const res = await fetch('/api/stats');
    const data = await res.json();
    document.getElementById('last-poll').textContent = data.last_poll;
    document.getElementById('new-ips').textContent = data.new_ips;
    document.getElementById('avg-4h').textContent = data.avg_per_4h;
}

// Optional: chart historical IP changes
async function fetchHistory(){
    const res = await fetch('/api/history');
    const data = await res.json();
    const labels = data.map((x,i) => i+1); // index for x-axis
    const changes = data.map(x => 1);      // each entry = 1 change
    const ctx = document.getElementById('chart').getContext('2d');
    new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [{label: 'IP Changes Over Time', data: changes, borderColor: 'blue', fill: false}]
        }
    });
}

// Manual Fetch button
document.getElementById('fetch-now-btn').addEventListener('click', async () => {
    const statusEl = document.getElementById('fetch-status');
    statusEl.textContent = "Fetching...";
    
    try {
        const res = await fetch('/api/fetch-now', { method: 'POST' });
        const data = await res.json();
        statusEl.textContent = data.message;
        fetchStats();   // Refresh dashboard
        fetchHistory(); // Refresh chart
    } catch (err) {
        statusEl.textContent = "Error calling API";
        console.error(err);
    }
});

// Initial load
fetchStats();
fetchHistory();
setInterval(fetchStats, 60 * 1000); // update stats every 1 min
