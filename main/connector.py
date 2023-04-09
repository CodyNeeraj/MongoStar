import os
import random
import threading
import pymongo

# loading the environment variables from a the secrets we created up here in the codespaces configuration
mongo_url = os.environ.get("REMOTE_MONGO_CLUSTER")
 
mongo_connection = pymongo.MongoClient(mongo_url)
mydb = mongo_connection["mydatabase"]

new_collection = mydb["testCollection"]
dictn = { "name": "John", "address": "Highway 37" }
x = new_collection.insert_one(dictn)

NUM_COLLECTIONS = 40
NUM_DOCUMENTS_PER_COLLECTION = 500

# Generate random data for documents
def generate_random_data():
    return {
        'name': ''.join(random.choices('abcdefghijklmnopqrstuvwxyz', k=10)),
        'age': random.randint(18, 65),
        'city': ''.join(random.choices(['New York', 'Los Angeles', 'Chicago', 'Houston'], k=1))
    }

# Function to add documents to a collection
def add_documents_to_collection(collection_name):
    # Connect to MongoDB
    client = pymongo.MongoClient(mongo_url)
    db = client["mydatabase"]
    collection = db[collection_name]
    
    # Add documents to the collection
    for i in range(NUM_DOCUMENTS_PER_COLLECTION):
        document = generate_random_data()
        collection.insert_one(document)
    # Disconnect from MongoDB
    client.close()

# Function to add collections to the database
def add_collections_to_database():
    # Connect to MongoDB
    client = pymongo.MongoClient(mongo_url)
    db = client["mydatabase"]
    
    # Add collections to the database
    for i in range(NUM_COLLECTIONS):
        collection_name = 'collection{}'.format(i)
        db.create_collection(collection_name)
        thread = threading.Thread(target=add_documents_to_collection, args=(collection_name,))
        thread.start()
    
    # Disconnect from MongoDB
    client.close()

# Run the script
if __name__ == '__main__':
    add_collections_to_database()