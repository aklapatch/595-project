from billStuff import *
import glob, xmltodict

i = 0 

# get all hconres xml's
for file in glob.glob('bills/BILLSXML/*s*.xml'):
  with open(file,encoding='utf8') as fd:
    xmldict = xmltodict.parse(fd.read())
    i += 1
    print(i)
    print(reduce_s_dict(xmldict))
