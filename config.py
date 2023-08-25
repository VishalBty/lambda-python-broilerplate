from pymongo import MongoClient
import logging
import certifi

MONGO_URL = None
DB_NAME = "something"

client = None
ca = certifi.where()
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def get_mongodb_client():
    global client
    if client is None:
        client = MongoClient(MONGO_URL)
    return client

