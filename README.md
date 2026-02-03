# CS:GO/CS2 Betting Data Collection

🤖 **Automated data collection system for CS:GO/CS2 match odds and results**

## 📊 Current Statistics

**Last Updated:** 2026-02-03 15:11:13 UTC

### Upcoming Matches
- **Total matches with odds:** 0/0
- **Active bookmakers:** None
- **Most frequent teams:** None

### Historical Results  
- **Total matches collected:** 0
- **Enriched with details:** 0 (0.0%)
- **Date range:** None to None
- **Top events:** None
- **Most played maps:** None

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
