from pymongo import MongoClient
from bson.objectid import ObjectId

client = MongoClient("localhost", 27017, maxPoolSize=50)
db = client.mtga
collection = db['decks']
cursor = collection.find({})

i = 0
for document in cursor:
    collection.update({'_id': ObjectId(document['_id'])}, {"$set": {'Inc_id': i}})
    i += 1


collection = db['cards']
cursor = collection.find({})

i = 0
for document in cursor:
    collection.update({'_id': ObjectId(document['_id'])}, {"$set": {'Inc_id': i}})
    i += 1

