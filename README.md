# Stock Checker

This application allows you to enter a stock symbol and retrieve the current stock data (price, daily change, and percentage change). It also displays a list of related companies for quick navigation.

## Features

- **Symbol Lookup**: Enter a stock symbol (e.g., `AAPL`) and fetch real-time data such as current price, change, and percent change.
- **Related Companies**: Automatically display peer symbols if available.
- **Loading Spinner**: A visual indicator shows while the data is being fetched.
- **Error Handling**: Clear messages guide you if the symbol is invalid or network issues occur.

## Requirements

- Python 3 or higher  
- Flask  
- Flask-Cors  
- Requests  
- A valid [Finnhub](https://finnhub.io/) API Key set as `FINNHUB_API_KEY` environment variable

## Setup

1. **Clone or download this repository.**
2. **Install the dependencies** (for example):
   ```bash
   pip install flask flask-cors requests
   ```
3. **Set up environment variables**:
   - `FINNHUB_API_KEY` (Required)  
   - `FINNHUB_BASE_URL` (Optional, defaults to `https://finnhub.io/api/v1`)

   For example:
   ```bash
   export FINNHUB_API_KEY="your_api_key"
   export FINNHUB_BASE_URL="https://finnhub.io/api/v1"  # Optional
   ```
4. **Run the application**:
   ```bash
   python app.py
   ```
5. **Open your browser** and navigate to [http://localhost:5000](http://localhost:5000).

## File Overview

- **app.py**  
  Contains the Flask application, including:
  - `/` route to serve the main HTML page.  
  - `/stock` route to fetch and return current stock data and related companies.
  - Uses environment variables for Finnhub API settings.

- **templates/index.html**  
  Displays a form to enter a stock symbol and shows:
  - Company name (or symbol if unavailable)
  - Current price, daily change, and percentage change
  - A list of peer symbols (related companies) if available

- **static/styles.css**  
  Defines the basic styling for the page. There may be some inline CSS within `index.html` to handle layout and the loading spinner.

## Usage

1. **Enter Symbol**  
   Type a valid stock symbol (e.g., `AAPL`, `AMZN`, etc.) in the input field.
2. **Submit**  
   Click **Search** to fetch real-time data.
3. **View Results**  
   The page will display:
   - Company name and symbol
   - Current stock price
   - Daily change and percentage change
   - Related companies (if available)

## Customization

- **Custom Style**  
  Modify or extend `styles.css` to change the page’s appearance.
- **Rate Limit & Handling**  
  [Finnhub API](https://finnhub.io/) enforces rate limits. You may add backoff/retry logic in `app.py` if needed.
- **Localization**  
  To localize labels and messages, edit the text in `index.html` and `app.py`.

## Troubleshooting

- **Empty/Invalid Symbol**  
  An error message appears if an invalid or unknown stock symbol is entered.
- **Peers Not Displaying**  
  Some symbols may not have any peers returned by the API.
- **Network/Timeout Errors**  
  Check your internet connection or verify the Finnhub API key in your environment. Refer to the console logs for more details.
