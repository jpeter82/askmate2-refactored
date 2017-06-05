import config
import psycopg2
from psycopg2 import extras
from psycopg2.pool import SimpleConnectionPool
from contextlib import contextmanager


DB = SimpleConnectionPool(1,
                          1,
                          host=config.HOST,
                          database=config.DB_NAME,
                          user=config.USER,
                          password=config.PASSWORD
                          )


@contextmanager
def get_cursor():
    conn = DB.getconn()
    try:
        yield conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        conn.commit()
    except Exception as e:
        conn.rollback()
        print('An SQL error occured:', e)
    finally:
        DB.putconn(conn)
