#create tools
from langchain_core.messages import HumanMessage
from langchain.tools import tool
from langchain_groq import ChatGroq
from dotenv import load_dotenv
import requests
import os

load_dotenv()

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


#tool binding

llm=ChatGroq(
    model_name="llama-3.3-70b-versatile",
    temperature=0,
    api_key=os.getenv("GROQ_API_KEY")
)

llm_with_tool=llm.bind_tools([get_conversion_factor, convert])

#tool calling

messages=[HumanMessage('what is the conversion rate between USD and PKR? , and base on that can you convert 10 usd to pkr? ')]

ai_message=llm_with_tool.invoke(messages)

print(ai_message)
