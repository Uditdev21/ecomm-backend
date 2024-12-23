from pymongo import MongoClient
from pydantic import BaseModel
from typing import Optional
from enum import Enum
from bson import ObjectId
from dotenv import load_dotenv
import os
load_dotenv()
db_url = os.getenv("DBSTRING")
client=MongoClient(db_url)

db = client["ecomm"]

users_collection=db["users"]
prdoducts_collection=db["Products"]
slidshow_collection=db["slidShow"]
catagory_collection=db["category"]
orders_cpollection=db["orders"]

class payment_type(Enum):
    CASH="cash"
    UIP="uip"

class user_status(Enum):
    ADMIN="admin"
    CLIENT="client"

class order_status(Enum):
    PENDING="pending"
    SHIPPED="shipped"
    DELIVERED="delivered"
    CANCELED="canceled"

class imageStruct(BaseModel):
    image_url:str
    image_publicid:str

class productModel(BaseModel):
    Name:str
    Discription:str
    image_small:imageStruct
    image_medium:imageStruct
    image_large:imageStruct
    price:int
    catagory:ObjectId

    class Config:
        arbitrary_types_allowed = True

class userModel(BaseModel):
    uid:str
    email:str
    user_type:user_status
    


# You can add further operations here, like checking a collection
print(f"Connected to database: {db.name}")