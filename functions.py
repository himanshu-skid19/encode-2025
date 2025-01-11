import json
from datetime import datetime, timedelta
import asyncio
from model import *
from web_search import web_agent

async def web_agent(params):
    print("params passed to web_agent", params)
    web_agent.print_response(params, stream=True)

# Function definitions that will be sent to the Voice Agent API
FUNCTION_DEFINITIONS = [
    
      {
        "name": "web_agent",
        "description": """Use this function to perform web searches when you need to gather up-to-date information or details about a specific topic, business, or any other relevant queries that a customer ask and you are not aware of.
        After initiating this function, you must follow up with a specific search request to retrieve the required data.""",
        "parameters": {
          "type": "object",
          "properties": {
            "message_type": {
              "type": "string",
              "description": "Type of search message to initiate. Use 'lookup' when searching for specific information, or 'general' for a broad search.",
              "enum": ["lookup", "general"]
            },
            "query": {
              "type": "string",
              "description": "The search term or query you want the web search agent to look up.",
              "minLength": 1
            }
          },
          "required": ["message_type", "query"]
        }
      }
    
]


# Map function names to their implementations
FUNCTION_MAP = {
    "web_agent": web_agent,
}