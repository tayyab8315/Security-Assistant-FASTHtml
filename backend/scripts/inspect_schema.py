import json
from backend.app.catalog import live_or_static_catalog

if __name__ == "__main__":
    print(json.dumps(live_or_static_catalog(), indent=2, default=str))
