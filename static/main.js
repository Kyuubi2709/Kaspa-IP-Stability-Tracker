// Called when page loads
document.addEventListener('DOMContentLoaded', () => {
    fetchStats();
    fetchHistory();

    // Refresh stats every 60 seconds automatically
    setInterval(fetchStats, 60000);
});

// Handle Fetch Now button click
document.getElementById('fetch-now-btn').addEventListener('click', async () => {
    const statusEl = document.getElementById('fetch-status');
    statusEl.textContent = "Fetching...";

    try {
        const res = await fetch('/api/fetch-now', { method: 'POST' });
        const data = await res.json();

        statusEl.textContent = data.message || "Fetch completed.";

        // Update dashboard metrics immediately
        if (data.stats) {
            document.getElementById('last-poll').textContent = data.stats.last_poll;
            document.getElementById('new-ips').textContent = data.stats.new_ips;
            document.getElementById('avg-4h').textContent = data.stats.avg_per_4h;
        }

        // Refresh the chart
        fetchHistory();

    } catch (err) {
        console.error("Error fetching data:", err);
        statusEl.textContent = "Error calling API";
    }
});

// Fetch current stats
async function fetchStats() {
    try {
        const res = await fetch('/api/stats');
        const data = await res.json();

        if (data) {
            document.getElementById('last-poll').textContent = data.last_poll;
            document.getElementById('new-ips').textContent = data.new_ips;
            document.getElementById('avg-4h').textContent = data.avg_per_4h;
        }
    } catch (err) {
        console.error("Error fetching stats:", err);
    }
}

// Fetch historical data for chart
async function fetchHistory() {
    try {
        const res = await fetch('/api/history');
        const data = await res.json();

        if (data && window.updateChart) {
            window.updateChart(data);
        }
    } catch (err) {
        console.error("Error fetching history:", err);
    }
}
