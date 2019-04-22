
from mongoWrapper import *

# test getting collection
print("getting collection\n")
collec = getBillCollection('localhost',27017)

# test insertion
print("getting test bill\n")
testBill = createBill("Test name", "test description", "text for bill", "in recview", "sponsor1", datetime.datetime.now())

print("inserting test bill\n")
id = collec.insert_one(testBill).inserted_id
print("printing inserted bill id: ", id)


# get a docuement with an e in the name
doc = collec.find_one({"name" : {"$regex": ".*e.*" } })

# get all documents
docs = collec.find({"name" : {"$regex": ".*e.*" } })
print("these are all documents with e in the name")
for elem in docs:
    print(elem)

# delete it
print("deleting ",doc)
collec.delete_one(doc)