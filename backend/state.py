from typing import TypedDict


class AgentState(TypedDict):
    question: str
    conversation_id: str
    history: list[dict]           # conversation history
    intent: str                   # "product_search" | "chitchat"
    tool_args: dict | None        # params từ LLM tool call (category, filters, sort...)
    products: list[dict]          # kết quả SQL
    answer: str                   # câu trả lời cuối cùng
