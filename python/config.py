import os
from dotenv import load_dotenv
load_dotenv()

# =============================================================================
# OpenAI Config
# =============================================================================
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# =============================================================================
# Database Config
# =============================================================================
DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "port": os.getenv("DB_PORT", "5432"),
    "database": os.getenv("DB_NAME", "ecommerce"),
    "user": os.getenv("DB_USER", "postgres"),
    "password": os.getenv("DB_PASSWORD", "postgres")
}

# =============================================================================
# Category Mapping: category → table, id, columns (whitelist)
# =============================================================================
CATEGORY_MAP = {
    "Dien thoai": {
        "table": "phones",
        "id": 1,
        "columns": {
            "posts": ["price", "sale_price", "sold_count"],
            "products": ["name"],
            "phones": ["battery", "ram", "storage", "screen_size", "os"]
        }
    },
    "Laptop": {
        "table": "laptops",
        "id": 2,
        "columns": {
            "posts": ["price", "sale_price", "sold_count"],
            "products": ["name"],
            "laptops": ["battery_hours", "ram", "storage", "screen_size", "cpu", "gpu"]
        }
    },
    "Phu kien": {
        "table": "accessories",
        "id": 3,
        "columns": {
            "posts": ["price", "sale_price", "sold_count"],
            "products": ["name"],
            "accessories": ["accessory_type", "compatible_with", "material"]
        }
    },
    "Thoi trang": {
        "table": "fashion",
        "id": 4,
        "columns": {
            "posts": ["price", "sale_price", "sold_count"],
            "products": ["name"],
            "fashion": ["size", "color", "material", "gender"]
        }
    },
    "Gia dung": {
        "table": "home_appliances",
        "id": 5,
        "columns": {
            "posts": ["price", "sale_price", "sold_count"],
            "products": ["name"],
            "home_appliances": ["power", "voltage", "warranty_months"]
        }
    },
}
