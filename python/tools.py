from .config import CATEGORY_MAP


INTENT_PROMPT = """
You are an intent classifier.

Allowed categories:
["Dien thoai", "Laptop", "Phu kien", "Thoi trang", "Gia dung"]

Classify the user message:

1. Greeting, general chat, not about buying anything → chit_chat
2. Wants to buy/search something NOT in allowed categories (e.g. house, car, food, book) → handle_other_types
3. Wants to buy/search something IN allowed categories → product_search

Return structured JSON.
"""

INTENT_SCHEMA = {
    "name": "intent_classification",
    "schema": {
        "type": "object",
        "properties": {
            "intent": {
                "type": "string",
                "enum": [
                    "chit_chat",
                    "handle_other_types",
                    "product_search"
                ]
            },
            "category": {
                "type": ["string", "null"]
            }
        },
        "required": ["intent", "category"],
        "additionalProperties": False,
        "if": {
            "properties": {"intent": {"const": "product_search"}}
        },
        "then": {
            "properties": {
                "category": {
                    "enum": [
                        "Dien thoai",
                        "Laptop",
                        "Phu kien",
                        "Thoi trang",
                        "Gia dung"
                    ]
                }
            }
        },
        "else": {
            "properties": {
                "category": {"const": None}
            }
        }
    }
}


# Prompt động theo category (chỉ trả cột liên quan)
def get_product_search_prompt(category):
    info = CATEGORY_MAP[category]
    table = info["table"]
    columns = info["columns"].get(table, [])
    cat_columns = ", ".join([f"{table}.{c}" for c in columns])

    return "\n".join([
        f"Extract search params for category: {category}.",
        "product_name: specific type in VIETNAMESE as user typed. Skip if asking about entire category.",
        "filters: only for numeric conditions (price, ram, storage...) or exact match. Do NOT duplicate product_name as a filter.",
        "column must use table.column format as listed below.",
        "",
        "General columns: posts.price, posts.sale_price, posts.sold_count, products.name",
        f"Category columns: {cat_columns}"
    ])


TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "search_products",
            "description": "Extract product search filters and sorting from user query.",
            "parameters": {
                "type": "object",
                "properties": {
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
                "required": []
            }
        }
    }
]