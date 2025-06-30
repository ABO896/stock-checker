# Stock Market Checker

This project is a simple stock market checker web application. It allows users to enter a stock symbol, view the current price, change, and related companies (peers).

## Features
- Search for a stock by symbol.
- Display stock information including:
  - Current price.
  - Change in value.
  - Percentage change.
- View a list of related companies (peers).
- Loading spinner while fetching data.
- Error handling for invalid symbols and network issues.

## Requirements
- Python 3.x
- Flask
- Internet connection (for fetching stock data)

## Setup Instructions
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/stock-checker.git
   cd stock-checker
   ```
2. Install dependencies:
   ```bash

   ```
3. Set the `FINNHUB_API_KEY` environment variable with your API key:
   ```bash
   export FINNHUB_API_KEY=YOUR_API_KEY_HERE
   ```
4. Run the Flask application:
   ```bash
   flask run
   ```
5. Open the application in your browser:
   ```
   http://127.0.0.1:5000
   ```

## Environment Variables

Before running the application, make sure to set a `FINNHUB_API_KEY`. The easiest way is to create a `.env` file containing:

```bash
FINNHUB_API_KEY=your_api_key_here
```

You can optionally set `FINNHUB_BASE_URL` to override the default endpoint of `https://finnhub.io/api/v1`.

## Project Structure
```
stock-checker/
├── static/
│   └── styles.css         # CSS for styling
├── templates/
│   └── index.html         # HTML file
├── app.py                 # Flask backend
└── README.md              # Project documentation
```

## Further Development
- Add stock performance graphs using Chart.js.
- Implement user accounts and favorites feature.
- Optimize API calls with caching.

## License
This project is licensed under the MIT License.
