from getBillsXML import *
from mongoWrapper import *

billcollec = getBillCollection('localhost',27017)

# hjres : house joint resoultion
# hconres: house con

# congress joint resolution https://www.govinfo.gov/bulkdata/BILLS/116/1/hjres/BILLS-116hjres10ih.xml

# 


bills = getXMLfrom("https://www.govinfo.gov/bulkdata/BILLS/116/1/s/BILLS-116s1000is.xml")

print(bills)

billcollec.insert_one(bills)