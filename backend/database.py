import os
import certifi
from mongoengine import connect
from dotenv import load_dotenv

load_dotenv()
MONGO_URI = os.getenv("MONGO_URI")

def init_db():
    if not MONGO_URI:
        print("❌ Error: MONGO_URI is missing!")
        return
    try:
        connect(host=MONGO_URI, tlsCAFile=certifi.where())
        print("✅ Successfully connected to MongoDB Atlas via MongoEngine")
    except Exception as e:
        print(f"❌ Failed to connect to MongoDB: {e}")