import requests
from loginFunctions import *

serverName= r'DESKTOP-F54A5DR\SQLEXPRESS'
dbName= r"ProjectTEst"

msSQLConnection=get_database_connection(serverName, dbName)
cursor = msSQLConnection.cursor()

def query_cursor(query_str,cursor):
  try:
    cursor.execute(query_str)
    return cursor.fetchall()
  except:
    return -1

'''
need:
* first and last name
* DOB
* gender
* party
* phoneNum
* email
* state
* district
* majority or minority speaker
'''

def getNumfromstr(string):
  output = ""
  for char in string:
    if char.isdigit():
      output +=char

  return output

def reduceAPIDictCongress(official,district):
  output_dict = {}

  if official['name'] == 'VACANT':
    return -1

  name_str = official['name'].split()
  # grab the first name
  output_dict['fname'] = name_str[0]
  output_dict['lname'] = name_str[-1]
  output_dict['district'] = str(district)

  if  official['party'].find('Republican') > -1:
    output_dict['party'] = 'R'
  elif official['party'].find('Democrat') > -1:
    output_dict['party'] = 'D'
  else:
    output_dict['party'] = 'I'

  output_dict['active'] = 1

  output_dict['phone'] = getNumfromstr(official['phones'][0])

  return output_dict

# google civic api key
# AIzaSyDJhTq7lWewiNgrT7TN10v8osTPN5Lk83M
key = "AIzaSyDJhTq7lWewiNgrT7TN10v8osTPN5Lk83M"
base_url="https://www.googleapis.com/civicinfo/v2/representatives/"
ocd_id_start="ocd-division%2Fcountry%3Aus%2Fstate%3A"
ocd_id_end="?levels=country&recursive=true&roles=legislatorLowerBody&key=" + key

states = ['AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA', 'HI', 'ID',
 'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 'MD', 'MA', 'MI', 'MN', 'MS', 'MO',
 'MT', 'NE', 'NV', 'NH', 'NJ', 'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'PA',
 'RI', 'SC', 'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WI','WY' ]
full_sates= ['Alabama','Alaska','Arizona','Arkansas','California','Colorado','Connecticut',
'Delaware','Florida','Georgia','Hawaii','Idaho','Illinois','Indiana','Iowa','Kansas','Kentucky',
'Louisiana','Maine','Maryland','Massachusetts','Michigan','Minnesota','Mississippi','Missouri',
'Montana','Nebraska','Nevada','New Hampshire','New Jersey','New Mexico','New York','North Carolina',
'North Dakota','Ohio','Oklahoma','Oregon','Pennsylvania','Rhode Island','South Carolina','South Dakota',
'Tennessee','Texas','Utah','Vermont','Virginia','Washington','West Virginia','Wisconsin','Wyoming']

populations = [4858979,	738432,	6828065,	2978204,	39144818,	5456574,	3590886,	945934,	20271272,
	10214860,	1431603,	1654930,	12859995,	6619680,	3123899,	2911641,	4425092,	4670724,	1329328,
	6006401,	6794422,	9922576,	5489594,	2992333,	6083672,	1032949,	1896190,	2890845,	1330608,
	8958013,	2085109,	19795791,	10042802,	756927,	11613423,	3911338,	4028977,	12802503,	1056298,
	4896146,	858469,	6600299,	27469114,	2995919,	626042,	8382993,	7170351,	1844128,	5771337,	586107 ]

districts = [ 	7,	1, 	9, 	4, 	53, 	7, 	5, 	1, 	27, 	14, 	2, 	2, 	18, 	9, 	4,	4, 	6, 	6, 	2, 	8, 	9,
 	14,  8, 	4, 	8, 	1, 	3, 	4, 	2, 	12, 	3, 	27, 	13, 	1, 	16, 	5, 	5, 	18, 	2, 	7, 	1, 	9, 	36, 	4,
 	1, 	11, 	10, 	3, 	8, 	1]


# check state number
num_results = query_cursor("select count(stateID) from State",cursor)
if num_results[0][0] < 50:
  print('reinserting states')
  # delete sates before adding the again
  query_cursor("delete from State",cursor)

  # insert states
  i = 0
  while i < len(full_sates):
    query = "insert into state values(" + str(i) + ",\'" + full_sates[i] + "\'," + str(populations[i]) + "," +str(districts[i]) + ");"
    
    cursor.execute(query)
    i+=1
  cursor.commit()


# check representative number
num_results = query_cursor("select count(employeeID) from employee",cursor)
if num_results[0][0] < 300:
  print('inserting representatives')
  query_cursor("delete from employee",cursor)
  query_cursor("delete from representative",cursor)
  cursor.commit()

  # convert to lowercase
  i = 0
  req_urls = [None] * len(states)
  while i < len(states):
    states[i] = states[i].lower()
    req_urls[i] = base_url + ocd_id_start + states[i] + ocd_id_end
    i+=1

  reps = [None]*500

  id = 0
  i = -1
  for url in req_urls:
    request = requests.get(url)
    i+=1
    if request.status_code == 200:
      tset_dict = request.json()
      officials = tset_dict['officials']

      district=1
      for official in officials:
        id+=1
        output_dict = reduceAPIDictCongress(official,district)

        if isinstance(output_dict,dict):
          #                                         id                    lname                           fname                  dob  gender  party               #phonenum, email
          query = 'insert into employee values(' + str(id) + ',\'' + output_dict['lname'] + '\',\'' + output_dict['fname'] + '\',null,null,\''+output_dict['party'] + '\',\'' + output_dict['phone'] + '\',\'\','
          query_end = str(i) + "," + str(1) + ',\'Representative\',null);'
          query_cursor(query+query_end,cursor)
          cursor.commit()

          # make the representative
          query = 'insert into representative values(\'' +str(district) + '\',0,0,' +str(id) + ');'
          query_cursor(query,cursor)
          cursor.commit()
          district += 1
          

# insert it