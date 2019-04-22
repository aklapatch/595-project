
from pymongo import MongoClient
import pprint
import json
import datetime

# returns the mongodb collection with the name 'bills' from the database 'project'
def getBillCollection(hostname, portnum):
  client = MongoClient(hostname,portnum)
  return client.project.bills
  
# inserts the billDict python dictionary into the mongodb collection specified by
# mongoCollec
def insertBill(billDict, mongoCollec):
  return mongoCollec.insert_one(billDict).inserted_id

# constructs bill dictionary from these parameters
# votedate should be a datetime object of some sort
# mongodb has an id built in for every item so we do 
# not need to use one here
def createBill(name, description, text, status, sponsors, votedate):
  return { "name" : name , "description" : description, "text": text, "status":status, "sponsors":sponsors, "votedate": votedate}