from config import GEMINI_KEY
from agent import get_details_of_users
# def genrate():
#     print("Hello World!")
#     return "Calling the function genrate()"
# response = genrate()
# full_response = "Here is the response: ok " + str(response)
# print(full_response)

# print("GEMINI_KEY:", GEMINI_KEY)    

print(get_details_of_users(2))