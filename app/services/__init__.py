import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

configs = {
    'host': os.environ.get('DB_HOST'),
    'database': os.environ.get('DB_NAME'),
    'user': os.environ.get('DB_USER'),
    'password': os.environ.get('DB_PWD') 
}


def check_if_exists_and_create_table_animes():
    conn = psycopg2.connect(**configs)
    cur = conn.cursor()
    query = """
    CREATE TABLE IF NOT EXISTS animes(
        id BIGSERIAL PRIMARY KEY,
        anime VARCHAR(100) NOT NULL UNIQUE,
        released_date DATE NOT NULL,
        seasons INTEGER NOT NULL
    )
    """
    cur.execute(query)

    conn.commit()
    cur.close()
    conn.close()

