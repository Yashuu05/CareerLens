from pymongo import MongoClient
from pymongo.server_api import ServerApi
import os 
from dotenv import load_dotenv

load_dotenv()
uri = os.getenv("MONGODB_URI")
if uri is None:
    print("No MongoDB URI found.")

def get_database():
    # Create a new client and connect to the server
    client = MongoClient(uri, server_api=ServerApi('1'))
    return client['careerlens']

if __name__ == "__main__":
    dbname = get_database()