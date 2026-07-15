# Stock Research Agent

A web app that takes a stock ticker, pulls real financial data, and generates an AI-powered analysis with a bullish/bearish/mixed stance — built from scratch as a learning project.

## What it does

1. Enter a stock ticker (e.g. `AAPL`, `MSFT`)
2. The app fetches, in real time:
   - Current price and daily change
   - Key fundamentals (P/E ratio, market cap, 52-week high/low, dividend yield, EPS, beta)
   - Recent company news (past 7 days)
3. All of that is passed to Google's Gemini model, which returns a structured analysis: a summary, a stance (**BULLISH**, **BEARISH**, or **MIXED**), and reasoning grounded in the specific data pulled

The AI is explicitly instructed to say **MIXED** rather than forcing a bullish or bearish call when the underlying data doesn't clearly support one — the goal is a tool that reflects genuine uncertainty rather than always sounding confident.

## Tech stack

- **Backend:** Python, Flask
- **Market data:** [Finnhub API](https://finnhub.io) (free tier)
- **AI analysis:** Google Gemini (`gemini-2.5-flash`) via the `google-genai` SDK
- **Frontend:** Server-rendered HTML/CSS (Jinja2 templates), no JS framework

## Architecture

```
User enters ticker → Flask (/analyze)
                          │
              ┌───────────┼───────────┐
              ▼                       ▼
        Finnhub API              Gemini API
   (quote, fundamentals,       (analysis + stance,
        news)                   built from the data)
              └───────────┬───────────┘
                          ▼
                 Rendered results page
```

- `finnhub_client.py` — fetches and curates quote, fundamentals, and news data from Finnhub
- `gemini_client.py` — builds a structured prompt from that data and calls Gemini for analysis
- `app.py` — Flask routes tying it together, with error handling for invalid tickers and API failures
- `templates/` — `index.html`, `results.html`, `error.html`

## Known limitations

- **US-listed stocks only (NYSE/NASDAQ).** Finnhub's free tier returns a `403 Forbidden` for real-time quotes on international exchanges (e.g. NSE/BSE), even though those symbols are nominally supported by the API. This is a data-provider plan restriction, not something fixable in application code.
- News relevance is loosely scoped — Finnhub's `company-news` endpoint occasionally surfaces articles that mention the company only tangentially (e.g. a nearby real estate deal), rather than being strictly about the company itself.
- No caching — every search re-fetches fresh data and re-runs the AI analysis, even for a ticker searched moments earlier.
- This is an educational/demo tool, not financial advice. AI-generated analysis should not be used as the sole basis for investment decisions.

## What I learned building this

- Making and validating REST API calls with `requests`, including handling responses that return `200 OK` but contain no useful data
- Reading and curating large, inconsistent real-world API responses
- Working with Unix timestamps and computing relative date ranges
- Structuring unstructured data into an effective LLM prompt
- Migrating between SDK versions (`google-generativeai` → `google-genai`)
- Building a minimal Flask app with proper error handling (`try`/`except` around external API calls)

## Author

**Yash Shingavi**
- GitHub: []
- LinkedIn: [https://www.linkedin.com/in/yash-shingavi-18213937b/]