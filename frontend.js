// =============================================================================
// CONFIG - Cấu hình API Backend
// =============================================================================
const API_URL = 'http://localhost:5000/api/chat';
const CONVERSATION_ID = crypto.randomUUID();

// =============================================================================
// UI - Xử lý giao diện
// =============================================================================
function formatPrice(price) {
    return new Intl.NumberFormat('vi-VN').format(price) + 'đ';
}

function addMessage(content, isUser = false, products = []) {
    const messagesDiv = document.getElementById('chatMessages');

    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${isUser ? 'user' : 'agent'}`;

    let html = `<span class="message-label">${isUser ? 'Bạn' : 'AI Agent'}</span>`;
    html += `<div class="message-content">${content}`;

    // Thêm product cards nếu có
    if (products.length > 0) {
        products.forEach((p, i) => {
            let specs = '';
            if (p.battery) specs += ` | Pin: ${p.battery}mAh`;
            if (p.battery_hours) specs += ` | Pin: ${p.battery_hours}h`;
            if (p.ram) specs += ` | RAM: ${p.ram}GB`;
            if (p.cpu) specs += ` | ${p.cpu}`;
            if (p.power) specs += ` | ${p.power}W`;

            html += `
                <div class="product-card">
                    <div class="name">${i + 1}. ${p.name}</div>
                    <div class="details">
                        <span class="price">${formatPrice(p.price)}</span>
                        ${p.brand ? ' | ' + p.brand : ''}${specs}
                    </div>
                </div>
            `;
        });
    }

    html += '</div>';
    messageDiv.innerHTML = html;

    messagesDiv.appendChild(messageDiv);
    messagesDiv.scrollTop = messagesDiv.scrollHeight;
}

function showTyping() {
    const messagesDiv = document.getElementById('chatMessages');
    const typingDiv = document.createElement('div');
    typingDiv.id = 'typingIndicator';
    typingDiv.className = 'message agent';
    typingDiv.innerHTML = `
        <span class="message-label">AI Agent</span>
        <div class="message-content">
            <div class="typing">
                <span></span><span></span><span></span>
            </div>
        </div>
    `;
    messagesDiv.appendChild(typingDiv);
    messagesDiv.scrollTop = messagesDiv.scrollHeight;
}

function hideTyping() {
    const typing = document.getElementById('typingIndicator');
    if (typing) typing.remove();
}

async function sendMessage() {
    const input = document.getElementById('userInput');
    const question = input.value.trim();

    if (!question) return;

    // Hiển thị câu hỏi của user
    addMessage(question, true);
    input.value = '';

    // Hiển thị typing indicator
    showTyping();

    try {
        // Gọi API Backend
        const res = await fetch(API_URL, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ question: question, conversation_id: CONVERSATION_ID })
        });

        const response = await res.json();

        hideTyping();
        addMessage(response.text, false, response.products || []);

    } catch (error) {
        hideTyping();
        addMessage(
            'Lỗi kết nối server! Hãy chắc chắn backend đang chạy.<br>' +
            '<small>Chạy: <code>python backend.py</code></small>',
            false
        );
        console.error('API Error:', error);
    }
}

function askQuestion(question) {
    document.getElementById('userInput').value = question;
    sendMessage();
}
