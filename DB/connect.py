
from pymongo import MongoClient
from pymongo.server_api import ServerApi
import os 

from dotenv import load_dotenv

load_dotenv()
uri = os.getenv("MONGODB_URI")
if uri is None:
    print("No MongoDB URI found.")

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))

# Send a ping to confirm a successful connection
try:
    print("trying to connect to MongoDB")
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")

except Exception as e:
    print(e)
    