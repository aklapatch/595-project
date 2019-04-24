import pyodbc
import hashlib

def get_database_connection(server_name,db_name):
  conn_param = (
    r'Driver={SQL Server};'
    r'Server=' + server_name + ';'
    r'Database=' + db_name + ';'
    r'Trusted_Connection=yes;'
  )
  try:
    connection = pyodbc.connect(conn_param)
  except:
    return False

  connection.setdecoding(pyodbc.SQL_CHAR, encoding='utf-8')
  connection.setdecoding(pyodbc.SQL_WCHAR, encoding='utf-8')
  connection.setencoding(encoding='utf-8')

  return connection

# get the server login
# you will need to replace this string later to check the login
def user_login(db_cursor, user_name, password):

  hash_func = hashlib.sha384()
  hash_func.update(password.encode())
  pass_hash = hash_func.hexdigest()

  sql_str = "select userID from users where username='" + user_name + "' and passwordHash='" + str(pass_hash) + "';"

  db_cursor.execute(sql_str)

  row = db_cursor.fetchone()

  # if the user was found
  if row:
    return True
  else:
    return False

def user_exists(db_cursor, user_name):

  sql_str = "select userID from users where username='" + user_name + "';"

  db_cursor.execute(sql_str)

  row = db_cursor.fetchone()

  # if the user was found
  if row:
    return True
  else:
    return False

def add_user(db_cursor,user_name,password):

  if user_exists(db_cursor,user_name):
    print('user already exists')
    return False

  sha_hash = hashlib.sha384()
  sha_hash.update(password.encode())
  pass_hash = sha_hash.hexdigest()

  insert_query = "insert into users values('" + user_name+ "','" + str(pass_hash) + "',null);"
  try:
    db_cursor.execute(insert_query)
  except:
    return False

  db_cursor.commit()

  return True  