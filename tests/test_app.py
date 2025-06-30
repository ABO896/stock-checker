import os

# Ensure the API key is set before importing the app
os.environ.setdefault("FINNHUB_API_KEY", "testkey")

import sys
from pathlib import Path
from unittest.mock import patch, Mock

# Ensure the project root is on the Python path so ``app`` can be imported
ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from app import app as flask_app


def create_mock_response(json_data, status=200):
    mock_resp = Mock()
    mock_resp.status_code = status
    mock_resp.json.return_value = json_data
    mock_resp.raise_for_status = Mock()
    return mock_resp


def test_get_stock_valid_symbol():
    client = flask_app.test_client()

    def mock_get(url, params=None, **kwargs):
        if url.endswith('/quote'):
            return create_mock_response({'c': 150.0, 'd': 2.5, 'dp': 1.7})
        elif url.endswith('/stock/peers'):
            return create_mock_response(['AAPL', 'GOOGL'])
        elif url.endswith('/stock/profile2'):
            return create_mock_response({'name': 'Test Corp'})
        elif url.endswith('/stock/metric'):
            return create_mock_response({'metric': {'52WeekHigh': 200, '52WeekLow': 100}})
        else:
            raise ValueError(f'Unexpected URL {url}')

    with patch('app.requests.get', side_effect=mock_get):
        response = client.get('/stock', query_string={'symbol': 'TEST'})

    assert response.status_code == 200
    data = response.get_json()
    assert data['symbol'] == 'TEST'
    assert data['company_name'] == 'Test Corp'
    assert data['current_price'] == 150.0
    assert data['peers'] == ['AAPL', 'GOOGL']
    assert data['financials']['52WeekHigh'] == 200


def test_get_stock_missing_symbol():
    client = flask_app.test_client()
    response = client.get('/stock')
    assert response.status_code == 400
    data = response.get_json()
    assert 'No stock symbol' in data['error']


def test_get_stock_invalid_symbol():
    client = flask_app.test_client()

    def mock_get(url, params=None, **kwargs):
        if url.endswith('/quote'):
            return create_mock_response({'c': 0})
        else:
            raise ValueError(f'Unexpected URL {url}')

    with patch('app.requests.get', side_effect=mock_get):
        response = client.get('/stock', query_string={'symbol': 'BAD'})

    assert response.status_code == 404
    data = response.get_json()
    assert 'Invalid stock symbol' in data['error']


def test_search_valid_query():
    client = flask_app.test_client()

    def mock_get(url, params=None, **kwargs):
        if url.endswith('/search'):
            return create_mock_response({'result': [{'symbol': 'AAPL', 'description': 'Apple Inc.'}]})
        else:
            raise ValueError(f'Unexpected URL {url}')

    with patch('app.requests.get', side_effect=mock_get):
        response = client.get('/search', query_string={'query': 'apple'})

    assert response.status_code == 200
    data = response.get_json()
    assert data['results'][0]['symbol'] == 'AAPL'


def test_search_missing_query():
    client = flask_app.test_client()
    response = client.get('/search')
    assert response.status_code == 400


def test_market_status():
    client = flask_app.test_client()

    def mock_get(url, params=None, **kwargs):
        if url.endswith('/stock/market-status'):
            return create_mock_response({'exchange': 'US', 'isOpen': True, 'session': 'regular'})
        else:
            raise ValueError(f'Unexpected URL {url}')

    with patch('app.requests.get', side_effect=mock_get):
        response = client.get('/market-status')

    assert response.status_code == 200
    data = response.get_json()
    assert data['isOpen'] is True


def test_company_news():
    client = flask_app.test_client()

    def mock_get(url, params=None, **kwargs):
        if url.endswith('/company-news'):
            return create_mock_response([
                {'headline': 'News 1', 'url': 'http://example.com'}
            ])
        else:
            raise ValueError(f'Unexpected URL {url}')

    with patch('app.requests.get', side_effect=mock_get):
        response = client.get('/company-news', query_string={
            'symbol': 'AAPL', 'from': '2025-01-01', 'to': '2025-01-31'
        })

    assert response.status_code == 200
    data = response.get_json()
    assert data[0]['headline'] == 'News 1'


def test_earnings():
    client = flask_app.test_client()

    def mock_get(url, params=None, **kwargs):
        if url.endswith('/stock/earnings'):
            return create_mock_response([
                {
                    'symbol': 'AAPL',
                    'period': '2024-12-31',
                    'actual': 2.1,
                    'estimate': 2.0,
                    'surprise': 0.1,
                }
            ])
        else:
            raise ValueError(f'Unexpected URL {url}')

    with patch('app.requests.get', side_effect=mock_get):
        response = client.get('/earnings', query_string={'symbol': 'AAPL', 'limit': '1'})

    assert response.status_code == 200
    data = response.get_json()
    assert data[0]['symbol'] == 'AAPL'
