# =============================================================================
# LANGGRAPH NODES
# =============================================================================

from decimal import Decimal
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage

from .config import OPENAI_API_KEY
from .tools import INTENT_PROMPT, INTENT_SCHEMA, TOOLS, get_product_search_prompt
from .sql_builder import build_sql
from .database import query_db
from .state import AgentState

llm = ChatOpenAI(model="gpt-4.1-mini", api_key=OPENAI_API_KEY)


# =============================================================================
# NODE 1: Phân loại intent
# =============================================================================
def classify_intent(state: AgentState) -> dict:
    structured_llm = llm.with_structured_output(INTENT_SCHEMA)

    messages = [
        SystemMessage(content=INTENT_PROMPT),
        HumanMessage(content=state["question"])
    ]

    result = structured_llm.invoke(messages)
    print(f"[classify_intent] {result}")

    intent = result["intent"]

    if intent == "handle_other_types":
        return {"intent": intent, "answer": "Xin lỗi, chúng tôi chỉ hỗ trợ: Điện thoại, Laptop, Phụ kiện, Thời trang, Gia dụng.", "products": []}

    return {"intent": intent, "category": result["category"]}


# =============================================================================
# NODE 2a: Trả lời chitchat bằng LLM
# =============================================================================
def chitchat(state: AgentState) -> dict:
    messages = [SystemMessage(content="You are a shopping assistant. Reply briefly in Vietnamese. Only answer shopping-related questions. If off-topic, remind user you only assist with shopping.")]

    for msg in state["history"]:
        if msg["role"] == "user":
            messages.append(HumanMessage(content=msg["content"]))
        elif msg["role"] == "assistant":
            messages.append(AIMessage(content=msg["content"]))

    messages.append(HumanMessage(content=state["question"]))

    response = llm.invoke(messages)

    return {"answer": response.content, "products": []}


# =============================================================================
# NODE 2b: Gọi tool 
# =============================================================================
def call_tool(state: AgentState) -> dict:
    category = state["category"]
    question = state["question"]
    history = state["history"]

    messages = [SystemMessage(content=get_product_search_prompt(category))]

    for msg in history:
        if msg["role"] == "user":
            messages.append(HumanMessage(content=msg["content"]))
        elif msg["role"] == "assistant":
            messages.append(AIMessage(content=msg["content"]))

    messages.append(HumanMessage(content=question))

    llm_with_tools = llm.bind_tools(TOOLS)
    response = llm_with_tools.invoke(messages)

    if response.tool_calls:
        tool_args = response.tool_calls[0]["args"]
        tool_args["category"] = category
        return {"tool_args": tool_args}

    return {"tool_args": {"category": category}}


# =============================================================================
# NODE 3: Execute SQL
# =============================================================================
def execute_search(state: AgentState) -> dict:
    tool_args = state.get("tool_args")

    if not tool_args:
        print("[execute_search] Không có tool_args → bỏ qua")
        return {}

    sql, sql_params = build_sql(**tool_args)
    print(f"[execute_search] SQL: {sql}")
    print(f"[execute_search] Params: {sql_params}")

    products = query_db(sql, sql_params) if sql else []

    # Convert Decimal → float
    for p in products:
        for k, v in p.items():
            if isinstance(v, Decimal):
                p[k] = float(v)

    print(f"[execute_search] Tìm thấy: {len(products)} sản phẩm")

    # Không còn generate_answer nữa → trả products trực tiếp
    if not products:
        return {
            "products": [],
            "answer": "Không tìm thấy sản phẩm phù hợp."
        }

    return {
        "products": products,
        "answer": f"Tìm thấy {len(products)} sản phẩm phù hợp."
    }

