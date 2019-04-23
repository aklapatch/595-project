from bson.objectid import ObjectId
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

def get_bill_from_id(mongo_collection, bill_id):
  return mongo_collection.find_one({ '_id': ObjectId(bill_id) })

# return bills with matching fields
def get_matching_bills(mongo_collection, bill_title, bill_date,bill_status, bill_sponsors, bill_text):
  # set up regex with a dict
  search_dict = {}
  if bill_sponsors != '':
    search_dict['sponsors'] = {'$regex':'.*'+ bill_sponsors + '.*' }
  
  if bill_title != '':
    search_dict['title'] = {'$regex':'.*'+ bill_title+ '.*' }
  
  if bill_date != '':
    search_dict['date'] = {'$regex':'.*'+ bill_date+ '.*' }

  if bill_status != '':
    search_dict['status'] = {'$regex':'.*'+ bill_status+ '.*' }

  if bill_text != '':
    search_dict['text'] = {'$regex': '.*'+ bill_text+ '.*' }

  return mongo_collection.find(search_dict)

def print_bill(bill_dict):

  if 'title' in bill_dict:
    print('\nTitle: ')
    print(bill_dict['title'])

  if 'date' in bill_dict:
    print('\nDate: ')
    print(bill_dict['date'])
    
  if 'status' in bill_dict:
    print('\nStatus: ')
    print(bill_dict['status'])
    
  if 'sponsors' in bill_dict:
    print('\nSponsors: ')
    print(bill_dict['sponsors'])

  if 'text' in bill_dict:
    print('\nText: ')
    print(bill_dict['text'])