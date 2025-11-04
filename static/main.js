from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from tracker import Tracker
import asyncio

app = FastAPI()

# Allow frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # restrict later if needed
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize tracker
tracker = Tracker(api_url="https://api.kaspa.org/info/peers")  # your real API endpoint here

# ------------------------
# 🔁 Automatic background task
# ------------------------
@app.on_event("startup")
async def start_background_fetch():
    """Runs automatic IP fetch every 1 hour."""
    async def auto_fetch():
        while True:
            print("[Auto Fetch] Calling tracker.update_ips() ...")
            tracker.update_ips()
            print("[Auto Fetch] Stats updated:", tracker.get_stats())
            await asyncio.sleep(3600)  # 3600 sec = 1 hour

    asyncio.create_task(auto_fetch())


# ------------------------
# 🖱 Manual fetch endpoint
# ------------------------
@app.get("/api/fetch")
def fetch_ips():
    """Manual trigger for Fetch Now button."""
    tracker.update_ips()
    stats = tracker.get_stats()
    return {"status": "success", "message": "API called successfully", "stats": stats}


# ------------------------
# 📊 Stats endpoint
# ------------------------
@app.get("/api/stats")
def get_stats():
    """Return latest tracker stats for dashboard cards."""
    stats = tracker.get_stats()
    return stats


# ------------------------
# 📈 History endpoint
# ------------------------
@app.get("/api/history")
def get_history():
    """Return IP change history for the chart."""
    return {"history": tracker.get_history()}
