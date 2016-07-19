from pymongo import  MongoClient
import gridfs

class MongoConnector:

    def __init__(self, host):
        self.client = MongoClient(host=host)
        self.storage_db = self.client.storage_db
        self.meta_collection = self.storage_db.meta
        self.fs = gridfs.GridFS(self.storage_db)
