from typing import TypedDict, Optional

class AgentState(TypedDict):
    question: str
    conversation_id: str
    history: list[dict]           # conversation history
    intent: str                   # "chit_chat" | "handle_other_types" | "product_search"
    category: str | None          # "Dien thoai" | "Laptop" | ...
    tool_args: dict | None        # params từ LLM tool call (filters, sort...)
    products: list[dict]          # kết quả SQL
    answer: str                   # câu trả lời cuối cùng

