# =============================================================================
# BACKEND API SERVER - AI AGENT E-COMMERCE (LangGraph version)
# =============================================================================
# Chạy: python -m backend.app
# API endpoint: http://localhost:5000/api/chat
# =============================================================================

from flask import Flask, request, jsonify
from flask_cors import CORS

from .config import OPENAI_API_KEY, MODEL
from .graph import create_graph

# Flask app
app = Flask(__name__)
CORS(app)

# LangGraph compiled graph
graph = create_graph()

# Short-term memory: lưu hội thoại gần đây theo conversation_id
conversations = {}
MAX_HISTORY = 5


# =============================================================================
# API ENDPOINTS
# =============================================================================
@app.route('/')
def home():
    return jsonify({"status": "running", "model": MODEL, "engine": "langgraph"})


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
        result = graph.invoke({
            "question": question,
            "conversation_id": conv_id,
            "history": history,
            "intent": "",
            "tool_args": None,
            "products": [],
            "answer": "",
        })

        text = result["answer"]
        products = result["products"]

        print(f"AI trả lời: {text}")
        print(f"{'='*50}\n")

        # Lưu vào history (chỉ giữ user + assistant, bỏ tool messages)
        history.append({"role": "user", "content": question})
        history.append({"role": "assistant", "content": text})
        conversations[conv_id] = history[-MAX_HISTORY:]

        return jsonify({"text": text, "products": products})

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"text": f"Lỗi: {str(e)}", "products": []})


# =============================================================================
# RUN
# =============================================================================
if __name__ == '__main__':
    if not OPENAI_API_KEY:
        print("CANH BAO: Chua set OPENAI_API_KEY!")
    print(f"Server: http://localhost:5000 | Model: {MODEL} | Engine: LangGraph")
    app.run(debug=True, host='0.0.0.0', port=5000)
