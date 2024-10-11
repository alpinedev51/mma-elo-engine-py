
import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

DB_USER = os.getenv("DATABASE_USER")
DB_PW = os.getenv("DATABASE_PW")
DB_HOST = os.getenv("DATABASE_HOST")
DB_PORT = os.getenv("DATABASE_PORT")
SUPER_DB = os.getenv("SUPER_DATABASE")
DB_NAME = os.getenv("DATABASE_NAME")
 
# connection establishment
conn = psycopg2.connect(
   database=SUPER_DB,
    user=DB_USER,
    password=DB_PW,
    host=DB_HOST,
    port=DB_PORT
)
 
conn.autocommit = True
 
# Creating a cursor object
cursor = conn.cursor()
 
# query to create a database 
sql = f''' CREATE database {DB_NAME} '''
 
# executing above query
cursor.execute(sql)
print("Database has been created successfully !!")
 
# Closing the connection
conn.close()
