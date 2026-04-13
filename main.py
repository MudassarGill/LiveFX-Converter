#create tools
from langchain.tools import tool
import requests
import os


@tool
def get_conversion_factor(base_currency: str, target_currency: str) -> float:
    """Get the current conversion rate between a given base currency and target currency"""
    url = f"https://v6 exchangerate-api.com/{os.getenv('EXCHANGE_RATE_API_KEY')}/pair/{base_currency}/{target_currency}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()["rate"]
    else:
        raise Exception(f"Failed to get conversion rate for {base_currency} to {target_currency}")
