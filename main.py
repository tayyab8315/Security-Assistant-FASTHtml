"""Run the unified FastHTML application with `python main.py`."""
import os
from backend.app.main import app

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=os.getenv("HOST", "127.0.0.1"), port=int(os.getenv("PORT", "8000")))
