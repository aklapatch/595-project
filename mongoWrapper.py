
from pymongo import MongoClient
import pprint
import json
import datetime

# returns the mongodb collection with the name 'bills' from the database 'project'
def get_bill_collection(hostname, portnum):
  client = MongoClient(hostname,portnum)
  return client.project.bills
  
# inserts the billDict python dictionary into the mongodb collection specified by
# mongoCollec
def insert_bill(billDict, mongoCollec):
  return mongoCollec.insert_one(billDict).inserted_id
