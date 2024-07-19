import psycopg2


def get_db_connection():
    conn = psycopg2.connect(
        dbname='quiz_master_db',
        user='postgres',
        password='bezhan2009',
        host='127.0.0.1',
        port='5432'
    )
    return conn
