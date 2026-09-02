from config import GEMINI_KEY, BASE_URL

# print("GEMINI_KEY:", GEMINI_KEY)  # Print the API key for verification
# print("BASE_URL:", BASE_URL)  # Print the base URL for verification

from langchain.agents import create_agent  # Create an agent SDK
from langchain_google_genai import (
    ChatGoogleGenerativeAI,
)  # Create a Google Generative AI chat model

import requests
from datetime import datetime, timezone

model = ChatGoogleGenerativeAI(
    model="gemini-3.5-flash-lite",  # Model name
    api_key=GEMINI_KEY,  # API key from config.py
    # temperature=0.2, # Temperature for randomness
    # max_output_tokens=1024, # Maximum output tokens
    # top_p=0.8, # Top-p sampling
    # top_k=40, # Top-k sampling
    # stop=["\n\n"], # Stop sequence
)  # Initialize the Google Generative AI chat model with the specified parameters


def get_details_of_users(user_id: int) -> dict:
    """Get details of a user by user_id from the API."""
    print(f"\n \n \n \n Tool called: {get_details_of_users.__name__} with user_id: {user_id} at {datetime.now(timezone.utc)}\n \n \n")
    api_url = f"{BASE_URL}users/{user_id}"
    response = requests.get(api_url)
    return response.json()

# https://www.mockapi.run/api/comments?userId=20
def get_comments_of_users(user_id: int) -> dict:
    """Get comments of a user by user_id from the API."""
    print(
        f"\n \n \n \n Tool called: {get_comments_of_users.__name__} with user_id: {user_id} at {datetime.now(timezone.utc)}\n \n \n"
    )
    api_url = f"{BASE_URL}comments?userId={user_id}"
    response = requests.get(api_url)
    return response.json()

agent = create_agent(
    model=model,
    system_prompt="You are a helpful assistant",  # System prompt for the agent
    tools=[get_details_of_users, get_comments_of_users],  # List of tools for the agent to use
)

response = agent.invoke(
    {"messages": [{"role": "user", "content": "Give me details of user with id 2 and comments"}]}
)
print(
    "Response:", response["messages"][-1].content[0]["text"]
)  # Print the response from the agent
