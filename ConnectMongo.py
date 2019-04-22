from pymongo import MongoClient
import pprint
import json

import datetime


client = MongoClient()

client = MongoClient('localhost', 27017)

db = client.play

# insert a document
post = {"name" : "First", "OtherData" : datetime.datetime(1990, 8, 7,0,0) }

print(post['name'])
data = post
collec = db.playCollection
post_id = collec.insert_one(data).inserted_id