import pandas as pd
from pymongo import MongoClient
import hashlib

mongoURI = 'mongodb+srv://actedcone:dualipa@atlascluster.t9cnxbb.mongodb.net/?retryWrites=true&w=majority&appName=AtlasCluster'
client = MongoClient(mongoURI)
db = client.ENCODE
collection = db.surveys

sheet_id = "1pYf3NbaqnUOl25UMLokWejQT_jBLQwGnhR3cHfrf8OA"
csv_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv"

data = pd.read_csv(csv_url)
records = data.to_dict("records")
new_entries = []

for record in records:
    record_hash = hashlib.md5(str(record).encode()).hexdigest()
    if not collection.find_one({"_id": record_hash}):
        record["_id"] = record_hash
        new_entries.append(record)

if new_entries:
    collection.insert_many(new_entries)
    print(f"{len(new_entries)} new entries added to MongoDB.")
else:
    print("No new entries found.")
