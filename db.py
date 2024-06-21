import sqlite3
from config import DB_NAME

def execute_sql(query):
    conn = sqlite3.connect(DB_NAME)

    conn.execute(query)
    conn.commit()
    conn.close()

def execute_read_sql(query):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(query)

    rows = cursor.fetchall()

    cursor.close()
    conn.close()
    return rows

def create_db():
    # Create users table
    create_table_sql='''
        CREATE TABLE KL_OUTLETS
        (
            NAME VARCHAR(255) PRIMARY KEY NOT NULL,
            ADDRESS VARCHAR(255),
            OPERATING_HOUR VARCHAR(255),
            WAZE_LINK VARCHAR(255),
            LONGITUDE VARCHAR(255),
            LATITUDE VARCHAR(255)
        )
        '''
    execute_sql(create_table_sql)

def read_kl_outlets():
    select_sql = "SELECT * FROM KL_OUTLETS"
    results = execute_read_sql(select_sql)
    return results