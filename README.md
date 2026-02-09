# CS:GO/CS2 Betting Data Collection

🤖 **Automated data collection system for CS:GO/CS2 match odds and results**

## 📊 Current Statistics

**Last Updated:** 2026-02-09 23:13:37 UTC

### Upcoming Matches
- **Total matches with odds:** 0/0
- **Active bookmakers:** None
- **Most frequent teams:** None

### Historical Results  
- **Total matches collected:** 23,229
- **Enriched with details:** 11,152 (48.0%)
- **Date range:** 1736550000000 to 1770255000000
- **Top events:** ESL Challenger League Season 48 South America, ESL Challenger League Season 47 South America, ESL Challenger League Season 48 North America
- **Most played maps:** Ancient, Mirage, Dust2

## 🔄 Automation

This repository automatically collects data every 4 hours using GitHub Actions:
- **Odds collection** from HLTV betting section
- **Results scraping** with detailed match statistics  
- **Data validation** and error handling
- **Automatic commits** when new data is available

## 📁 Data Files

- `upcoming.json` - Current matches with betting odds
- `results.json` - Historical match results with detailed statistics
- `scrape_state.json` - Scraping progress state (auto-generated)
- `failed_urls.json` - Failed URL log for debugging (auto-generated)

## 🛠️ Technical Details

**Dependencies:**
- Python 3.11+
- FlareSolverr (Docker container for Cloudflare bypass)
- BeautifulSoup4 for HTML parsing
- Requests for HTTP handling

**Data Sources:**
- HLTV.org betting odds
- HLTV.org match results and statistics

---
*This README is automatically updated by the data collection system.*
