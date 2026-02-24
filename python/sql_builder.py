from .config import CATEGORY_MAP
from unidecode import unidecode
import re

def resolve_column(allowed_columns: list, column: str) -> str | None:
    """
    Tìm column trong whitelist. Nếu AI gửi thiếu table prefix (vd: "price"),
    tự tìm match trong whitelist (vd: "posts.price").
    Trả về full table.column nếu hợp lệ, None nếu không.
    """
    # Đã có prefix → kiểm tra trực tiếp
    if column in allowed_columns:
        return column

    # Thiếu prefix → tìm match
    matches = [c for c in allowed_columns if c.endswith(f".{column}")]
    if len(matches) == 1:
        return matches[0]

    return None


def build_sql(category: str, product_name: str = None, filters: list = None,
              sort_column: str = None, sort_direction: str = "ASC") -> tuple:
    """
    Backend quyết định: Build SQL an toàn với parameterized query

    Args:
        category: Danh mục sản phẩm
        product_name: tên sản phẩm cụ thể (nếu có)
        filters: List các filter [{column, operator, value}, ...]
        sort_column: Cột để ORDER BY
        sort_direction: ASC hoặc DESC

    Returns:
        (sql, params) tuple để execute với query_db()
    """
    if category not in CATEGORY_MAP:
        return None, None

    table = CATEGORY_MAP[category]["table"]
    category_id = CATEGORY_MAP[category]["id"]

    # Build allowed_columns 1 lần, dùng chung cho filters và sort
    allowed_columns = []
    for tbl, cols in CATEGORY_MAP[category]["columns"].items():
        for col in cols:
            allowed_columns.append(f"{tbl}.{col}")

    # Base SQL với JOIN 4 bảng: posts, products, brands, detail_table
    sql = f"""
        SELECT posts.description, posts.price, posts.sale_price, posts.currency, posts.quantity, posts.sold_count, products.name, brands.brand, {table}.*
        FROM posts
        INNER JOIN products ON posts.product_id = products.product_id
        INNER JOIN brands ON products.brand_id = brands.id
        INNER JOIN {table} ON posts.product_id = {table}.product_id
        WHERE products.category_id = %s
          AND posts.status = 'active'
    """
    params = [category_id]

    # Backend validate product_name: dùng EXISTS để check + lọc trong 1 câu SQL
    if product_name and product_name.strip():
        productName = unidecode(re.sub(r'\s+', ' ', product_name.strip()))
        sql += f"""
            AND (
                CASE
                    WHEN EXISTS (SELECT 1 FROM products p2 INNER JOIN {table} t2 ON p2.product_id = t2.product_id WHERE p2.name ILIKE %s)
                    THEN products.name ILIKE %s
                    ELSE true
                END
            )
        """
        params.extend([f"%{productName}%"] * 2)

    # Backend validate và build WHERE an toàn
    if filters:
        for f in filters:
            column = f.get("column")
            operator = f.get("operator")
            value = f.get("value")

            # Resolve column (whitelist + auto-prefix)
            resolved = resolve_column(allowed_columns, column)
            if not resolved:
                print(f"⚠️ Backend từ chối column không hợp lệ: {column}")
                continue

            # Validate operator (whitelist)
            if operator not in ["=", ">", "<", ">=", "<=", "ILIKE"]:
                print(f"⚠️ Backend từ chối operator không hợp lệ: {operator}")
                continue

            sql += f" AND {resolved} {operator} %s"
            # ILIKE: tìm theo tên, wrap %value%
            if operator == "ILIKE":
                params.append(f"%{value}%")
            else:
                params.append(value)

    # Backend validate ORDER BY
    resolved_sort = resolve_column(allowed_columns, sort_column) if sort_column else None
    if resolved_sort:
        direction = "DESC" if sort_direction == "DESC" else "ASC"
        sql += f" ORDER BY {resolved_sort} {direction}"
    else:
        sql += " ORDER BY posts.price ASC"

    # Limit (Backend kiểm soát max)
    sql += " LIMIT 5"

    return sql, tuple(params)
