import variables
import shared
import sms
from pydantic import BaseModel
from global_storage import storage_context
from twilio.rest import Client
import datetime
from fastapi.responses import JSONResponse
from typing import Optional

def add_value_to_responses_dict(dict_obj, key, value):
    # Check if key exist in dict or not
    if key in dict_obj:
        # Key exist in dict.
        # Check if type of value of key is list or not
        if not isinstance(dict_obj[key], list):
            # If type is not list then make it list
            dict_obj[key] = [dict_obj[key]]
        # Append the value in list
        dict_obj[key].append("DATE/TIME: " + str(datetime.datetime.now()) + " BODY: " + value)
    else:
        # As key is not in dict,
        # so, add key-value pair and add them to Users dict
        dict_obj[key] = str(datetime.datetime.now()) + value

def new_user(dict_obj, key):
  if key in dict_obj:
    return False
  else:
    return True
    

class IncomingText(BaseModel):
  ToCountry: str
  ToState: str
  SmsMessageSid: str
  NumMedia: str
  ToCity: str
  FromZip: str
  SmsSid: str
  FromState: str
  SmsStatus: str
  FromCity: str
  Body: str
  FromCountry: str
  To: str
  ToZip: str
  NumSegments: str
  MessageSid: str
  AccountSid: str
  From: str
  ApiVersion: str

class User(BaseModel):
  """
  Description
  """
  name: Optional[str]
  phone: Optional[str]
  # email: Optional[str]
  # sport: Optional[Sport] 
  class Config:
    title = 'Main'

# Hook for incoming texts
def get(ToCountry: str, ToState: str, SmsMessageSid: str, NumMedia: str, ToCity: str, FromZip: str, SmsSid: str, FromState: str, SmsStatus: str, FromCity: str, Body: str, FromCountry: str, To: str, ToZip: str, NumSegments: str, MessageSid: str, AccountSid: str, From: str, ApiVersion: str, incoming_texts_store = storage_context("incoming_texts"), user_store = storage_context("users")):
  add_value_to_responses_dict(incoming_texts_store, From, Body)
  client = Client(variables.ACCOUNT_SID, variables.TWILIO_AUTH_TOKEN)
  is_new_user = new_user(user_store, From)

  # Was it a signup?
  if is_new_user:
    # sign up new user
    user_store[From] = "NoName"
    message = client.messages \
      .create(
          body="Welcome to the BOYS.CLUB, where you get the latest on all things that you’d rather us cover for you. No more boys club talk that keeps you out of the conversation. \n 🥊 Here a few things you can expect from us: \n 🏀 The latest buzz on all things pop culture for featured games, so you know what people are laughing about in your Tuesday morning meetings. \n 🏈 Headlines, close games, and players to know about (yes this will include photos of Jimmy G 🔥). \n ⚽️ Important upcoming dates, so you’re never stuck asking if anyone has weekend plans on the Friday before the Super Bowl (ouch, we’ve all been there). \n ⚾️ Interactive engagement on your side, send us a 👍 or 👎 for a quick pulse check on how our updates are sitting with you, send us ‘MORE’ and if we’ve got it, we’ll send follow up articles or tweets for more info, and of course ‘STOP’ at any time to end your boys.club membership.",
          from_='+14153580188',
          # status_callback='https://9lfthysp.brev.dev/api/signup_welcome',
          to=From
        )
  # Or feedback?
  else:
    message = client.messages \
      .create(
          body="Thanks for the feedback, we are currently in Beta mode and working on getting more responsive. For questions or concerns, feel free to reach out to ella@boys.club or @boysclubtext on Twitter.",
          from_='+14153580188',
          # status_callback='https://9lfthysp.brev.dev/api/sms',
          to=From
        )

  return "status: success."




def post(user: User, user_store = storage_context("users")):
  user_store[user.phone] = user.dict()
  client = Client(variables.ACCOUNT_SID, variables.TWILIO_AUTH_TOKEN)
  message = client.messages \
    .create(
        body="Welcome to the BOYS.CLUB, where you get the latest on all things that you’d rather us cover for you. No more boys club talk that keeps you out of the conversation. \n 🥊 Here a few things you can expect from us: \n 🏀 The latest buzz on all things pop culture for featured games, so you know what people are laughing about in your Tuesday morning meetings. \n 🏈 Headlines, close games, and players to know about (yes this will include photos of Jimmy G 🔥). \n ⚽️ Important upcoming dates, so you’re never stuck asking if anyone has weekend plans on the Friday before the Super Bowl (ouch, we’ve all been there). \n ⚾️ Interactive engagement on your side, send us a 👍 or 👎 for a quick pulse check on how our updates are sitting with you, send us ‘MORE’ and if we’ve got it, we’ll send follow up articles or tweets for more info, and of course ‘STOP’ at any time to end your boys.club membership.",
        from_='+14153580188',
        status_callback='https://9lfthysp.brev.dev/api/signup_welcome',
        to=user.phone
      )

  # print(message.sid)
  return JSONResponse(status_code=201, content={"status": f"{user.name} success."})