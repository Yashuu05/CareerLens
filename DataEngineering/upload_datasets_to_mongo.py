import os
import pandas as pd
from DB.create_db import get_database

def upload_csv_to_mongo():
    # Get the MongoDB database instance using your existing connection module
    db = get_database()
    
    # Directory where the datasets were extracted by your tests.py script
    data_dir = "SkillGap\DataSource"
    
    # Map the CSV filenames to the target MongoDB collection names
    collections_mapping = {
        "category_weights.csv": "category_weights",
        "domain_skill_weights.csv": "domain_skill_weights",
        "domains.csv": "domains",
        "skill_requirement.csv": "skill_requirements"
    }
    
    for filename, collection_name in collections_mapping.items():
        file_path = os.path.join(data_dir, filename)
        
        if not os.path.exists(file_path):
            print(f"[!] File not found: {file_path}. Please make sure you have run the download script first.")
            continue
            
        print(f"Processing {filename}...")
        try:
            # Read CSV into a Pandas DataFrame
            df = pd.read_csv(file_path)
            
            # Convert the DataFrame to a list of dictionaries (JSON-like objects)
            records = df.to_dict('records')
            
            if not records:
                print(f"[-] {filename} has no data. Skipping...")
                continue
                
            # Select the collection (creates it automatically if it doesn't exist)
            collection = db[collection_name]
            
            # OPTIONAL: Drop the collection first to avoid duplicating data if run multiple times
            collection.drop()
            print(f"    -> Cleared old data in collection '{collection_name}'.")
            
            # Insert the records into MongoDB
            collection.insert_many(records)
            print(f"    -> [SUCCESS] Inserted {len(records)} records into '{collection_name}' collection.\n")
            
        except Exception as e:
            print(f"    -> [ERROR] Failed processing {filename}: {e}\n")

if __name__ == "__main__":
    print("Starting data migration to MongoDB Atlas...\n")
    upload_csv_to_mongo()
    print("Migration complete!")
