import psycopg2
from psycopg2.extras import RealDictCursor
from .config import DB_CONFIG


def get_db_connection():
    """Tạo kết nối tới PostgreSQL database"""
    return psycopg2.connect(**DB_CONFIG, cursor_factory=RealDictCursor)


def query_db(sql: str, params: tuple = None) -> list:
    """
    Execute SQL query và trả về kết quả dạng list of dict
    Sử dụng parameterized query để tránh SQL injection
    """
    conn = None
    try:
        conn = get_db_connection()
        with conn.cursor() as cursor:
            cursor.execute(sql, params)
            results = cursor.fetchall()
            return [dict(row) for row in results]
    except Exception as e:
        print(f"Database Error: {e}")
        return []
    finally:
        if conn:
            conn.close()
