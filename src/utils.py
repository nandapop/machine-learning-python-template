''''#psql -h localhost -U airbnb_ny_user -d airbnb_ny
#dropdb -h localhost -U postgres sample-db
#\l list databases
#\dt list all tables'''
import pandas as pd
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
engine = create_engine(os.getenv('DATABASE_URL'))


if engine:
    print("connected")

def delete_tables(cursor):
    
    drop_queries = (
        "DROP TABLE IF EXISTS test;",
        "DROP TABLE IF EXISTS train;"
    )
    
    for query in drop_queries:
        cursor.execute(query)

    
def create_tables():
    my_connection = psycopg2.connect(
    host = db_parameters['host'],
    database = db_parameters['database'], 
    user = db_parameters['user'],
    password = db_parameters['password']
    )   
    cursor = my_connection.cursor()
    delete_tables(cursor)
    
    queries = (
            """
            CREATE TABLE IF NOT EXISTS test (
                id SERIAL PRIMARY KEY,
                minimum_nights INTEGER,
                number_of_reviews INTEGER,
                reviews_per_month INTEGER,
                price   FLOAT
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS train (
                id SERIAL PRIMARY KEY,
                column1 VARCHAR(255),
                column2 INTEGER,
                column3 DATE
            )
        """)
    for query in queries:
        cursor.execute(query)
        
    my_connection.commit()
    print("Tables created.")
    cursor.close()
    my_connection.close()
    
if __name__ == '__main__':
    create_tables()

def load_files(csv_files):
    for table_name, file_path in csv_files.items():
        df = pd.read_csv(file_path)
        df.to_sql(table_name, engine, if_exists='replace', index=False)  
