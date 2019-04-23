
from mongoWrapper import *

# test getting collection
print("getting collection\n")
collec = get_bill_collection('localhost',27017)

# test insertion
print("inserting test object\n")
id = collec.insert_one({'test' : "test text"}).inserted_id
print("printing inserted bill id: ", id)

found = collec.find_one({'_id': ObjectId(id)})

bill = get_bill_from_id(collec, id)
print(bill)

# delete it
print("deleting ",id)
collec.delete_one(found)

found = collec.find_one({'_id': ObjectId(id)})
print(found)

bills = get_matching_bills(collec,'HCON 105 IH','','','','')
for bill in bills:
  print_bill(bill)