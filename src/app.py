'''I didn't create model classes as suggested by the README file.

`models/` - This directory should contain your SQLAlchemy model classes.
'''
from utils import *
from sqlalchemy import create_engine
import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

db_parameters = {
    'host': os.getenv('DB_HOST'),
    'database': os.getenv('DB_NAME'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD')
}

def show_data(cursor):
    select_query = (
            """
            SELECT * FROM test LIMIT 10; 
            """,
            """
            SELECT * FROM  train LIMIT 10;
        """)
    for query in select_query:
        cursor.execute(query)
        rows = cursor.fetchall()
        print(f"\nResults for query",query)
        for row in rows:
            print(row)

if __name__ == '__main__':
    
    my_connection = psycopg2.connect(
        host = db_parameters['host'],
        database = db_parameters['database'], 
        user = db_parameters['user'],
        password = db_parameters['password']
    )   
cursor = my_connection.cursor()

create_tables()
csv_files = {
        'test': '../machine-learning-python-template/data/processed/clean_airbnb_test.csv',
        'train': '../machine-learning-python-template/data/processed/clean_airbnb_train.csv'
    }
load_files(csv_files)
show_data(cursor)            
cursor.close()
my_connection.close()