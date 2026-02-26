// =============================================================================
// CONFIG - Cấu hình API Backend
// =============================================================================
const API_URL = 'http://localhost:5000/api/chat';
const CONVERSATION_ID = crypto.randomUUID();

// =============================================================================
// UI - Xử lý giao diện
// =============================================================================


// thêm sự kiện cho các nút

const chips = document.querySelectorAll(".chip");
const form = document.querySelector(".chat-input");

chips.forEach(chip => {
  chip.addEventListener("click", function () {
    askQuestion(this.textContent);
  });
});

form.addEventListener("submit", function (event) {
  event.preventDefault();   // chặn reload trang
  sendMessage();            // gọi hàm xử lý
});

// hàm gọi API

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
        const startTime = performance.now();
        // Gọi API Backend
        const res = await fetch(API_URL, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ question: question, conversation_id: CONVERSATION_ID })
        });

        const response = await res.json();

        const endTime = performance.now();
        const responseTime = ((endTime - startTime) / 1000).toFixed(2);
        console.log("Thời gian chờ: ", responseTime)

        hideTyping();
        addMessage(response.text, false, response.products || []);

    } catch (error) {
        hideTyping();
        addMessage(
            'Lỗi kết nối server! Hãy chắc chắn server đang chạy.<br>' +
            '<small>Chạy: <code>python backend.py</code></small>',
            false
        );
        console.error('API Error:', error);
    }
}

// các hàm con, hỗ trợ hàm trên

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
            const currency = p['Đơn vị tiền'] || '';
            const entries = Object.entries(p).filter(([k]) =>
                !['Tên', 'Giá', 'Giá KM', 'Đơn vị tiền', 'Mã SP', 'ID'].includes(k)
            );
            let specs = entries.map(([k, v]) => `<span class="spec-item">${k}: ${v}</span>`).join('');

            const price = p['Giá'] ? formatPrice(p['Giá']) + (currency ? ' ' + currency : '') : '';
            const salePrice = p['Giá KM'] ? formatPrice(p['Giá KM']) + (currency ? ' ' + currency : '') : '';

            html += `
                <div class="product-card">
                    <div class="card-header">
                        <span class="name">${i + 1}. ${p['Tên'] || ''}</span>
                    </div>
                    <div class="card-prices">
                        <span class="price${salePrice ? ' price-original' : ''}">${price}</span>
                        ${salePrice ? `<span class="sale-price">${salePrice}</span>` : ''}
                    </div>
                    <div class="card-specs">${specs}</div>
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

function askQuestion(question) {
    document.getElementById('userInput').value = question;
    sendMessage();
}
