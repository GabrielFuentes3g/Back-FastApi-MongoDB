import certifi
import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

conn = MongoClient(
    os.environ.get('MONGO_URI'),
    tlsCAFile=certifi.where()
)

db = conn["mydb"]



