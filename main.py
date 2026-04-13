#create tools
from langchain.tools import tool
import requests
import os


@tool
def get_stock_price(symbol: str) -> float:
    """Get the current stock price for a given symbol."""
    url = f"https://api.example.com/stocks/{symbol}/price"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()["price"]
    else:
        raise Exception(f"Failed to get stock price for {symbol}")
