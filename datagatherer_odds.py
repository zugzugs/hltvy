import requests
from bs4 import BeautifulSoup
import json
import logging
import re
import hashlib
from datetime import datetime, timezone
from pathlib import Path

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

FLARE_SOLVER_URL = "http://localhost:8191/v1"
USE_FLARE = True
DATA_FILE = Path("hltv_odds_history.json")

# ───────────────────────── HELPERS ─────────────────────────

def utc_now():
    return datetime.now(timezone.utc).isoformat()


def stable_match_id(team1, team2, url):
    """
    HLTV betting links are not guaranteed to have numeric match IDs.
    This guarantees a stable ID across runs.
    """
    raw = f"{team1.lower()}::{team2.lower()}::{url or ''}"
    return hashlib.md5(raw.encode("utf-8")).hexdigest()


def load_history():
    if DATA_FILE.exists():
        return json.loads(DATA_FILE.read_text(encoding="utf-8"))
    return {}


def save_history(history):
    DATA_FILE.write_text(
        json.dumps(history, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )

# ───────────────────────── HTTP ─────────────────────────

def get_html(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
        "Referer": "https://www.hltv.org/",
        "Accept-Language": "en-US,en;q=0.9",
    }

    if USE_FLARE:
        try:
            payload = {
                "cmd": "request.get",
                "url": url,
                "maxTimeout": 65000,
                "cookies": [],
            }
            resp = requests.post(FLARE_SOLVER_URL, json=payload, timeout=100)
            resp.raise_for_status()
            data = resp.json()
            if data.get("status") == "ok":
                return data["solution"]["response"]
            logging.error("FlareSolverr error: %s", data.get("message"))
        except Exception as e:
            logging.error("FlareSolverr failed: %s", e)
        return None

    try:
        r = requests.get(url, headers=headers, timeout=25)
        r.raise_for_status()
        return r.text
    except Exception as e:
        logging.error("Direct request failed: %s", e)
        return None

# ───────────────────────── PARSER (UNCHANGED) ─────────────────────────

def parse_matches(html):
    if not html:
        return []

    soup = BeautifulSoup(html, "lxml")
    matches = []

    match_containers = soup.find_all("div", class_="b-match-container")
    if not match_containers:
        logging.warning("No 'b-match-container' found – trying fallback selectors")
        match_containers = soup.find_all(["div"], class_=re.compile(r"match|upcoming"))

    for container in match_containers:
        table = container.find("table", class_="bookmakerMatch")
        if not table:
            continue

        team_divs = table.find_all("div", class_="team-name")
        if len(team_divs) >= 2:
            team1 = team_divs[0].get_text(strip=True)
            team2 = team_divs[1].get_text(strip=True)
        else:
            team_spans = table.find_all(["span", "div"], class_=re.compile(r"team|text-ellipsis"))
            if len(team_spans) < 2:
                continue
            team1 = team_spans[0].get_text(strip=True)
            team2 = team_spans[1].get_text(strip=True)

        link_tag = table.find("a", class_="a-reset")
        match_href = link_tag["href"] if link_tag else None
        full_url = f"https://www.hltv.org{match_href}" if match_href and match_href.startswith("/") else match_href

        odds = {}
        provider_cells = table.find_all(
            "td",
            class_=lambda v: v and any("odds-provider" in c for c in v.split())
        )

        cell_index = 0
        for cell in provider_cells:
            classes = cell.get("class", [])
            provider_cls = next((c for c in classes if "odds-provider" in c), None)
            if not provider_cls:
                continue

            provider = re.sub(r"^(b-list-)?odds-provider-", "", provider_cls).lower()
            side = "team1" if cell_index % 2 == 0 else "team2"

            txt = cell.get_text(strip=True)
            if re.match(r"^\d+\.?\d{1,2}$", txt):
                odds.setdefault(provider, {})[side] = float(txt)

            cell_index += 1

        if odds:
            matches.append({
                "team1": team1,
                "team2": team2,
                "odds": odds,
                "match_url": full_url,
            })

    return matches

# ───────────────────────── MAIN (TRACKING ADDED) ─────────────────────────

def main():
    url = "https://www.hltv.org/betting/money"
    html = get_html(url)

    if not html:
        logging.error("Failed to retrieve page")
        return

    results = parse_matches(html)
    logging.info("Extracted %d matches", len(results))

    history = load_history()
    ts = utc_now()

    for match in results:
        mid = stable_match_id(
            match["team1"],
            match["team2"],
            match["match_url"]
        )

        snapshot = {
            "ts": ts,
            "odds": match["odds"]
        }

        if mid not in history:
            history[mid] = {
                "team1": match["team1"],
                "team2": match["team2"],
                "match_url": match["match_url"],
                "snapshots": []
            }

        history[mid]["snapshots"].append(snapshot)

    save_history(history)

    # Console preview
    for match in results:
        print(f"{match['team1']} vs {match['team2']}")
        for prov, sides in match["odds"].items():
            print(f"  {prov:15} {sides}")
        print("─" * 60)


if __name__ == "__main__":
    main()
