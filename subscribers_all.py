

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
  name: Optional[str]
  phone: Optional[str]
  # email: Optional[str]
  # sport: Optional[Sport] 
  class Config:
    title = 'Main'

def post(user: User, user_store = storage_context("users")):
  user_store[user.phone] = user.dict()
  client = Client(variables.ACCOUNT_SID, variables.TWILIO_AUTH_TOKEN)
  # Send to everyone in users Collection.
  # for user_id in user_store:
  message = client.messages \
    .create(
        body="Oh no! Looks like your carrier is rejecting some of our texts. Try to add us as a contact to help prevent this. "
        # body="March Madness continues on after a WILD ending of what is known as the ‘Elite 8’ last night. If you want to learn more about how March Madness works and understand the tournament you can watch this 3 minute video: https://youtu.be/BLDb8sK95PE \n\nHighlights from yesterday evening include: \n\n🏀 #11 UCLA beating #1 University of Michigan by 2 points. People will most likely be talking about the “air-ball” at the end. You can say something like “Well what about the layup right after?” Here is context: https://youtu.be/0m18O---QyU \n\n🏀 Also included in Women’s NCAA, University of Connecticut going to the Final 4 AGAIN. They are the most dominant team in Women’s basketball history with 11 Championships, including 4 championships in a row from ’13 to ’16, and hold the two longest winning streaks in NCAA (both men’s and women’s) history. \n\n🏀 Finally, always remember that players are NOT allowed to accept any financial payments while playing for the NCAA under any circumstances while this tournament generates $1.1 Billion in revenue. Many argue that players are exploited for their likeliness and deserve a share of the money they generate! We’ll save that for another time ;) \n\nWhat to know: The final four resumes this Saturday and the winners will advance to the championship. Pick a school, learn some players' names, and enjoy March Madness! ⛹️‍♀️⛹️‍♂️ \n\nReminder: March Madness is only for college basketball and not the NBA.",
        from='+14156872582',
        # to=user_store[user_id]["phone"]
        to="+1"
    )

  # print(message.sid)
  # sms.send(user.phone, "Welcome to the boysclub.")
  # return {
  #   "status": f"{user.name} says hi!"
  # }
  return JSONResponse(status_code=201, content={"status": f"success."})


