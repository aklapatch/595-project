import requests, xmltodict

def getXMLfrom(URL):
  response = requests.get(URL)
  return xmltodict.parse(response.content)



# get all the bi