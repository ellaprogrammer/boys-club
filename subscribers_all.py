

import variables
import shared
import sms
from fastapi.responses import JSONResponse
from twilio.rest import Client
from typing import Optional
from pydantic import BaseModel
from global_storage import storage_context

def get(greeting):
  # sms.send("8185851298", "hello from brev sms")
  return { f"{greeting} brev!" }


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

def post(user: User, user_store = storage_context("users")):
  user_store[user.phone] = user.dict()
  client = Client(variables.ACCOUNT_SID, variables.TWILIO_AUTH_TOKEN)
  # Send to everyone in users Collection.
  for user_id in user_store:
    message = client.messages \
      .create(
          body="membership.",
          from_='+14153580188',
          to=user_store[user_id]["phone"]
      )

  print(message.sid)
  # sms.send(user.phone, "Welcome to the boysclub.")
  # return {
  #   "status": f"{user.name} says hi!"
  # }
  return JSONResponse(status_code=201, content={"status": f"success."})


