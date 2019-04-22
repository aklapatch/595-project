import urllib.request, json 
with urllib.request.urlopen("https://www.govinfo.gov/bulkdata/json") as url:
    data = json.loads(url.read().decode())
    print(data)