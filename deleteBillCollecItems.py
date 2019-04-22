import pymongo
from mongoWrapper import *

# get the bills collection
bill_collec = get_bill_collection('localhost',27017)

# delete all items
bill_collec.delete_many({})


