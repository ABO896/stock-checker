from flask import Flask, request, jsonify, render_template
import requests
from flask_cors import CORS
import os
from dotenv import load_dotenv
import time

load_dotenv()


app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Load API Key from environment variables for better security
API_KEY = os.getenv("FINNHUB_API_KEY")
if not API_KEY:
    raise ValueError(
        "API Key for Finnhub is not set. Please configure it in the environment variables."
    )

BASE_URL = os.getenv("FINNHUB_BASE_URL", "https://finnhub.io/api/v1")

# Simple in-memory cache to reduce repeated API calls
CACHE_TTL = int(os.getenv("CACHE_TTL", "60"))  # seconds
_cache = {}


def cached_get(url, params=None):
    """Fetch JSON data with basic TTL caching."""
    key = (url, tuple(sorted((params or {}).items())))
    now = time.time()
    entry = _cache.get(key)
    if entry and now - entry[1] < CACHE_TTL:
        return entry[0]
    resp = requests.get(url, params=params, timeout=10)
    resp.raise_for_status()
    data = resp.json()
    _cache[key] = (data, now)
    return data


@app.route("/")
def index():
    """
    Serve the front-end HTML page.
    """
    return render_template("index.html")


@app.route("/search")
def search_symbol():
    """Return symbol suggestions for autocomplete."""
    query = request.args.get("query")
    if not query:
        return jsonify({"error": "No query provided"}), 400

    try:
        data = cached_get(
            f"{BASE_URL}/search",
            params={"q": query, "token": API_KEY},
        )
        results = []
        for item in data.get("result", [])[:5]:
            results.append(
                {
                    "symbol": item.get("symbol"),
                    "description": item.get("description"),
                }
            )
        return jsonify({"results": results})
    except requests.RequestException as err:
        return jsonify({"error": f"Failed to fetch suggestions: {err}"}), 500


@app.route("/market-status")
def market_status():
    """Return current market status for a given exchange."""
    exchange = request.args.get("exchange", "US")
    try:
        data = cached_get(
            f"{BASE_URL}/stock/market-status",
            params={"exchange": exchange, "token": API_KEY},
        )
        return jsonify(data)
    except requests.RequestException as err:
        return jsonify({"error": f"Failed to fetch market status: {err}"}), 500


@app.route("/stock", methods=["GET"])
def get_stock_data():
    """
    Fetch current stock data (price, change, percent change) and related companies for a given symbol.
    """
    symbol = request.args.get("symbol")
    if not symbol:
        return jsonify({"error": "No stock symbol provided"}), 400

    try:
        # Fetch stock quote
        quote_data = cached_get(
            f"{BASE_URL}/quote",
            params={"symbol": symbol, "token": API_KEY},
        )

        # Validate quote data
        if "c" not in quote_data or quote_data["c"] == 0:
            return jsonify({"error": "Invalid stock symbol or no data available"}), 404

        # Fetch peers data
        peers_data = cached_get(
            f"{BASE_URL}/stock/peers",
            params={"symbol": symbol, "token": API_KEY},
        )

        # Ensure peers data is a valid list
        if not isinstance(peers_data, list):
            peers_data = []

        # Fetch company profile for dynamic company name
        profile_data = cached_get(
            f"{BASE_URL}/stock/profile2",
            params={"symbol": symbol, "token": API_KEY},
        )

        company_name = profile_data.get("name", f"{symbol.upper()} Inc.")

        # Fetch basic financial metrics
        financials_json = cached_get(
            f"{BASE_URL}/stock/metric",
            params={"symbol": symbol, "metric": "all", "token": API_KEY},
        ).get("metric", {})

        basic_financials = {
            "52WeekHigh": financials_json.get("52WeekHigh"),
            "52WeekLow": financials_json.get("52WeekLow"),
            "52WeekPriceReturnDaily": financials_json.get("52WeekPriceReturnDaily"),
            "beta": financials_json.get("beta"),
        }

        # Return stock data and peers
        return jsonify(
            {
                "symbol": symbol.upper(),
                "company_name": company_name,
                "current_price": quote_data["c"],
                "change": quote_data["d"],
                "percent_change": quote_data["dp"],
                "peers": peers_data,
                "financials": basic_financials,
            }
        )
    except requests.HTTPError as http_err:
        return jsonify({"error": f"HTTP error occurred: {http_err}"}), 500
    except requests.RequestException as req_error:
        return jsonify({"error": f"Network error: {str(req_error)}"}), 500
    except Exception as e:
        return jsonify({"error": f"Failed to fetch stock data: {str(e)}"}), 500


@app.route("/company-news")
def company_news():
    """Return latest company news for a symbol between two dates."""
    symbol = request.args.get("symbol")
    from_date = request.args.get("from")
    to_date = request.args.get("to")
    if not symbol or not from_date or not to_date:
        return (
            jsonify({"error": "symbol, from and to parameters are required"}),
            400,
        )

    try:
        data = cached_get(
            f"{BASE_URL}/company-news",
            params={
                "symbol": symbol,
                "from": from_date,
                "to": to_date,
                "token": API_KEY,
            },
        )
        return jsonify(data)
    except requests.RequestException as err:
        return jsonify({"error": f"Failed to fetch company news: {err}"}), 500


@app.route("/earnings")
def earnings_surprises():
    """Return quarterly earnings surprises for a company."""
    symbol = request.args.get("symbol")
    limit = request.args.get("limit")
    if not symbol:
        return jsonify({"error": "symbol parameter is required"}), 400

    params = {"symbol": symbol, "token": API_KEY}
    if limit:
        params["limit"] = limit

    try:
        data = cached_get(f"{BASE_URL}/stock/earnings", params=params)
        return jsonify(data)
    except requests.RequestException as err:
        return jsonify({"error": f"Failed to fetch earnings data: {err}"}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
