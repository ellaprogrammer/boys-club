
import variables
import shared
from global_storage import storage_context
from pydantic import BaseModel

from pydantic import BaseModel
from typing import Optional

class User(BaseModel):
  """
  Description
  """
  name: Optional[str]
  phone: str
  # email: Optional[str]
  # sport: Optional[Sport] 
  class Config:
    title = 'Main'

def post(user: User, user_store = storage_context("users")):
  user_store[user.phone] = user.dict()
  return