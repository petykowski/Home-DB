import json
import config
import pymysql
import logging
from datetime import datetime

# Database Settings
rds_hostname  = config.db_hostname
name = config.db_username
password = config.db_password
db_name = config.db_name

logger = logging.getLogger()
logger.setLevel(logging.INFO)

try:
  connnection = pymysql.connect(rds_hostname, user=name, passwd=password, db=db_name, connect_timeout=5)
except pymysql.MySQLError as e:
  logger.error("ERROR: Unexpected error: Could not connect to MySQL instance.")
  logger.error(e)
  sys.exit()

logger.info("SUCCESS: Connection to RDS MySQL instance succeeded")

def lambda_handler(event, context):

  # Placeholder for GET Call
  if event['type'] == 'temperature':

    with connnection.cursor() as cursor:
      sql = 'SELECT VALUE FROM READING WHERE TYPE_CDE = \'T\' ORDER BY READING_DT DESC LIMIT 1'
      cursor.execute(sql)
      result = cursor.fetchone()

      return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!'),
        'value': result[0]
      }

  # Placeholder for GET Call
  if event['type'] == 'humidity':

    with connnection.cursor() as cursor:
      sql = 'SELECT VALUE FROM READING WHERE TYPE_CDE = \'H\' ORDER BY READING_DT DESC LIMIT 1'
      cursor.execute(sql)
      result = cursor.fetchone()

      return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!'),
        'value': result[0]
      }

  # Get Values
  reading_type = event['type']
  reading_value = event['value']
  reading_unit = event['unit']
  device_id = event['deviceId']

  with connnection.cursor() as cursor:

    # Write Reading to Database
    sql = "INSERT INTO READING (TYPE_CDE, VALUE, UNIT_CDE, READING_DT, DEVICE_MAC_ADDR) VALUES (%s, %s, %s, %s, %s)"
    cursor.execute(sql, (reading_type, reading_value, reading_unit, datetime.now(), device_id))
    connnection.commit()

  return {
    'statusCode': 200,
    'body': json.dumps('Reading written successfully')
  }
