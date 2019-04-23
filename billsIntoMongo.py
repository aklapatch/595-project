from billStuff import *
from mongoWrapper import *
import glob, xmltodict,pymongo

bill_collection = get_bill_collection('localhost',27017)

i = 0 
# get all s xml's
for file in glob.glob('bills/BILLSXML/*.xml'):
  with open(file,encoding='utf8') as fd:
    xmldict = xmltodict.parse(fd.read())
    i += 1
    test = reduce_s_dict(xmldict)
    insert_bill(test,bill_collection)