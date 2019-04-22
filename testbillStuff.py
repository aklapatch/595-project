from billStuff import *
import glob, xmltodict

i = 0

# get all hconres xml's
for file in glob.glob('bills/BILLSXML/*hconres*.xml'):
  with open(file,encoding='utf8') as fd:
    xmldict = xmltodict.parse(fd.read())
    i += 1
    print(i, "hconres ")

i = 0 
# get all s xml's
for file in glob.glob('bills/BILLSXML/*s*.xml'):
  with open(file,encoding='utf8') as fd:
    xmldict = xmltodict.parse(fd.read())
    i += 1
    print(i, " s ")
