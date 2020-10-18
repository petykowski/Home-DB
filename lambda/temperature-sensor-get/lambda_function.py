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

  # Build SQL Query
  sql = ''
  sql_base = 'SELECT VALUE FROM READING WHERE TYPE_CDE = \'T\' '
  sql_order = 'ORDER BY READING_DT DESC LIMIT 1'

  # Add Conditions
  condition_count = 0
  if event['device_mac_address'] != "":
    sql_conditions = 'AND DEVICE_MAC_ADDR = %s '
    condition_count += 1

  with connnection.cursor() as cursor:

    # Execute Query
    if condition_count == 0:
      sql = sql_base + sql_order
      cursor.execute(sql)
    else:
      sql = sql_base + sql_conditions + sql_order
      cursor.execute(sql, (event['device_mac_address']))

    # Commit and Fetch Results
    connnection.commit()
    result = cursor.fetchone()

    return {
      'statusCode': 200,
      'body': json.dumps('Hello from Lambda!'),
      'value': result[0]
    }

  connnection.close()
