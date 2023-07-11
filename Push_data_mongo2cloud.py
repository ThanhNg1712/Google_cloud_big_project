#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pymongo
from google.cloud import storage
from google.oauth2.service_account import Credentials
import jsonlines
import time
import os

# Connect to MongoDB and retrieve data
def get_mongodb_data(limit=None):
    mongodb_uri = 'mongodb://localhost:27017'
    database_name = 'tiki_product'
    collection_name = 'tiki_data'

    # Connect to the MongoDB server
    client = pymongo.MongoClient(mongodb_uri)
    db = client[database_name]
    collection = db[collection_name]

    # Define projection to exclude certain fields from the query result
    projection = {
        "_id": 0,
        "installment_info_v2": 0,
        "configurable_products": 0,
        "add_on_title": 0,
        "add_on": 0,
        "has_other_fee": 0,
        "badges_new": 0,
        "badges": 0
    }

    # Retrieve data from the collection with optional limit
    if limit:
        data = collection.find({}, projection).limit(limit)
    else:
        data = collection.find({}, projection)

    return data

# Measure the time taken to retrieve data from MongoDB
start_time = time.time()
mongodb_data = get_mongodb_data(limit=50000)
end_time = time.time()
loading_time = end_time - start_time
print(f"time upload from MongoDB: {loading_time} sec")

# Create a temporary JSONL file and write MongoDB data into it
temp_jsonl_file = "temp.json"

start_time = time.time()

with jsonlines.open(temp_jsonl_file, mode='w') as writer:
    for doc in mongodb_data:
        writer.write(doc)

end_time = time.time()
writing_time = end_time - start_time
print(f"time to update record JSONL: {writing_time} sec")

# Set up Google Cloud Storage credentials
#key to upload to google cloud in the file json that download from IAM and admin section with json key type when create service account
#and downloaded in the local host folder in the path below
credentials_path = r"/Users/thanhnguyen/Desktop/Data_analysis/DE_k2/project_5/project5_phase2/mongo_to_gcs_key.json"
credentials = Credentials.from_service_account_file(credentials_path)

# Connect to Google Cloud Storage
client = storage.Client(credentials=credentials)

# Define the bucket and destination blob names
bucket_name = "ggcloud_tiki_project"
destination_blob_name = "tiki_data_test1.json"
# Retrieve the bucket
bucket = client.get_bucket(bucket_name)

# Measure the time taken to upload the JSONL file to Google Cloud Storage
start_time = time.time()

# Create a new blob and upload the JSONL file
blob = bucket.blob(destination_blob_name)
blob.upload_from_filename(temp_jsonl_file, content_type='application/octet-stream')

end_time = time.time()
upload_time = end_time - start_time

# Delete the temporary JSONL file
os.remove(temp_jsonl_file)

print(f"Time to upload Google Cloud Storage: {upload_time} sec")
print(f"Upload completed gs://{bucket_name}/{destination_blob_name}")

