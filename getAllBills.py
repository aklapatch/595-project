from billStuff import *
from bs4 import BeautifulSoup
import requests
import lxml

def getlinks(url):
    html = requests.get(url)
    bsObj = BeautifulSoup(html.text, 'html.parser')

    links = bsObj.findAll('a')
    for link in links:
      print("here")
      print(link.get('href'))

baseUrl = "https://www.govinfo.gov/bulkdata/BILLS/"

# 116 congress https://www.govinfo.gov/bulkdata/BILLS/116
# 1st session https://www.govinfo.gov/bulkdata/BILLS/116/1

# then you have 
# hconres, hjres, hr, hres, s, sconres, sjres, sres
# and the billes after that.

hconres = "https://www.govinfo.gov/bulkdata/BILLS/116/1/hconres"

getlinks(hconres)
print("done")