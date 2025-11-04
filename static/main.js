async function fetchStats() {
    const res = await fetch('/api/stats');
    const data = await res.json();
    document.getElementById('last-poll').textContent = data.last_poll;
    document.getElementById('new-ips').textContent = data.new_ips;
    document.getElementById('avg-4h').textContent = data.avg_per_4h;
}

// Optional: chart historical averages
async function fetchHistory(){
    const res = await fetch('/api/history');
    const data = await res.json();
    const labels = data.map((x,i) => i+1); // simple index for now
    const changes = data.map(x => 1); // each entry is 1 change
    const ctx = document.getElementById('chart').getContext('2d');
    new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [{label: 'IP Changes Over Time', data: changes, borderColor: 'blue', fill: false}]
        }
    });
}

fetchStats();
fetchHistory();
setInterval(fetchStats, 60 * 1000); // update stats every 1 min
