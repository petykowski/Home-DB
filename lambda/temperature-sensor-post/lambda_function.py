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
  logger.info("SUCCESS: Connection to RDS MySQL instance succeeded")
except pymysql.MySQLError as e:
  logger.error("ERROR: Unexpected error: Could not connect to MySQL instance.")
  logger.error(e)
  sys.exit()

def lambda_handler(event, context):

  # Set Values
  reading_type = 'T'
  reading_value = event['value']
  reading_unit = 'C'
  device_id = event['device_mac_address']

  with connnection.cursor() as cursor:

    # Determine if device is authorized to write data
    sql_validate_device = "SELECT is_device_authorized(%s)"
    cursor.execute(sql_validate_device, (device_id))
    connnection.commit()
    is_device_authorized = cursor.fetchone()

    if is_device_authorized[0]:

      # Write Reading to Database
      sql = "INSERT INTO READING (TYPE_CDE, VALUE, UNIT_CDE, READING_DT, DEVICE_MAC_ADDR) VALUES (%s, %s, %s, %s, %s)"
      cursor.execute(sql, (reading_type, reading_value, reading_unit, datetime.now(), device_id))
      connnection.commit()

      return {
        'statusCode': 200,
        'body': json.dumps('Reading written successfully')
      }

    else:
      return {
          'statusCode': 450,
          'body': json.dumps('Device not authorized to write data.')
        }

  connnection.close()
