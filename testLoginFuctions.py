from loginFunctions import *

server_name = r'DESKTOP-F54A5DR\SQLEXPRESS'

connection = get_database_connection(server_name,'ProjectTEst')

if connection:
  db_cursor = connection.cursor()
  username = 'username'
  passw = 'passowrd'

  if add_user(db_cursor,username,passw):
    print('user was added')
  else:
    print('user was not added')


  if user_login(db_cursor,username,passw):
    print('logged in with that user')
  else:
    print('could not login with that user')

else:
  print('connection was not successful')