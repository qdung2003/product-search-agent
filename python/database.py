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

    
    SELECT products.name, posts.price, brands.brand, {table}.*

    Ví dụ kết quả trả về (category = "Dien thoai", table = phones):
    [
        {
            "name": "Samsung Galaxy S24",
            "price": 15000000,
            "brand": "Samsung",
            "product_id": 1,
            "battery": 4000,
            "ram": 8,
            "storage": 256,
            "screen_size": 6.2,
            "os": "Android"
        },
        {
            "name": "iPhone 16",
            "price": 22000000,
            "brand": "Apple",
            "product_id": 2,
            "battery": 3561,
            "ram": 8,
            "storage": 128,
            "screen_size": 6.1,
            "os": "iOS"
        }
    ]
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
