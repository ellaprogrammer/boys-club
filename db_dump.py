
import variables
import shared
from global_storage import storage_context
from pydantic import BaseModel
import json

def get(user_store = storage_context("users"), waitlist_store = storage_context("waitlist")):
  return {json.dumps({ k:v for k,v in user_store.items()}, indent=4)}

def post(user_store = storage_context("users")):
  return {user_store.items()}
