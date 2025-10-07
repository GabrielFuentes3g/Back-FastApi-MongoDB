import certifi
from pymongo import MongoClient

conn = MongoClient(
    "mongodb+srv://gabrielfuentes:20195263@clusterfastapi.zvsrar2.mongodb.net/MyEcomersDB?retryWrites=true&w=majority&appName=ClusterFastApi",
    tlsCAFile=certifi.where()
)

db = conn["mydb"]