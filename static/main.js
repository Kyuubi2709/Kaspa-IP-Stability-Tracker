// Fetch and display current stats
async function fetchStats() {
    const res = await fetch('/api/stats');
    const data = await res.json();
    document.getElementById('last-poll').textContent = data.last_poll;
    document.getElementById('new-ips').textContent = data.new_ips;
    document.getElementById('avg-24h').textContent = data.avg_per_day;
}

// Fetch and render IP history chart + table
async function fetchHistory() {
    const res = await fetch('/api/history');
    const data = await res.json();

    if (!data || data.length === 0) return;

    // ---- Chart rendering ----
    const labels = data.map((h) =>
        new Date(h.timestamp).toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" })
    );
    const changes = data.map((h) => h.change_count);

    const ctx = document.getElementById('chart').getContext('2d');
    new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [
                {
                    label: 'IP Changes Over Time',
                    data: changes,
                    borderColor: 'blue',
                    fill: false,
                    tension: 0.1
                }
            ]
        },
        options: {
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });

    // ---- Table rendering ----
    const tbody = document.getElementById('history-body');
    tbody.innerHTML = ""; // clear existing rows

    data
        .slice()
        .reverse() // newest first
        .forEach((h) => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${new Date(h.timestamp).toUTCString()}</td>
                <td>${h.change_count}</td>
                <td>${h.total_ips}</td>
            `;
            tbody.appendChild(row);
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

        if (data.stats) {
            document.getElementById('last-poll').textContent = data.stats.last_poll;
            document.getElementById('new-ips').textContent = data.stats.new_ips;
            document.getElementById('avg-24h').textContent = data.stats.avg_per_day;
        }

        fetchStats();
        setTimeout(fetchHistory, 500); // wait half a second before reloading table/chart
    } catch (err) {
        statusEl.textContent = "Error calling API";
        console.error(err);
    }
});

// Initial load
fetchStats();
fetchHistory();
setInterval(fetchStats, 60 * 1000); // refresh stats every minute
