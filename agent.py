from config import GEMINI_KEY, BASE_URL

from langchain.agents import create_agent  # Create an agent SDK
from langchain_google_genai import (
    ChatGoogleGenerativeAI,
)  # Create a Google Generative AI chat model

import requests
from datetime import datetime, timezone

model = ChatGoogleGenerativeAI(
    model="gemini-3.5-flash-lite",  # Model name
    api_key=GEMINI_KEY,  # API key from config.py
)

# creating dectionary for agent previous response
message_dectionary = {}


def get_messages(user_id: int) -> list:
    """Get the messages from the agent's previous responses."""
    return message_dectionary.get(
        user_id, []
    )  # Return the messages for the given user_id, or an empty list if not found


def set_messages(user_id: int, messages: list) -> None:
    """Set the messages for the agent's previous responses."""
    message_dectionary[user_id] = messages
    return


def get_details_of_users(user_id: int) -> dict:
    """Get details of a user by user_id from the API."""
    print(
        f"\n Tool called: {get_details_of_users.__name__} with user_id: {user_id} at {datetime.now(timezone.utc)} \n"
    )
    api_url = f"{BASE_URL}users/{user_id}"
    response = requests.get(api_url)
    return response.json()


# https://www.mockapi.run/api/comments?userId=20
def get_comments_of_users(user_id: int) -> dict:
    """Get comments of a user by user_id from the API."""
    print(
        f"\n Tool called: {get_comments_of_users.__name__} with user_id: {user_id} at {datetime.now(timezone.utc)} \n"
    )
    api_url = f"{BASE_URL}comments?userId={user_id}"
    response = requests.get(api_url)
    return response.json()


# https://www.mockapi.run/api/posts?userId=20
def get_posts_of_users(user_id: int) -> dict:
    """Get posts of a user by user_id from the API."""
    print(
        f"\n Tool called: {get_posts_of_users.__name__} with user_id: {user_id} at {datetime.now(timezone.utc)} \n"
    )
    api_url = f"{BASE_URL}posts?userId={user_id}"
    response = requests.get(api_url)
    return response.json()


agent = create_agent(
    model=model,
    system_prompt=""" You are a helpful assistant

    you only respond to the user queries related to the user details, comments and posts. otherwise you will respond with "I am sorry, I can only help you with user details, comments and posts."

    """,  # System prompt for the agent
    tools=[
        get_details_of_users,
        get_comments_of_users,
        get_posts_of_users,
    ],  # List of tools for the agent to use
)


def call_agent(user_id: int, user_query: str) -> str:
    """Call the agent with a user query and user_id."""
    build_conversion = get_messages(
        user_id
    )  # Get the previous messages for the user_id

    new_query = {"role": "user", "content": user_query}

    build_conversion.append(new_query)  # Append the new user query to the conversation

    set_messages(user_id, build_conversion)  # Update the messages for the user_id
    response = agent.invoke({"messages": build_conversion})
    answer = response["messages"][-1].content[0]["text"]

    ai_response = {
        "role": "assistant",
        "content": [
            {
                "text": answer,
            }
        ],
    }
    build_conversion.append(
        ai_response
    )  # Append the agent's response to the conversation
    set_messages(user_id, build_conversion)
    print(type(answer))
    return answer  # Return the agent's response


query1 = call_agent(1, "Give me detail of user with id 5")
print(query1)  # Print the response from the agent for user_id 1

query2 = call_agent(1, "summarize all its comments.")
print(query2)  # Print the summarized comments from the agent for user_id 1


# response = agent.invoke(
#     {
#         "messages": [
#             {"role": "user", "content": "Give me detail of user with id 2"},
#             {"role": "assistant", "content": "previous response"},
#             {"role": "user", "content": "summarize all comments."},
#             {"role": "user", "content": "summarize about oop."},
#         ]
#     }
# )
# print(
#     "Response:", response["messages"][-1].content[0]["text"]
# )  # Print the response from the agent
