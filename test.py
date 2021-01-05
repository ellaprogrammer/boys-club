
import variables
import shared
import sms

def get(greeting):
  sms.send("8185851298", "hello from brev sms")
  return { f"{greeting} brev!" }

from pydantic import BaseModel
from global_storage import storage_context

# type definition of incoming JSON body
class Sport(BaseModel):
  sport1: str
  sport2: str
  sport3: str
  sport4: str
  live: str
  summary: str
  culture: str

class User(BaseModel):
  name: str
  phone: str #
  email: str
  sport: Sport 

# pass it in to function
def post(user: User, user_store = storage_context("users")):
  user_store[user.phone] = user.dict()
  return {
      "status": f"{user.name} says hi!"
  }


