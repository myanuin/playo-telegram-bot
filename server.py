import os
import asyncio
from flask import Flask, request
from daily_task import run_daily_update

app = Flask(__name__)

@app.route("/update-playo", methods=["POST"])
def update_playo():
    if request.headers.get("X-CRON-TOKEN") != os.getenv("CRON_SECRET"):
        return "Forbidden", 403
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(run_daily_update())
        return "OK", 200
    except Exception as e:
        return str(e), 500

if __name__ == "__main__":
    app.run(port=10001)
