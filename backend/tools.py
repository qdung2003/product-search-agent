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
                    "product_type": {
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


# Prompt lần 1: phân loại + build tool call (cần column info)
SYSTEM_PROMPT_TOOL = "\n".join([
    "Shopping assistantool for the 5 categories below, otherwise do NOT call tool.",
    "product_type: specific type within category in VIETNAMESE as user typed (e.g. áo, ốp lưng, chuột). Skip if asking about entire category.",
    "column must use table.column format as listed below.",
    "",
    "Common columns: posts.price, posts.sale_price, posts.sold_count, products.name",
    "",
    *[
        f"{cat}: " + ", ".join(f"{info['table']}.{c}" for c in info["columns"].get(info["table"], []))
        for cat, info in CATEGORY_MAP.items()
    ]
])

# Prompt lần 2: tóm tắt kết quả (KHÔNG cần column info → tiết kiệm token)
SYSTEM_PROMPT_ANSWER = "Reply with ONE short summary sentence in Vietnamese. Do NOT list products (UI handles that). Do NOT suggest, compare, or ask follow-up."
