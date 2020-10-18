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

  with connnection.cursor() as cursor:
    sql = 'SELECT VALUE FROM READING WHERE TYPE_CDE = \'C\' ORDER BY READING_DT DESC LIMIT 1'
    cursor.execute(sql)
    connnection.commit()
    result = cursor.fetchone()

    return {
      'statusCode': 200,
      'body': json.dumps('Hello from Lambda!'),
      'value': result[0]
    }

  connnection.close()
