
import variables
import shared
import sms
from typing import Optional
from pydantic import BaseModel
from global_storage import storage_context
from fastapi.responses import JSONResponse
from twilio.rest import Client

# def get(response):
#   if response == "👍": # do we need all the shades?
#     return { f"positive feedback" }
#   elif response == "👎":
#     return { f"negative feedback" }
#   else:
#     return { f"response: {response}!" }

# type definition of incoming JSON body
class Sport(BaseModel):
  sport1: str
  team1: str
  live: str
  summary: str
  culture: str

class User(BaseModel):
  """
  Description
  """
  name: str
  phone: str
  # email: Optional[str]
  # sport: Optional[Sport] 
  class Config:
    title = 'Main'

# POST webhook on website
def post(user: User, user_store = storage_context("users")):
  phone_number = "+1" + str(user.phone) 
  user_store[phone_number] = user.dict()
  client = Client(variables.ACCOUNT_SID, variables.TWILIO_AUTH_TOKEN)
  message = client.messages \
    .create(
        body="Welcome to the BOYS.CLUB, where you get the latest on all things that you’d rather us cover for you. No more boys club talk that keeps you out of the conversation. \n 🥊 Here a few things you can expect from us: \n 🏀 The latest buzz on all things pop culture for featured games, so you know what people are laughing about in your Tuesday morning meetings. \n 🏈 Headlines, close games, and players to know about (yes this will include photos of Jimmy G 🔥). \n ⚽️ Important upcoming dates, so you’re never stuck asking if anyone has weekend plans on the Friday before the Super Bowl (ouch, we’ve all been there). \n ⚾️ Interactive engagement on your side (coming soon!), send us a 👍 or 👎 for a quick pulse check on how our updates are sitting with you, send us ‘MORE’ and if we’ve got it, we’ll send follow up articles or tweets for more info. Reply STOP to unsubscribe at anytime.",
        from_='+14153580188',
        # status_callback='https://9lfthysp.brev.dev/api/signup_welcome',
        to=user.phone
      )

  print(message.sid)
  # sms.send(user.phone, "Welcome to the boysclub.")
  # return {
  #   "status": f"{user.name} says hi!"
  # }
  return JSONResponse(status_code=201, content={"status": f"{user.name} success."})


