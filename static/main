async function fetchHistory(){
    const res = await fetch('/api/history');
    const data = await res.json();
    const labels = data.map(x => x.timestamp);
    const changes = data.map(x => x.changes);
    const ctx = document.getElementById('chart').getContext('2d');
    new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [{label: 'IP Changes', data: changes, borderColor: 'blue', fill: false}]
        }
    });
}
fetchHistory();
