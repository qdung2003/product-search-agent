from .config import CATEGORY_MAP


def resolve_column(category: str, column: str) -> str | None:
    """
    Tìm column trong whitelist. Nếu AI gửi thiếu table prefix (vd: "price"),
    tự tìm match trong whitelist (vd: "posts.price").
    Trả về full table.column nếu hợp lệ, None nếu không.
    """
    if category not in CATEGORY_MAP:
        return None

    allowed_columns = []
    for table, cols in CATEGORY_MAP[category]["columns"].items():
        for col in cols:
            allowed_columns.append(f"{table}.{col}")

    # Đã có prefix → kiểm tra trực tiếp
    if column in allowed_columns:
        return column

    # Thiếu prefix → tìm match
    matches = [c for c in allowed_columns if c.endswith(f".{column}")]
    if len(matches) == 1:
        return matches[0]

    return None


def build_sql(category: str, product_type: str = None, filters: list = None,
              sort_column: str = None, sort_direction: str = "ASC", **kwargs) -> tuple:
    """
    Backend quyết định: Build SQL an toàn với parameterized query

    Args:
        category: Danh mục sản phẩm
        filters: List các filter [{column, operator, value}, ...]
        sort_column: Cột để ORDER BY
        sort_direction: ASC hoặc DESC
        limit: Số lượng kết quả

    Returns:
        (sql, params) tuple để execute với parameterized query
    """
    if category not in CATEGORY_MAP:
        return None, None

    table = CATEGORY_MAP[category]["table"]
    category_id = CATEGORY_MAP[category]["id"]

    # Base SQL với JOIN 4 bảng: posts, products, brands, detail_table
    sql = f"""
        SELECT products.name, posts.price, brands.brand, {table}.*
        FROM posts
        INNER JOIN products ON posts.product_id = products.product_id
        INNER JOIN brands ON products.brand_id = brands.id
        INNER JOIN {table} ON posts.product_id = {table}.product_id
        WHERE products.category_id = %s
          AND posts.status = 'active'
    """
    params = [category_id]

    # Backend validate product_type trước khi dùng ILIKE
    if product_type and product_type.strip():
        kw = product_type.strip()
        kw_lower = kw.lower().replace(" ", "")
        cat_lower = category.lower().replace(" ", "")

        # Lấy tất cả giá trị filter để so sánh
        filter_values = set()
        if filters:
            for f in filters:
                v = str(f.get("value", "")).lower()
                if v:
                    filter_values.add(v)

        skip = False
        # 1. Trùng tên category → bỏ qua (cùng cấp)
        if kw_lower == cat_lower:
            skip = True
        # 2. Quá dài (>3 từ) → AI gửi cả câu hỏi, bỏ qua
        elif len(kw.split()) > 3:
            skip = True
        # 3. Trùng giá trị thuộc tính trong filter → bỏ qua (là attribute, không phải tên)
        elif kw.lower() in filter_values:
            skip = True

        if skip:
            print(f"⚠️ Backend bỏ qua product_type: '{kw}'")
        else:
            sql += " AND unaccent(products.name) ILIKE unaccent(%s)"
            params.append(f"%{kw}%")

    # Backend validate và build WHERE an toàn
    if filters:
        for f in filters:
            column = f.get("column")
            operator = f.get("operator")
            value = f.get("value")

            # Resolve column (whitelist + auto-prefix)
            resolved = resolve_column(category, column)
            if not resolved:
                print(f"⚠️ Backend từ chối column không hợp lệ: {column}")
                continue

            # Validate operator (whitelist)
            if operator not in ["=", ">", "<", ">=", "<=", "ILIKE"]:
                print(f"⚠️ Backend từ chối operator không hợp lệ: {operator}")
                continue

            # ILIKE: tìm theo tên, wrap %value%
            if operator == "ILIKE":
                sql += f" AND {resolved} ILIKE %s"
                params.append(f"%{value}%")
            else:
                sql += f" AND {resolved} {operator} %s"
                params.append(value)

    # Backend validate ORDER BY
    resolved_sort = resolve_column(category, sort_column) if sort_column else None
    if resolved_sort:
        direction = "DESC" if sort_direction == "DESC" else "ASC"
        sql += f" ORDER BY {resolved_sort} {direction}"
    else:
        sql += " ORDER BY posts.price ASC"

    # Limit (Backend kiểm soát max)
    sql += " LIMIT 5"

    return sql, tuple(params)
