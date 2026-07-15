import os
from google import genai
from dotenv import load_dotenv
from finnhub_client import get_quote, get_fundamentals, get_news

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=GEMINI_API_KEY)


def test_gemini():
    """
    Quick sanity check — sends a hardcoded prompt to confirm the API key and setup work.
    """
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents="Say hello and confirm you're working, in one sentence."
    )
    return response.text


def build_prompt(ticker, quote, fundamentals, news):
    """
    Takes raw data from Finnhub and formats it into a text prompt for Gemini.
    """
    news_lines = []
    for i, article in enumerate(news, start=1):
        news_lines.append(f"{i}. \"{article['headline']}\" ({article['source']})")
    news_text = "\n".join(news_lines)

    prompt = f"""You are a financial analyst. Analyze the following stock data for {ticker} 
and provide a concise summary followed by a clear stance: BULLISH, BEARISH, or MIXED.
If the data doesn't clearly support a direction, say MIXED and explain why — 
do not force a bullish or bearish call when the signals conflict.

CURRENT PRICE DATA:
Current Price: ${quote['c']}
Change: ${quote['d']} ({quote['dp']}%)
Day's High: ${quote['h']}
Day's Low: ${quote['l']}

FUNDAMENTALS:
P/E Ratio: {fundamentals['pe_ratio']}
Market Cap: ${fundamentals['market_cap']} million
52-Week High: ${fundamentals['52_week_high']}
52-Week Low: ${fundamentals['52_week_low']}
Dividend Yield: {fundamentals['dividend_yield']}%
EPS: {fundamentals['eps']}
Beta: {fundamentals['beta']}

RECENT NEWS:
{news_text}

Provide your analysis in this format:
SUMMARY: (2-3 sentences)
STANCE: (BULLISH, BEARISH, or MIXED)
REASONING: (2-3 sentences justifying the stance using the specific data above)
"""
    return prompt


def get_ai_analysis(ticker, quote, fundamentals, news):
    """
    Sends the built prompt to Gemini and returns the analysis text.
    """
    prompt = build_prompt(ticker, quote, fundamentals, news)
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )
    return response.text


if __name__ == "__main__":
    result = test_gemini()
    print(result)

    ticker = "AAPL"
    quote = get_quote(ticker)
    fundamentals = get_fundamentals(ticker)
    news = get_news(ticker)

    analysis = get_ai_analysis(ticker, quote, fundamentals, news)
    print(analysis)