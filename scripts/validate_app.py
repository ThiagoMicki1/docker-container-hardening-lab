import json
import sys
from urllib.error import URLError
from urllib.request import urlopen


def fetch_json(url: str) -> dict:
    with urlopen(url, timeout=5) as response:
        return json.loads(response.read().decode("utf-8"))


def validate(base_url: str) -> int:
    try:
        health = fetch_json(f"{base_url}/health")
        index = fetch_json(f"{base_url}/")
    except (TimeoutError, URLError, json.JSONDecodeError) as error:
        print(f"[FAIL] Could not validate app at {base_url}: {error}")
        return 1

    if health.get("status") != "healthy":
        print(f"[FAIL] Health endpoint returned unexpected body: {health}")
        return 1

    if index.get("status") != "ok":
        print(f"[FAIL] Index endpoint returned unexpected body: {index}")
        return 1

    print(f"[OK] App validation passed for {base_url}")
    return 0


if __name__ == "__main__":
    target = sys.argv[1] if len(sys.argv) > 1 else "http://127.0.0.1:8000"
    raise SystemExit(validate(target))
