import os
import certifi
from dotenv import load_dotenv
from mongoengine import connect, Document, StringField

# Load environment variables
load_dotenv()
MONGO_URI = os.getenv("MONGO_URI")

# Connect to database
connect(host=MONGO_URI, tlsCAFile=certifi.where())

class User(Document):
    email = StringField(required=True, unique=True)
    meta = {
        'collection': 'users',
        'strict': False  # <--- This tells it to ignore the other fields!
    }

def delete_specific_user():
    target = "admin@helpdesk.local"
    
    user = User.objects(email=target).first()
    if user:
        user.delete()
        print(f"✅ Successfully deleted {target} from the database.")
    else:
        print(f"⚠️ Could not find {target} in the database. It may already be deleted.")

if __name__ == "__main__":
    delete_specific_user()