# Stock Checker

This application allows you to enter a stock symbol and retrieve the current stock data (price, daily change, and percentage change). It also displays a list of related companies for quick navigation(WIP), it is still in very early development as Im a beginner and I want to expand it a lot more.

## Features

- **Symbol Lookup**: Enter a stock symbol (e.g., `AAPL`) and fetch real-time data such as current price, change, and percent change.
- **Related Companies**: Automatically display peer symbols if available.
- **Loading Spinner**: A visual indicator shows while the data is being fetched.
- **Error Handling**: Clear messages guide you if the symbol is invalid or network issues occur.

## Requirements

- Python 3 or higher  
- Flask (`pip install flask`)  
- Requests (`pip install requests`)  
- A valid [Finnhub](https://finnhub.io/) API Key set as `FINNHUB_API_KEY` environment variable

## Setup

1. **Clone or download this repository.**
2. **Install the dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
3. **Ensure your environment has the `FINNHUB_API_KEY` (and optional `FINNHUB_BASE_URL`) set:**
   ```bash
   export FINNHUB_API_KEY="your_api_key"
   export FINNHUB_BASE_URL="https://finnhub.io/api/v1"  # Optional
   ```
4. **Run the application:**
   ```bash
   python app.py
   ```
5. **Open your browser and navigate to** [http://localhost:5000](http://localhost:5000).

## File Overview

- **app.py**  
  Contains the Flask application, including:
  - `/` route to serve the main HTML page.  
  - `/stock` route to fetch and return current stock data and related companies.

- **templates/index.html**  
  Provides a form where you enter a stock symbol, then displays:
  - Company name (or symbol if unavailable)
  - Current price, daily change, and percentage change
  - Related companies as a list of peer symbols

- **static/styles.css**  
  Defines basic styling for the page. Additional inline styles in `index.html` handle the layout for the peers section and the loading spinner.

## Usage

1. **Enter Symbol**  
   Enter a valid stock symbol (e.g., `AAPL` or `AMZN`) in the text box.
2. **Submit**  
   Click **Search** to fetch real-time data.
3. **View Results**  
   The page updates with:
   - Company name and symbol
   - Current stock price
   - Daily change and percentage change
   - Related companies (if available)

## Customization

- **Custom Style**  
  Adjust or add CSS in `styles.css` to change the page’s appearance.
- **Rate Limit & Handling**  
  [Finnhub API](https://finnhub.io/) enforces rate limits. Enhance `app.py` if you need backoff or retry logic.
- **Localization**  
  To localize output text, modify the strings in `index.html` and `app.py`.

## Troubleshooting

- **Empty/Invalid Symbol**  
  The page displays an error message for invalid or unknown stock symbols.
- **Peers Not Displaying**  
  Some symbols may not have any peers returned by the API.
- **Network/Timeout Errors**  
  Check your internet connection or the Finnhub API key and logs for details.
