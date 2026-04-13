#create tools
from langchain.tools import tool
import requests
import os


@tool
def get_conversion_factor(base_currency: str, target_currency: str) -> float:
    """Get the current conversion rate between a given base currency and target currency"""
    url = f"https://v6.exchangerate-api.com/v6/{os.getenv('EXCHANGE_RATE_API_KEY')}/pair/{base_currency}/{target_currency}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Failed to get conversion rate for {base_currency} to {target_currency}")
@tool
def convert(base_currency_value: int, conversion_rate:float) -> float:
    """Convert a given amount from a base currency to a target currency using the conversion rate"""
    return base_currency_value * conversion_rate


print(convert(100, 277.50))
