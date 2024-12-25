import matplotlib
matplotlib.use('Agg')  # Use non-GUI backend for server rendering
import matplotlib.pyplot as plt
from flask import Flask, request, jsonify, render_template
import requests
import io
import base64
from flask_cors import CORS
import datetime

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Finnhub API Key
API_KEY = "ctm58v9r01qvk0t3brsgctm58v9r01qvk0t3brt0"
BASE_URL = "https://finnhub.io/api/v1"

@app.route('/')
def index():
    """Serve the front-end HTML page."""
    return render_template('index.html')

@app.route('/stock', methods=['GET'])
def get_stock_data():
    """Fetch current stock data (price, change, percent change) for a given symbol."""
    symbol = request.args.get('symbol')
    if not symbol:
        return jsonify({"error": "No stock symbol provided"}), 400

    symbol = symbol.upper()  # Ensure symbol is uppercase
    try:
        # Fetch stock quote from Finnhub API
        response = requests.get(f"{BASE_URL}/quote", params={"symbol": symbol, "token": API_KEY})
        data = response.json()

        # Debugging: Log API response
        print(f"Stock Data Response for {symbol}: {data}")

        # Check for errors in the API response
        if response.status_code != 200 or 'c' not in data:
            return jsonify({"error": "Invalid stock symbol or no data available"}), 404

        # Return stock data
        return jsonify({
            "symbol": symbol,
            "current_price": data['c'],
            "change": data['d'],
            "percent_change": data['dp']
        })
    except Exception as e:
        return jsonify({"error": f"Failed to fetch stock data: {str(e)}"}), 500

@app.route('/graph', methods=['GET'])
def plot_stock_data():
    """Generate a graph for a given stock symbol using historical data."""
    symbol = request.args.get('symbol')
    if not symbol:
        return jsonify({"error": "No stock symbol provided"}), 400

    symbol = symbol.upper()  # Ensure symbol is uppercase
    try:
        # Get the past 5 days of historical data
        end_time = int(datetime.datetime.now().timestamp())
        start_time = end_time - 5 * 86400  # 5 days in seconds
        response = requests.get(
            f"{BASE_URL}/stock/candle",
            params={
                "symbol": symbol,
                "resolution": "D",  # Daily data
                "from": start_time,
                "to": end_time,
                "token": API_KEY
            }
        )
        data = response.json()

        # Debugging: Log historical data response
        print(f"Historical Data Response for {symbol}: {data}")

        if data.get('s') != 'ok':  # Check if data fetch was successful
            return jsonify({"error": "No historical data available or invalid symbol"}), 404

        # Extract days and prices
        days = [datetime.datetime.fromtimestamp(ts).strftime('%a') for ts in data.get('t', [])]
        prices = data.get('c', [])

        if not days or not prices:
            return jsonify({"error": "Insufficient data to generate graph"}), 404

        # Generate the graph
        plt.figure(figsize=(5, 3))
        plt.plot(days, prices, marker='o')
        plt.title(f"Stock Prices for {symbol} Over the Week")
        plt.xlabel("Day")
        plt.ylabel("Price")
        plt.grid(True)

        # Save the plot to a bytes buffer
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        encoded_image = base64.b64encode(buf.read()).decode('utf-8')
        buf.close()

        return jsonify({"graph": f"data:image/png;base64,{encoded_image}"})
    except Exception as e:
        import traceback
        traceback.print_exc()  # Log the traceback for debugging
        return jsonify({"error": f"Failed to generate graph: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
