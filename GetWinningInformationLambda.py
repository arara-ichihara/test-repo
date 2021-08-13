import mysql.connector
import os
import sys
import traceback
from datetime import date

def lambda_handler(event, context):
  count = 0
  status_code = 0
  today = event["today"]
  user_id = event["user_id"]
  conn = mysql.connector.connect(
      user=os.environ['USER'], 
      password=os.environ['PASSWORD'], 
      port=os.environ['PORT'],
      host=os.environ['HOST'], 
      database=os.environ['DATABASE'])
  cur = None
  try:
      cur = conn.cursor(dictionary=True)
      cur.execute("select * from reservations join menus on (reservations.menu_id = menus.id) where menus.date='" 
                  + today + "' and reservations.user_id='" + user_id + "';")
      cur.fetchall()
      count = cur.rowcount
      if count == 1:
          status_code = 200
      elif count == 0:
          status_code = 404
      cur.close
  except:
      traceback.print_exc()
      print(sys.exc_info())
  finally:
      cur.close
      conn.close 

  return {
      'statusCode': status_code,
      'body': count
  }  
