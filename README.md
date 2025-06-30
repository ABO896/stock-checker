# Stock Market Checker

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.10%2B-blue)](#requirements)

A lightweight Flask application for checking stock prices and related market information using the [Finnhub](https://finnhub.io/) API. It provides a web interface to search for symbols, view peers, basic financial metrics and the latest news.

## Table of Contents
- [Features](#features)
- [Quick Start](#quick-start)
- [Environment Variables](#environment-variables)
- [Usage](#usage)
- [Tests](#tests)
- [Project Structure](#project-structure)
- [Deployment](#deployment)
- [Contributing](#contributing)
- [License](#license)

## Features
- Autocomplete search for stock symbols
- Display current price, daily change and percentage change
- Show related companies (peers)
- Present basic financial metrics
- Fetch recent company news and earnings surprises
- API caching to reduce network calls
- Simple HTML/CSS front‑end with accessible design

## Quick Start
Clone the repository and install the dependencies:
```bash
git clone https://github.com/yourusername/stock-checker.git
cd stock-checker
pip install -r requirements.txt
```

Create a `.env` file with your [Finnhub API key](https://finnhub.io/):
```bash
FINNHUB_API_KEY=your_api_key_here
# FINNHUB_BASE_URL=https://finnhub.io/api/v1  # optional
```

Run the application using Flask:
```bash
flask --app app run
```
Then open <http://127.0.0.1:5000> in your browser.

## Environment Variables
The application relies on the following variables:
- `FINNHUB_API_KEY` (required) – your Finnhub API token.
- `FINNHUB_BASE_URL` (optional) – override the base URL of the API.
- `CACHE_TTL` (optional) – cache time‑to‑live in seconds (default: `60`).

## Usage
The web interface is the easiest way to interact with the app, but you can also query the JSON endpoints directly:

- `/search?query=AAPL` – symbol autocomplete.
- `/market-status?exchange=US` – current market status.
- `/stock?symbol=AAPL` – core stock information and peers.
- `/company-news?symbol=AAPL&from=2025-01-01&to=2025-01-31` – recent news.
- `/earnings?symbol=AAPL&limit=4` – quarterly earnings surprises.

Results are returned as JSON and used by the front‑end.

## Tests
Run the unit tests with `pytest`:
```bash
pytest -q
```
All tests should pass without needing a real API key because network calls are mocked.

## Project Structure
```
stock-checker/
├── app.py            # Flask application
├── static/           # CSS styles
├── templates/        # HTML templates
├── tests/            # Pytest suite
├── requirements.txt  # Python dependencies
└── vercel.json       # Configuration for Vercel deployment
```

## Deployment
The project includes a `vercel.json` file for deploying to [Vercel](https://vercel.com/). Make sure to add `FINNHUB_API_KEY` (and optionally `FINNHUB_BASE_URL`) as environment variables in your Vercel project settings.

## Contributing
Contributions are welcome! Please open an issue or submit a pull request. Make sure your changes are covered by tests and pass `pytest` before sending a PR.

## License
This project is licensed under the [MIT License](LICENSE).
