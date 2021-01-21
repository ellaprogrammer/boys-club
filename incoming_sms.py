import variables
import shared
import sms
from pydantic import BaseModel
from global_storage import storage_context
from twilio.rest import Client
import datetime
from fastapi.responses import JSONResponse
from typing import Optional
import random

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

def existing_user(dict_obj, key):
  if key in dict_obj:
    return True
  else:
    return False

def new_to_waitlist(dict_obj, key):
  if key in dict_obj:
    return False
  else:
    return True

def on_waitlist(dict_obj, key):
  if key in dict_obj:
    return True
  else:
    return False

def unsubcribe_user(dict_obj_waitlist, dict_obj_users, key):
  if key in dict_obj_waitlist:
    del dict_obj_waitlist[key]
  if key in dict_obj_users:
    del dict_obj_users[key]
    

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
def get(ToCountry: str, ToState: str, SmsMessageSid: str, NumMedia: str, ToCity: str, FromZip: str, SmsSid: str, FromState: str, SmsStatus: str, FromCity: str, Body: str, FromCountry: str, To: str, ToZip: str, NumSegments: str, MessageSid: str, AccountSid: str, From: str, ApiVersion: str, incoming_texts_store = storage_context("incoming_texts"), user_store = storage_context("users"), waitlist_store = storage_context("waitlist")):
  # Log everything this user ever sends us.
  add_value_to_responses_dict(incoming_texts_store, From, Body)
  # Set up TWILIO variables.
  client = Client(variables.ACCOUNT_SID, variables.TWILIO_AUTH_TOKEN)
  # Are they on the waitlist still?
  is_not_on_waitlist = new_to_waitlist(waitlist_store, From)
  is_on_waitlist = on_waitlist(waitlist_store, From)
  # Have we seen this user before in our Users table?
  is_existing_user = existing_user(user_store, From)

  # TODO: check if Body == "STOP" and delete them and send a confirmation
  if (Body == 'STOP'):
    unsubcribe_user(waitlist_store, user_store, From)
    message = client.messages \
      .create(
          body="You are now successfully unsubscribed. We appreciate your feedback as we are early on in launching this product, can you share your reason for leaving? After this text, you won't hear from us again but we would appreciate your feedback greatly! Thanks, xx.",
          from_='+14156872582',
          # status_callback='https://9lfthysp.brev.dev/api/signup_welcome',
          to=From
        )
    return "unsubscribed"
  
  waitlist_with_num = f"Welcome to the boys.club waitlist! 🥳\n\nWe’re currently letting users in on a rolling basis and you are currently #{random.randint(29,41)} in line. \n\n🤔 Want to move up in line? \n - Reply to this text with your name \n - Let us know why you signed up \n - Tag us on social @boysclubtext \n\n 🥊 We’ll get back to you soon & let you know when we’re ready to have you join the boysclub. \nReply STOP to unsubscribe at anytime."
  # Was it a signup?
  if is_existing_user:
    message = client.messages \
      .create(
          body="Your message has been received! Thanks for the feedback/info. As we are working on getting more responsive, if you want to get in touch with us, feel free to reach out to ella@boys.club or @boysclubtext on Twitter.",
          from_='+14156872582',
          # status_callback='https://9lfthysp.brev.dev/api/sms',
          to=From
        )
  elif is_not_on_waitlist:
    # Sign up new user, for now with NoName.
    waitlist_store[From] = "NoName"
    # TODO: Send a real waitlist number
    message = client.messages \
      .create(
          body=waitlist_with_num,
          from_='+14156872582',
          # status_callback='https://9lfthysp.brev.dev/api/signup_welcome',
          to=From
        )
  elif is_on_waitlist:
    message = client.messages \
      .create(
          body="Your message has been received! Thanks for the feedback/info. As we are working on getting more responsive, if you want to get in touch with us, feel free to reach out to ella@boys.club or @boysclubtext on Twitter.",
          from_='+14156872582',
          # status_callback='https://9lfthysp.brev.dev/api/sms',
          to=From
        )
  

  return "status: success."




def post(user: User, user_store = storage_context("users")):
  # TODO: this is a fallback method, so update similar logic
  user_store[user.phone] = user.dict()
  client = Client(variables.ACCOUNT_SID, variables.TWILIO_AUTH_TOKEN)
  message = client.messages \
    .create(
        body="Welcome to the BOYS.CLUB, where you get the latest on all things that you’d rather us cover for you. No more boys club talk that keeps you out of the conversation. \n 🥊 Here a few things you can expect from us: \n 🏀 The latest buzz on all things pop culture for featured games, so you know what people are laughing about in your Tuesday morning meetings. \n 🏈 Headlines, close games, and players to know about (yes this will include photos of Jimmy G 🔥). \n ⚽️ Important upcoming dates, so you’re never stuck asking if anyone has weekend plans on the Friday before the Super Bowl (ouch, we’ve all been there). \n ⚾️ Interactive engagement on your side, send us a 👍 or 👎 for a quick pulse check on how our updates are sitting with you, send us ‘MORE’ and if we’ve got it, we’ll send follow up articles or tweets for more info, and of course ‘STOP’ at any time to end your boys.club membership.",
        from_='+14156872582',
        status_callback='https://9lfthysp.brev.dev/api/signup_welcome',
        to=user.phone
      )

  # print(message.sid)
  return JSONResponse(status_code=201, content={"status": f"{user.name} success."})