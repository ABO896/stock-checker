# Stock Checker

> **Note**: This project was created by a beginner and may contain mistakes or incomplete features. I am actively working on adding more functionality and improvements. Specifically, the peers feature is currently not working properly, but I hope to fix it soon.

This application allows you to enter a stock symbol and retrieve the current stock data (price, daily change, and percentage change). It also displays a list of related companies (peers) for quick navigation, plus a loading spinner for better user feedback.

## Features

- **Symbol Lookup**: Enter a stock symbol (e.g., `AAPL`) and fetch real-time data such as current price, change, and percentage change.
- **Related Companies**: Displays a list of peer symbols if available. *(Currently has issues, being fixed soon!)*
- **Loading Spinner**: A visual indicator while stock data is being fetched.
- **Error Handling**: Clear messages guide you if the symbol is invalid or if network issues occur.

## Requirements

- Python 3 or higher  
- Flask  
- Flask-Cors  
- Requests  
- A valid [Finnhub](https://finnhub.io/) API Key set as `FINNHUB_API_KEY` environment variable  

## Setup

1. **Clone or download this repository.**
2. **Install the dependencies**, for example:
   ```bash
   pip install flask flask-cors requests
   ```
3. **Configure Environment Variables**:
   - **FINNHUB_API_KEY** (Required)
   - **FINNHUB_BASE_URL** (Optional, defaults to `https://finnhub.io/api/v1`)
   
   For example:
   ```bash
   export FINNHUB_API_KEY="your_api_key"
   export FINNHUB_BASE_URL="https://finnhub.io/api/v1"  # Optional
   ```
4. **Run the application**:
   ```bash
   python app.py
   ```
5. **Open your browser** and go to [http://localhost:5000](http://localhost:5000).

## File Overview

- **app.py**  
  - Contains the Flask application that:
    - Serves the main HTML page at `/`.
    - Provides a `/stock` endpoint to return current stock data and a list of peer companies.
  - Utilizes environment variables for the Finnhub API key and optional base URL.

- **templates/index.html**  
  - A simple front-end page with:
    - A form to enter the stock symbol.
    - Sections to display:
      - Current price, daily change, and percentage change.
      - A list of peer symbols (related companies).
      - A loading spinner while requests are in progress.
    - Basic error messages for invalid symbols or network issues.

- **static/styles.css**  
  - Provides the default styling for the page (e.g., font, layout, colors).
  - Some inline styling in `index.html` manages the peers layout and the loading spinner’s animation.

## Usage

1. **Enter a Symbol**  
   - Type a valid stock symbol (e.g., `AAPL`, `AMZN`, etc.) in the input field.
2. **Submit**  
   - Click **Search** to fetch real-time data.
   - A loading spinner shows while the data is being retrieved.
3. **View Results**  
   - The page updates with:
     - Company name and symbol
     - Current stock price
     - Daily change and percentage change
     - Related companies (if available)

## Customization

- **Styling**  
  - Modify `styles.css` or the inline `style` section in `index.html` to change the page’s appearance, including the spinner or peer list styling.
- **Rate Limit & Handling**  
  - The [Finnhub API](https://finnhub.io/) enforces rate limits. You can add backoff or retry logic in `app.py` if you expect heavy use.
- **Localization**  
  - To support other languages, change the text in `index.html` and `app.py` accordingly.

## Troubleshooting

- **Invalid or Unknown Symbol**  
  - An error message appears if the symbol is invalid or no data is available for that ticker.
- **Peers Not Displaying**  
  - Some symbols may not have any peers returned by the API.
  - Currently, the peers feature has known issues. Updates are planned.
- **Network/Timeout Errors**  
  - Verify your internet connection and your Finnhub API key. Check `app.py` logs for details.
