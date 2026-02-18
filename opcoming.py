import requests

FLARE_SOLVERR_URL = "http://localhost:8191/v1"
TARGET_URL = "https://www.hltv.org/matches"
OUTPUT_FILE = "matches.html"

def main():
    payload = {
        "cmd": "request.get",
        "url": TARGET_URL,
        "maxTimeout": 60000
    }

    response = requests.post(FLARE_SOLVERR_URL, json=payload, timeout=120)
    response.raise_for_status()

    data = response.json()

    if data.get("status") != "ok":
        raise RuntimeError("FlareSolverr failed to solve the page")

    html = data["solution"]["response"]

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"Saved HTML to {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
