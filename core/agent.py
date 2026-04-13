import os
import json
import requests
from dotenv import load_dotenv
from typing import Annotated

from langchain_core.messages import HumanMessage
from langchain.tools import tool
from langchain_core.tools import InjectedToolArg

load_dotenv()

def get_exchange_api_key():
    """Extract exchange API key from env, handling URL format from old setup."""
    raw_key = os.getenv("EXCHANGE_RATE_API_KEY", "")
    if "exchangerate-api.com" in raw_key:
        # e.g., https://v6 exchangerate-api.com/4f9411e6002e5d96dbd4e1cf/pair/EUR/GBP
        parts = raw_key.replace(" ", "/").split('/')
        # Attempt to grab the key part which is typically 24 chars
        for part in parts:
            if len(part) == 24 and str.isalnum(part):
                return part
    return raw_key

EXCHANGE_API_KEY = get_exchange_api_key()

@tool
def get_conversion_factor(base_currency: str, target_currency: str) -> float:
    """Get the current conversion rate between a given base currency and target currency"""
    url = f"https://v6.exchangerate-api.com/v6/{EXCHANGE_API_KEY}/pair/{base_currency}/{target_currency}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Failed to get rate for {base_currency} to {target_currency}. Status: {response.text}")

@tool
def convert(base_currency_value: float, conversion_rate: Annotated[float, InjectedToolArg]) -> float:
    """Convert a given amount from a base currency to a target currency using the conversion rate"""
    return float(base_currency_value) * conversion_rate


def get_llm():
    """Initializes LLM. Tries Groq first, falls back to HuggingFace."""
    if os.getenv("GROQ_API_KEY"):
        try:
            from langchain_groq import ChatGroq
            return ChatGroq(model_name="llama3-8b-8192", temperature=0)
        except Exception as e:
            print(f"Warning: Groq initialization failed ({e}). Falling back to HuggingFace.")
    
    from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
    
    # HuggingFace requires an LLM object passed into ChatHuggingFace
    llm_endpoint = HuggingFaceEndpoint(
        repo_id="meta-llama/Meta-Llama-3.1-8B-Instruct",
        huggingfacehub_api_token=os.getenv("HUGGINGFACE_API_KEY"),
        task="text-generation",
    )
    
    return ChatHuggingFace(llm=llm_endpoint)


def process_chat(query: str) -> str:
    """End-to-end chat processing with tools."""
    llm = get_llm()
    tools = [get_conversion_factor, convert]
    llm_with_tool = llm.bind_tools(tools)
    
    messages = [HumanMessage(content=query)]
    
    ai_message = llm_with_tool.invoke(messages)
    messages.append(ai_message)
    
    if hasattr(ai_message, 'tool_calls') and ai_message.tool_calls:
        conversion_rate = 1.0
        for tool_call in ai_message.tool_calls:
            # Execute get_conversion_factor
            if tool_call['name'] == 'get_conversion_factor':
                tool_msg1 = get_conversion_factor.invoke(tool_call)
                # Parse to save the rate for the next tool
                try:
                    content = tool_msg1.content
                    if isinstance(content, str):
                        content = json.loads(content)
                    conversion_rate = content.get('conversion_rate', 1.0)
                except Exception as e:
                    print(f"Error parsing rate: {e}")
                messages.append(tool_msg1)
                
            # Execute convert tool using the injected rate
            elif tool_call['name'] == 'convert':
                tool_call['args']['conversion_rate'] = conversion_rate
                tool_msg2 = convert.invoke(tool_call)
                messages.append(tool_msg2)
                
        final_response = llm_with_tool.invoke(messages)
        return final_response.content
    
    return ai_message.content
