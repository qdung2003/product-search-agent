from .config import CATEGORY_MAP

TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "search_products",
            "description": "Search products in the store by category, filters, and sorting.",
            "parameters": {
                "type": "object",
                "properties": {
                    "category": {
                        "type": "string",
                        "enum": list(CATEGORY_MAP.keys())
                    },
                    "product_name": { 
                        "type": "string"
                    },
                    "filters": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "column": {"type": "string"},
                                "operator": {"type": "string", "enum": ["=", ">", "<", ">=", "<=", "ILIKE"]},
                                "value": {}
                            },
                            "required": ["column", "operator", "value"]
                        }
                    },
                    "sort_column": {"type": "string"},
                    "sort_direction": {"type": "string", "enum": ["ASC", "DESC"]},
                },
                "required": ["category"]
            }
        }
    }
]

# Dienthoai: phones.battery, phones.ram, phones.storage, phones.screen_size, phones.os
'''
Shopping assistantool for the 5 categories below, otherwise do NOT call tool.",
product_type: specific type within category in VIETNAMESE as user typed (e.g. áo, ốp lưng, chuột). Skip if asking about entire category.
column must use table.column format as listed below.

Common columns: posts.price, posts.sale_price, posts.sold_count, products.name

Dien thoai: phones.battery, phones.ram, phones.storage, phones.screen_size, phones.os
Laptop: laptops.battery_hours, laptops.ram, laptops.storage, laptops.screen_size, laptops.cpu, laptops.gpu
Phu kien: accessories.accessory_type, accessories.compatible_with, accessories.material
Thoi trang: fashion.size, fashion.color, fashion.material, fashion.gender
Gia dung: home_appliances.power, home_appliances.voltage, home_appliances.warranty_months
'''

# Prompt lần 1: phân loại + build tool call (cần column info)
# Tạo danh sách mô tả cột cho từng category
category_columns = []
for cat, info in CATEGORY_MAP.items():
    table = info["table"]
    columns = info["columns"].get(table, [])
    column_strings = [f"{table}.{c}" for c in columns]
    line = f"{cat}: " + ", ".join(column_strings)
    category_columns.append(line)

SYSTEM_PROMPT_TOOL = "\n".join([
    "Shopping assistantool for the 5 categories below, otherwise do NOT call tool.",
    "product_name: specific type within category in VIETNAMESE as user typed (e.g. áo, ốp lưng, chuột). Skip if asking about entire category.",
    "column must use table.column format as listed below.",
    "",
    "General columns: posts.price, posts.sale_price, posts.sold_count, products.name",
    "Column by category:",
    *category_columns
])

# Prompt lần 2: tóm tắt kết quả (KHÔNG cần column info → tiết kiệm token)
SYSTEM_PROMPT_ANSWER = "Reply with ONE short summary sentence in Vietnamese. Do NOT list products (UI handles that). Do NOT suggest, compare, or ask follow-up."
