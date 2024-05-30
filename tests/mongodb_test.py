import pymongo

"""
Localhost database for now, will migrate to cluster

For start/stop mongodb service on localhost mac: 
brew services start mongodb-community@7.0
brew services stop mongodb-community@7.0
"""
def db_init():
    client = pymongo.MongoClient("mongodb://localhost:27017/")

    local_db = client["hpc_training_raw_local_db"]

    print(client.list_database_names())

if __name__ == "__main__":
    db_init()
