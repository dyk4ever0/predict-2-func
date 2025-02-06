import psycopg2
from dotenv import load_dotenv
import os

load_dotenv()

def get_db_connection():
    """
    PostgreSQL 데이터베이스 연결 생성
    """
    connection = psycopg2.connect(
        database=os.getenv('DBname'),
        host=os.getenv('DBhost'),
        port=os.getenv('DBport'),
        user=os.getenv('DBuser'),
        password=os.getenv('DBpassword')
    )
    return connection

if __name__ == '__main__':
    try:
        conn = get_db_connection()
        print("연결 성공")
    except Exception as e:
        print("연결 실패:", e)
    finally:
        if 'conn' in locals() and conn:
            conn.close()