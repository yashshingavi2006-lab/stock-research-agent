from flask import Flask, render_template, request
from finnhub_client import get_quote, get_fundamentals, get_news
from gemini_client import get_ai_analysis

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/analyze")
def analyze():
    ticker = request.args.get("ticker")

    try:
        quote = get_quote(ticker)
        fundamentals = get_fundamentals(ticker)
        news = get_news(ticker)
        analysis = get_ai_analysis(ticker, quote, fundamentals, news)

        return render_template(
            "results.html",
            ticker=ticker,
            quote=quote,
            fundamentals=fundamentals,
            news=news,
            analysis=analysis
        )
    except Exception as e:
        return render_template("error.html", ticker=ticker, error=str(e))


if __name__ == "__main__":
    app.run(debug=True)