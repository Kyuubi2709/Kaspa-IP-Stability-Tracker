
// Fetch and display current stats
async function fetchStats() {
    const res = await fetch('/api/stats');
    const data = await res.json();
    document.getElementById('last-poll').textContent = data.last_poll;
    document.getElementById('new-ips').textContent = data.new_ips;
    document.getElementById('avg-24h').textContent = data.avg_per_day;
    document.getElementById('total-changes').textContent = data.total_changes; // ✅ new
}

// Fetch and render IP history chart + table
async function fetchHistory() {
    const res = await fetch('/api/history');
    const data = await res.json();

    if (!data || data.length === 0) return;

    const labels = data.map((h) =>
        new Date(h.timestamp).toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" })
    );
    const changes = data.map((h) => h.change_count);

    const ctx = document.getElementById('chart').getContext('2d');

    if (window.ipChart) window.ipChart.destroy();

    window.ipChart = new Chart(ctx, {
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
            responsive: true,
            scales: {
                y: { beginAtZero: true }
            }
        }
    });

    const tbody = document.getElementById('history-body');
    tbody.innerHTML = "";
    data
        .slice()
        .reverse()
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
            document.getElementById('total-changes').textContent = data.stats.total_changes; // ✅ new
        }

        setTimeout(() => {
            fetchStats();
            fetchHistory();
        }, 800);

    } catch (err) {
        statusEl.textContent = "Error calling API";
        console.error(err);
    }
});

// Initial load
fetchStats();
fetchHistory();
setInterval(fetchStats, 60 * 1000);
