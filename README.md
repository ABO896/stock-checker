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
   git clone https://github.com/yourusername/stockmarketchecker.git
   cd stockmarketchecker
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
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

## Project Structure
```
stockmarketchecker/
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
