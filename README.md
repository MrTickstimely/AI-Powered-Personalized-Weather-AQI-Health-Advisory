# AI-Powered-Personalized-Weather-AQI-Health-Advisory
# 🌤️ Personalized Weather & AQI Health Advisory

## Why this matters

On **August 26, 2026**, a glacier collapse on Langtang Lirung in Nepal triggered a catastrophic flash flood that swept nearly 100 km down the Trishuli River, killing over 1,000 people and leaving thousands missing. Existing flood monitoring systems were tuned for monsoon patterns — the region that failed was, in the words of one disaster expert, a total "blind spot."

The lesson isn't that this specific tool would have stopped that disaster — it wouldn't have. The lesson is broader: **climate and environmental risk hits people unevenly, and generic, one-size-fits-all alerts consistently fail the people who need tailored warnings most** — the elderly, people with respiratory or heart conditions, outdoor workers, children. A single blanket AQI warning or weather alert doesn't tell an asthmatic teenager and a healthy office worker anything different, even though their actual risk is wildly different.

This project is a small step in the opposite direction: instead of generic thresholds, it generates a **personalized, plain-English health advisory** based on who you are — not just where you are.

---

## What it does

- Pulls **live weather** (temperature, humidity) via the free Open-Meteo API
- Pulls **live AQI** for the nearest monitoring station via the WAQI API
- Takes a simple health profile: age group, health condition, occupation type
- Uses an LLM (via Groq) to generate a **short, direct, personalized advisory** — not a generic threshold message
- Tracks recent checks in-session so users can see how conditions are trending

---

## Tech stack

| Layer | Tool |
|---|---|
| Frontend | Streamlit |
| Weather data | Open-Meteo (free, no key) |
| AQI data | WAQI (free tier, token-based) |
| AI advisory | Groq API (`qwen/qwen3.8-27b`) |
| Language | Python |

---

## How it works

1. User selects a city (or types a custom one) and fills a short profile
2. App geocodes the city → gets lat/lon
3. Lat/lon is used to fetch **both** weather and the nearest AQI station (more accurate than name-based lookup, since city names can match the wrong station)
4. Live data + profile are passed to an LLM prompt asking for a specific, practical advisory
5. Advisory is displayed alongside the raw numbers, so the AI's reasoning stays checkable — not a black box

---

## Setup

```bash
pip install streamlit requests python-dotenv groq
```

Create a `.env` file:
```
WAQI_TOKEN=your_waqi_token
GROQ_API_KEY=your_groq_key
```

Run:
```bash
streamlit run app.py
```

---

## Honest limitations

- AQI/weather values are pulled from free public APIs and may differ slightly from other AQI sites due to differing standards (US EPA AQI vs. Indian National AQI) or station selection — this is a known tradeoff of free-tier data, not a bug in the pipeline.
- This is a 10-hour hackathon build. It does not replace official emergency alert systems, and makes no claim to disaster prediction — it addresses everyday exposure risk (heat, humidity, air quality), which is a different and more tractable problem than flash-flood forecasting.

---

## Disqualification compliance
No hardcoded/fake data presented as live — every number shown comes from a live API call at request time.
