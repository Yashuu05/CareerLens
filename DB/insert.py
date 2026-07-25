from pymongo import MongoClient
from pymongo.server_api import ServerApi
import os 
import sys
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if not project_root in sys.path:
    sys.path.insert(0, project_root)

def create_collection(database_name, collection_name: str):
    """
    - *purpose*: to create a mongodb collection

    - *inputs*:
        1. database_name: name of database to create collection ,
        2. collection_name: name of collection to create. 
    
    - *returns*: a collection
    """
    collection = database_name[collection_name]
    return collection

def add_many_documents(collection, items: list):
    """
    - *purpose*: insert more than one documents in given collection
    - *inputs*:
        1. collection: collection to insert documents
        2. items: list of documents to insert
    """
    collection.insert_many(items)

if __name__ == "__main__":
    print("connecting to database..")
    # Get the database using the method we defined in pymongo_test_insert file
    from DB.create_db import get_database
    dbname = get_database()

    print("creating collection *students*")
    # create collection
    collection = create_collection(database_name=dbname, collection_name="students")

    # insert documents
    print("inserting documents to test database working.")

    personal_info = {
        "first_name" : "Yash",
        "last_name": "Chillal",
        "age" : 20,
        "course" : "computer engineering",
        "degree" : "B.E",
        "country" : "India",
        "selected_domain" : "Data Science"    
    }

    skill_gap = {
        "python" : 0.045,
        "java" : 0.007,
        "javascript" : 0.03,
        "html_css" : 0.021,
        "ml" : 0.13,
    }

    add_many_documents(collection=collection, items=[personal_info, skill_gap])
    print(f"Document added to database {dbname}.")