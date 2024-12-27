from flask import Flask, request, jsonify, render_template
import requests
from flask_cors import CORS
import os
from dotenv import load_dotenv

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


@app.route("/")
def index():
    """
    Serve the front-end HTML page.
    """
    return render_template("index.html")


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
        quote_response = requests.get(
            f"{BASE_URL}/quote", params={"symbol": symbol, "token": API_KEY}
        )
        quote_response.raise_for_status()  # Raise an error for bad status codes
        quote_data = quote_response.json()

        # Validate quote data
        if "c" not in quote_data or quote_data["c"] == 0:
            return jsonify({"error": "Invalid stock symbol or no data available"}), 404

        # Fetch peers data
        peers_response = requests.get(
            f"{BASE_URL}/stock/peers", params={"symbol": symbol, "token": API_KEY}
        )
        peers_response.raise_for_status()
        peers_data = peers_response.json()

        # Ensure peers data is a valid list
        if not isinstance(peers_data, list):
            peers_data = []

        # Fetch company profile for dynamic company name
        profile_response = requests.get(
            f"{BASE_URL}/stock/profile2", params={"symbol": symbol, "token": API_KEY}
        )
        profile_response.raise_for_status()
        profile_data = profile_response.json()

        company_name = profile_data.get("name", f"{symbol.upper()} Inc.")

        # Return stock data and peers
        return jsonify(
            {
                "symbol": symbol.upper(),
                "company_name": company_name,
                "current_price": quote_data["c"],
                "change": quote_data["d"],
                "percent_change": quote_data["dp"],
                "peers": peers_data,
            }
        )
    except requests.HTTPError as http_err:
        return jsonify({"error": f"HTTP error occurred: {http_err}"}), 500
    except requests.RequestException as req_error:
        return jsonify({"error": f"Network error: {str(req_error)}"}), 500
    except Exception as e:
        return jsonify({"error": f"Failed to fetch stock data: {str(e)}"}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
