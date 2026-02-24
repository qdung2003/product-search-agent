# =============================================================================
# LANGGRAPH NODES - Các hàm xử lý cho từng node trong graph
# =============================================================================

import json
from decimal import Decimal
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage

from .config import OPENAI_API_KEY, MODEL
from .tools import TOOLS, SYSTEM_PROMPT_TOOL, SYSTEM_PROMPT_ANSWER
from .sql_builder import build_sql
from .database import query_db
from .state import AgentState

# LLM instance dùng chung
llm = ChatOpenAI(model=MODEL, api_key=OPENAI_API_KEY)


# =============================================================================
# NODE 1: Gọi LLM với function calling để xác định search params (kiêm phân loại intent)
# =============================================================================
def call_tool(state: AgentState) -> dict:
    """
    LLM với function calling → trả về category, filters, sort.
    Giống Phase 1 của app.py cũ.
    """
    question = state["question"]
    history = state["history"]

    # Build messages giống logic cũ
    messages = [SystemMessage(content=SYSTEM_PROMPT_TOOL)]
    for msg in history:
        if msg["role"] == "user":
            messages.append(HumanMessage(content=msg["content"]))
        elif msg["role"] == "assistant":
            from langchain_core.messages import AIMessage
            messages.append(AIMessage(content=msg["content"]))
    messages.append(HumanMessage(content=question))

    # Gọi LLM với tools (OpenAI function calling)
    llm_with_tools = llm.bind_tools(TOOLS)
    response = llm_with_tools.invoke(messages)

    # Kiểm tra có tool call không
    if not response.tool_calls:
        print("[call_tool] LLM không gọi tool → chitchat")
        return {"intent": "chitchat", "tool_args": None}

    # Lấy tool call đầu tiên
    tool_call = response.tool_calls[0]
    tool_args = tool_call["args"]

    print(f"[call_tool] Category: {tool_args.get('category')}")
    print(f"[call_tool] Filters: {tool_args.get('filters', [])}")
    print(f"[call_tool] Sort: {tool_args.get('sort_column')} {tool_args.get('sort_direction')}")

    return {"tool_args": tool_args}


# =============================================================================
# NODE 2: Execute SQL query (logic thuần, không LLM)
# =============================================================================
def execute_search(state: AgentState) -> dict:
    """
    Build SQL an toàn và query database.
    Tái sử dụng build_sql() và query_db() hiện có.
    """
    tool_args = state["tool_args"]

    if not tool_args:
        print("[execute_search] Không có tool_args → bỏ qua")
        return {"products": []}

    # Build SQL (backend validate + parameterized query)
    sql, sql_params = build_sql(**tool_args)
    print(f"[execute_search] SQL: {sql}")
    print(f"[execute_search] Params: {sql_params}")

    # Execute query
    products = query_db(sql, sql_params) if sql else []

    # Convert Decimal → float để JSON serializable
    for p in products:
        for k, v in p.items():
            if isinstance(v, Decimal):
                p[k] = float(v)

    print(f"[execute_search] Tìm thấy: {len(products)} sản phẩm")

    return {"products": products}


# =============================================================================
# NODE 3: Sinh câu trả lời từ kết quả tìm kiếm
# =============================================================================
def generate_answer(state: AgentState) -> dict:
    """
    LLM tóm tắt kết quả tìm kiếm thành câu trả lời ngắn gọn.
    Giống Phase 2 của app.py cũ.
    """
    question = state["question"]
    products = state["products"]

    # Tạo bản slim cho LLM (tiết kiệm token)
    slim = [{"name": p["name"], "price": p["price"]} for p in products]
    product_info = json.dumps(slim, ensure_ascii=False)

    response = llm.invoke([
        SystemMessage(content=SYSTEM_PROMPT_ANSWER),
        HumanMessage(content=f"Câu hỏi: {question}\nKết quả: {product_info}"),
    ])

    answer = response.content
    print(f"[generate_answer] {answer}")
    return {"answer": answer}


# =============================================================================
# NODE 4: Xử lý chitchat (không cần tool)
# =============================================================================
def handle_chitchat() -> dict:
    """Trả lời cho câu hỏi không liên quan đến sản phẩm."""
    print("[handle_chitchat] Không liên quan → từ chối")
    return {
        "answer": "Xin lỗi, tôi chỉ hỗ trợ tìm sản phẩm trong cửa hàng.",
        "products": [],
    }
