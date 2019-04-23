
from mongoWrapper import *

# test getting collection
print("getting collection\n")
collec = get_bill_collection('localhost',27017)

# test insertion
print("inserting test object\n")
id = collec.insert_one({'test' : "test text"}).inserted_id
print("printing inserted bill id: ", id)

# delete it
print("deleting ",id)
remove = collec.find_one({ '_id' : id})
collec.delete_one(remove)

bills = get_matching_bills(collec,'115','','','','')
for bill in bills:
  print_bill(bill)