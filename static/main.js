let chartInstance = null;

// Fetch and display current stats
async function fetchStats() {
    const res = await fetch('/api/stats');
    const data = await res.json();
    document.getElementById('last-poll').textContent = data.last_poll;
    document.getElementById('new-ips').textContent = data.new_ips;
    document.getElementById('avg-4h').textContent = data.avg_per_4h;
}

// Fetch and render IP history chart + table
async function fetchHistory() {
    const res = await fetch('/api/history');
    const data = await res.json();

    // Format timestamps nicely for chart
    const labels = data.map((h) =>
        new Date(h.timestamp).toLocaleString([], {
            hour: '2-digit',
            minute: '2-digit',
            day: '2-digit',
            month: 'short'
        })
    );
    const changes = data.map((h) => h.change_count);

    // Create or update chart
    const ctx = document.getElementById('chart').getContext('2d');
    if (chartInstance) {
        chartInstance.data.labels = labels;
        chartInstance.data.datasets[0].data = changes;
        chartInstance.update();
    } else {
        chartInstance = new Chart(ctx, {
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
                    x: {
                        title: { display: true, text: 'Timestamp (UTC)' }
                    },
                    y: {
                        beginAtZero: true,
                        title: { display: true, text: 'IP Changes' }
                    }
                },
                plugins: {
                    legend: { display: true },
                    tooltip: { enabled: true }
                }
            }
        });
    }

    // Update the table below the chart
    updateTable(data);
}

// Build the data table showing each API call
function updateTable(data) {
    const tableContainer = document.getElementById('data-table');
    if (!data.length) {
        tableContainer.innerHTML = "<p>No data yet.</p>";
        return;
    }

    let html = `
        <table style="width:100%; border-collapse:collapse; margin-top:20px;">
            <thead>
                <tr style="background:#007BFF; color:white;">
                    <th style="padding:8px;">Timestamp (UTC)</th>
                    <th style="padding:8px;">IP Changes</th>
                    <th style="padding:8px;">Total IPs</th>
                </tr>
            </thead>
            <tbody>
    `;
    for (const h of data.slice().reverse()) { // newest first
        html += `
            <tr style="text-align:center; background:#fff;">
                <td style="padding:6px;">${new Date(h.timestamp).toUTCString()}</td>
                <td style="padding:6px;">${h.change_count}</td>
                <td style="padding:6px;">${h.total_ips}</td>
            </tr>
        `;
    }
    html += `</tbody></table>`;
    tableContainer.innerHTML = html;
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
            document.getElementById('avg-4h').textContent = data.stats.avg_per_4h;
        }

        fetchStats();
        fetchHistory();
    } catch (err) {
        statusEl.textContent = "Error calling API";
        console.error(err);
    }
});

// Initial load
fetchStats();
fetchHistory();
setInterval(fetchStats, 60 * 1000); // refresh stats every minute
