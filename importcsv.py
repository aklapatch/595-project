import csv
from loginFunctions import *
x=700


serverName= r'DESKTOP-F54A5DR\SQLEXPRESS'
dbName= r"ProjectTEst"
connection = get_database_connection(serverName,dbName)
cursor = connection.cursor()

with open('us-115th1-congress-members.csv', 'r') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
    next(spamreader)
    for row in spamreader:
      lname = row[1][1:-1]
      dex = lname.find('.')
      if dex != -1:
        lname = lname[0:dex-2]
      DB_entry= "insert into employee values("+str(x)+",\'"+str(row[0][1:])+"\',\'"+ lname+"\',\'"+row[2]+"\',\'"+ row[3]+"\',\'"+row[4][0]+"\',"+row[5]+",\'"+row[6]+"\',"+row[7]+","+row[8]+",\'"+row[9]+"\',\'"+row[10]+"\')"
      print(DB_entry)
      query_cursor(DB_entry,cursor)
      cursor.commit()
      
      # add to rep database
      if x==800:
        print("majority speaker")
        DB_entry= "insert into representative values(\'\',1,0,\'"+ str(x) + "\');"
      elif x==765:
        print("minority speaker")
        DB_entry= "insert into representative values(\'\',0,1,\'"+ str(x) + "\');"
      else:
        DB_entry= "insert into representative values(\'\',0,0,\'"+ str(x) + "\');"

      query_cursor(DB_entry,cursor)
      cursor.commit()
      x=x+1
