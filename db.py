import sqlite3
from config import DB_NAME

def execute_sql(query:str):
    conn = sqlite3.connect(DB_NAME)

    conn.execute(query)
    conn.commit()
    conn.close()

def execute_read_sql(query:str):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(query)

    rows = cursor.fetchall()

    cursor.close()
    conn.close()
    return rows

def execute_read_sql_w_param(query:str, param:list):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(query, param)

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
    select_sql = "SELECT NAME, ADDRESS, OPERATING_HOUR, WAZE_LINK, LONGITUDE, LATITUDE FROM KL_OUTLETS"
    results = execute_read_sql(select_sql)
    return results

def get_location_outlets(location):
    count_sql = "SELECT NAME, ADDRESS, OPERATING_HOUR, WAZE_LINK, LONGITUDE, LATITUDE FROM KL_OUTLETS WHERE ADDRESS LIKE ?"
    param = [f"%{location}%"]

    result = execute_read_sql_w_param(count_sql, param)
    return result

def find_latest_closing(time):
    select_sql = "SELECT NAME, ADDRESS, OPERATING_HOUR, WAZE_LINK, LONGITUDE, LATITUDE FROM KL_OUTLETS WHERE REPLACE(OPERATING_HOUR, ' ', '') LIKE ?"
    param = [f"%{time}%"]

    results = execute_read_sql_w_param(select_sql, param)
    return results