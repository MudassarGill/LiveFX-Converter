#create tools
from langchain_core.messages import HumanMessage
from langchain.tools import tool
from langchain_groq import ChatGroq
from langchain_huggingface import ChatHuggingFace
from langchain_core.tools import InjectedToolArg
from langchain_core.messages import HumanMessage,AIMessage
from typing import Annotated
from dotenv import load_dotenv
import requests
import os
import json

load_dotenv()

@tool
def get_conversion_factor(base_currency: str, target_currency: str) -> float:
    """Get the current conversion rate between a given base currency and target currency"""
    url = f"https://v6.exchangerate-api.com/v6/{os.getenv('HUGGINGFACE_API_KEY')}/pair/{base_currency}/{target_currency}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Failed to get conversion rate for {base_currency} to {target_currency}")
@tool
def convert(base_currency_value: int, conversion_rate:Annotated[float, InjectedToolArg]) -> float:
    """Convert a given amount from a base currency to a target currency using the conversion rate"""
    return base_currency_value * conversion_rate


#tool binding

llm=ChatHuggingFace(
    model_name="meta-llama/Meta-Llama-3.1-8B-Instruct",
    temperature=0,
    api_key=os.getenv("HUGGINGFACE_API_KEY")
)

llm_with_tool=llm.bind_tools([get_conversion_factor, convert])

#tool calling

messages=[HumanMessage('what is the conversion rate between USD and PKR? , and base on that can you convert 10 usd to pkr? ')]

ai_message=llm_with_tool.invoke(messages)
messages.append(ai_message)

for tool_call in ai_message.tool_calls:
    if tool_call['name']=='get_conversion_factor':
        tool_message1=get_conversion_factor.invoke(tool_call)
        converion_rate=json.loads(tool_message1.content)['conversion_rate']
        messages.append(tool_message1)
    if tool_call['name']=='convert':
        tool_call['args']['conversion_rate']=converion_rate
        tool_message2=convert.invoke(tool_call)
        messages.append(tool_message2)
final_response=llm_with_tool.invoke(messages)
print(final_response.content)
