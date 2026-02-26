# =============================================================================
# BACKEND API SERVER - AI AGENT E-COMMERCE (LangGraph version)
# =============================================================================
# Chạy: python -m python.app
# API endpoint: http://localhost:5000/api/chat
# =============================================================================

import time
from flask import Flask, request, jsonify
from flask_cors import CORS
from .graph import create_graph

# Mapping tên cột tiếng Anh → tiếng Việt
COLUMN_VI = {
    # posts
    "description": "Mô tả",
    "price": "Giá",
    "sale_price": "Giá KM",
    "currency": "Đơn vị tiền",
    "quantity": "Số lượng",
    "sold_count": "Đã bán",
    # products
    "name": "Tên",
    # brands
    "brand": "Thương hiệu",
    # phones
    "battery": "Pin",
    "ram": "RAM",
    "storage": "Bộ nhớ",
    "screen_size": "Màn hình",
    "os": "Hệ điều hành",
    # laptops
    "battery_hours": "Pin",
    "cpu": "CPU",
    "gpu": "GPU",
    # accessories
    "accessory_type": "Loại",
    "compatible_with": "Tương thích",
    # fashion
    "size": "Kích cỡ",
    "color": "Màu sắc",
    "gender": "Giới tính",
    # shared
    "material": "Chất liệu",
    # home_appliances
    "power": "Công suất",
    "voltage": "Điện áp",
    "warranty_months": "Bảo hành",
    # ID columns (từ {table}.*)
    "id": "ID",
    "product_id": "Mã SP",
}

# Mapping đơn vị cho từng cột (hiển thị sau giá trị)
COLUMN_UNIT = {
    "battery": "mAh",
    "ram": "GB",
    "storage": "GB",
    "screen_size": "inch",
    "battery_hours": "giờ",
    "power": "W",
    "voltage": "V",
    "warranty_months": "tháng",
}


def translateColumn(products):
    """Chuyển key tiếng Anh → tiếng Việt, thêm đơn vị sau giá trị."""
    result = []
    for p in products:
        translated = {}
        for k, v in p.items():
            new_key = COLUMN_VI.get(k, k)
            unit = COLUMN_UNIT.get(k)
            
            if isinstance(v, float) and round(v, 2) != v:
                v = round(v, 2)
            new_value = f"{v} {unit}" if unit and v is not None else v
            translated[new_key] = new_value
        result.append(translated)
    return result

# Flask app
app = Flask(__name__)
CORS(app)

# LangGraph compiled graph
graph = create_graph()

# Short-term memory: lưu hội thoại gần đây theo conversation_id
conversations = {}
MAX_HISTORY = 4


# =============================================================================
# API ENDPOINTS
# =============================================================================
@app.route('/')
def home():
    return jsonify({"status": "running", "engine": "langgraph"})


@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.get_json()
    question = data.get('question', '')
    conv_id = data.get('conversation_id', 'default')

    # Lấy history (short-term memory)
    history = conversations.get(conv_id, [])

    print(f"\n{'='*50}")
    print(f"Câu hỏi: {question}")
    print(f"History: {len(history)} messages")

    try:
        # Chạy LangGraph
        start = time.time()
        result = graph.invoke({
            "question": question,
            "conversation_id": conv_id,
            "history": history,
        })

        llm_time = time.time() - start

        text = result["answer"]
        products = translateColumn(result["products"])

        print(f"AI trả lời: {text}")
        print(f"Thời gian phản hồi: {llm_time:.2f}s")
        print(f"{'='*50}\n")

        # Lưu vào history (chỉ giữ user + assistant, bỏ tool messages)
        history.append({"role": "user", "content": question})
        history.append({"role": "assistant", "content": text})
        conversations[conv_id] = history[-MAX_HISTORY:]

        return jsonify({"text": text, "products": products})

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"text": f"Lỗi: {str(e)}", "products": []})

