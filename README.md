# E-Commerce AI Agent Chatbot

AI chatbot hỗ trợ tìm kiếm sản phẩm e-commerce bằng ngôn ngữ tự nhiên tiếng Việt.

## Architecture

```
User → Frontend (HTML/JS) → Flask API → LangGraph StateGraph → PostgreSQL
```

**LangGraph flow:**
```
classify_intent → route_by_intent
                    ├── product_search → call_tool → execute_search → generate_answer
                    └── chitchat → handle_chitchat
```

- **classify_intent**: Phân loại ý định user (tìm sản phẩm / hỏi chuyện)
- **call_tool**: LLM + function calling → xác định category, filters, sort
- **execute_search**: Build SQL an toàn (parameterized query) + query DB
- **generate_answer**: LLM tóm tắt kết quả
- **handle_chitchat**: Trả lời câu hỏi ngoài phạm vi

## Tech Stack

- **Backend**: Python, Flask, LangGraph, LangChain, OpenAI API
- **Frontend**: HTML, CSS, JavaScript (vanilla)
- **Database**: PostgreSQL
- **Security**: Column whitelist, operator whitelist, parameterized queries

## Setup

```bash
# 1. Clone & cài dependencies
pip install -r requirements.txt

# 2. Cấu hình environment
cp .env.example .env
# Sửa .env: thêm OPENAI_API_KEY và DB credentials

# 3. Tạo database & seed data
python seed_data.py

# 4. Chạy server
python -m backend.app
# → http://localhost:5000

# 5. Mở frontend
# Mở frontend.html trong browser
```

## Project Structure

```
backend/
├── app.py          # Flask API + LangGraph integration
├── graph.py        # StateGraph definition (nodes + edges)
├── nodes.py        # Node functions (classify, search, answer...)
├── state.py        # AgentState TypedDict
├── config.py       # Category mapping + whitelist columns
├── tools.py        # Tool schema + system prompts
├── sql_builder.py  # SQL builder với security validation
└── database.py     # PostgreSQL connection

frontend.html       # Chat UI
frontend.js         # API client
frontend.css        # Styling
seed_data.py        # Database seeder (5 categories, 50 products)
```

## Supported Categories

| Category | Table | Filterable Columns |
|----------|-------|--------------------|
| Dien thoai | phones | battery, ram, storage, screen_size, os |
| Laptop | laptops | battery_hours, ram, storage, screen_size, cpu, gpu |
| Phu kien | accessories | accessory_type, compatible_with, material |
| Thoi trang | fashion | size, color, material, gender |
| Gia dung | home_appliances | power, voltage, warranty_months |
