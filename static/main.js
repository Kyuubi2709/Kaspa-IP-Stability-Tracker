// ------------------------
// DOM Elements
// ------------------------
const lastPollEl = document.getElementById("last-poll");
const newIpsEl = document.getElementById("new-ips");
const avg4hEl = document.getElementById("avg-4h");
const fetchBtn = document.getElementById("fetch-now-btn");
const fetchStatus = document.getElementById("fetch-status");

// ------------------------
// Chart setup
// ------------------------
const ctx = document.getElementById("chart").getContext("2d");
const chart = new Chart(ctx, {
    type: "line",
    data: {
        labels: [], // timestamps
        datasets: [{
            label: "IP Changes",
            data: [],
            borderColor: "#007BFF",
            backgroundColor: "rgba(0, 123, 255, 0.2)",
            tension: 0.3,
        }],
    },
    options: {
        responsive: true,
        plugins: {
            legend: { display: false },
        },
        scales: {
            x: { title: { display: true, text: "Time" } },
            y: { title: { display: true, text: "IP Changes" } },
        },
    },
});

// ------------------------
// Fetch latest stats
// ------------------------
async function fetchStats() {
    try {
        const res = await fetch("/api/stats");
        const data = await res.json();
        lastPollEl.textContent = data.last_poll || "--";
        newIpsEl.textContent = data.new_ips ?? "--";
        avg4hEl.textContent = data.avg_per_4h ?? "--";
    } catch (err) {
        console.error("Error fetching stats:", err);
    }
}

// ------------------------
// Fetch history for chart
// ------------------------
async function fetchHistory() {
    try {
        const res = await fetch("/api/history");
        const json = await res.json();
        const history = json.history || [];

        chart.data.labels = history.map(h => h.timestamp);
        chart.data.datasets[0].data = history.map(h => h.new_ips);
        chart.update();
    } catch (err) {
        console.error("Error fetching history:", err);
    }
}

// ------------------------
// Manual Fetch Now
// ------------------------
fetchBtn.addEventListener("click", async () => {
    fetchStatus.textContent = "Fetching...";
    try {
        const res = await fetch("/api/fetch");
        const data = await res.json();
        fetchStatus.textContent = "✅ Fetch complete!";
        fetchStats();
        fetchHistory();
    } catch (err) {
        fetchStatus.textContent = "❌ Fetch failed!";
        console.error("Error fetching manually:", err);
    }
    setTimeout(() => fetchStatus.textContent = "", 3000);
});

// ------------------------
// Auto-refresh dashboard every 60s
// ------------------------
fetchStats();
fetchHistory();
setInterval(() => {
    fetchStats();
    fetchHistory();
}, 60000);
