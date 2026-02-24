# =============================================================================
# BACKEND API SERVER - AI AGENT E-COMMERCE
# =============================================================================
# Chạy: python backend.py
# API endpoint: http://localhost:5000/api/chat
# =============================================================================

from python.app import app
from python.config import OPENAI_API_KEY, MODEL

if __name__ == '__main__':
    if not OPENAI_API_KEY:
        print("CANH BAO: Chua set OPENAI_API_KEY!")
    print(f"Server: http://localhost:5000 | Model: {MODEL}")
    app.run(debug=True, host='0.0.0.0', port=5000)

