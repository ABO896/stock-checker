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
CORS(app)

API_KEY = "your_api_key"  # Replace with your API key
BASE_URL = "https://finnhub.io/api/v1"

@app.route('/')
def index():
    """Serve the front-end HTML page."""
    return render_template('index.html')

@app.route('/stock', methods=['GET'])
def get_stock_data():
    """Fetch current stock data."""
    symbol = request.args.get('symbol', '').upper()
    if not symbol:
        return jsonify({"error": "No stock symbol provided"}), 400

    try:
        response = requests.get(f"{BASE_URL}/quote", params={"symbol": symbol, "token": API_KEY})
        data = response.json()
        if response.status_code != 200 or 'c' not in data:
            return jsonify({"error": "Stock data not found."}), 404
        return jsonify({
            "symbol": symbol,
            "current_price": data.get('c'),
            "change": data.get('d'),
            "percent_change": data.get('dp')
        })
    except Exception as e:
        return jsonify({"error": f"Failed to fetch stock data: {str(e)}"}), 500

@app.route('/graph', methods=['GET'])
def plot_stock_data():
    """Generate a stock price graph."""
    symbol = request.args.get('symbol', '').upper()
    if not symbol:
        return jsonify({"error": "No stock symbol provided"}), 400

    try:
        # Fetch historical data
        end_time = int(datetime.datetime.now().timestamp())
        start_time = end_time - 5 * 86400  # Last 5 days
        response = requests.get(
            f"{BASE_URL}/stock/candle",
            params={
                "symbol": symbol,
                "resolution": "D",
                "from": start_time,
                "to": end_time,
                "token": API_KEY
            }
        )
        data = response.json()
        if data.get('s') != 'ok':
            return jsonify({"error": "No historical data available"}), 404

        days = [datetime.datetime.fromtimestamp(ts).strftime('%a') for ts in data['t']]
        prices = data['c']

        # Plot the graph
        plt.figure(figsize=(5, 3))
        plt.plot(days, prices, marker='o')
        plt.title(f"Stock Prices for {symbol} Over the Week")
        plt.xlabel("Day")
        plt.ylabel("Price")
        plt.grid(True)

        # Save plot to buffer
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        encoded_image = base64.b64encode(buf.read()).decode('utf-8')
        buf.close()

        return jsonify({"graph": f"data:image/png;base64,{encoded_image}"})
    except Exception as e:
        return jsonify({"error": f"Failed to generate graph: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(debug=True)
