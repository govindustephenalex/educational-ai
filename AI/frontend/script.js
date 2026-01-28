document.addEventListener('DOMContentLoaded', () => {
    const userInput = document.getElementById('user-input');
    const sendBtn = document.getElementById('send-btn');
    const messagesContainer = document.getElementById('messages-container');
    const newChatBtn = document.querySelector('.new-chat-btn');
    const historyContainer = document.querySelector('.history');

    let currentSessionId = null;

    // Load history on start
    loadSessions();

    function getBaseUrl() {
        return 'http://localhost:8000';
    }

    // New Chat Button
    newChatBtn.addEventListener('click', () => {
        currentSessionId = null;
        messagesContainer.innerHTML = `
            <div class="message bot-message">
                <div class="avatar-icon"><i class="fa-solid fa-robot"></i></div>
                <div class="content">
                    Hello! I'm your personal AI Tutor. Start a new topic!
                </div>
            </div>
        `;
        // Remove active class from history items
        document.querySelectorAll('.history-item').forEach(el => el.classList.remove('active'));
    });

    // Auto-resize textarea
    userInput.addEventListener('input', function () {
        this.style.height = 'auto';
        this.style.height = (this.scrollHeight) + 'px';
        if (this.value === '') this.style.height = 'auto';
    });

    // Send on Enter
    userInput.addEventListener('keydown', function (e) {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            sendMessage();
        }
    });

    sendBtn.addEventListener('click', sendMessage);

    async function sendMessage() {
        const text = userInput.value.trim();
        if (!text) return;

        // Add user message
        addMessage(text, 'user');
        userInput.value = '';
        userInput.style.height = 'auto';

        // Show loading state
        const loadingId = addLoadingMessage();

        try {
            const response = await fetch(`${getBaseUrl()}/chat`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    message: text,
                    session_id: currentSessionId
                })
            });

            if (!response.ok) {
                throw new Error('Network response was not ok');
            }

            const data = await response.json();

            // Remove loading and add bot response
            removeMessage(loadingId);
            addMessage(data.response, 'bot', data.grade_level, data.subject);

            // Update Session ID
            if (currentSessionId !== data.session_id) {
                currentSessionId = data.session_id;
                loadSessions(); // Refresh sidebar to show new chat
            }

        } catch (error) {
            console.error('Error:', error);
            removeMessage(loadingId);
            addMessage(`Error: ${error.message}. Please ensure backend is running using 'uvicorn app.main:app --reload'`, 'bot');
        }
    }

    async function loadSessions() {
        try {
            const res = await fetch(`${getBaseUrl()}/sessions`);
            if (!res.ok) return;
            const sessions = await res.json();

            // Clear existing history (except header if involved, but here we rebuild)
            historyContainer.innerHTML = '<h3>History</h3>';

            sessions.forEach(session => {
                const item = document.createElement('div');
                item.className = 'history-item';
                if (session.id === currentSessionId) item.classList.add('active');
                item.textContent = session.title;
                item.onclick = () => loadSession(session.id);
                historyContainer.appendChild(item);
            });
        } catch (e) {
            console.error("Failed to load sessions", e);
        }
    }

    async function loadSession(sessionId) {
        currentSessionId = sessionId;

        // Highlight active item
        loadSessions();

        try {
            const res = await fetch(`${getBaseUrl()}/sessions/${sessionId}`);
            if (!res.ok) throw new Error("Failed to load");
            const session = await res.json();

            messagesContainer.innerHTML = '';
            session.messages.forEach(msg => {
                addMessage(msg.content, msg.role === 'bot' ? 'bot' : 'user', msg.grade, msg.subject);
            });
        } catch (e) {
            console.error(e);
        }
    }

    function addMessage(text, sender, grade = null, subject = null) {
        const div = document.createElement('div');
        div.className = `message ${sender}-message`;

        let icon = sender === 'user' ? '<i class="fa-solid fa-user"></i>' : '<i class="fa-solid fa-robot"></i>';

        let metadataHtml = '';
        if (sender === 'bot' && grade && subject) {
            metadataHtml = `<div style="font-size: 0.75rem; color: #64748b; margin-bottom: 5px;">Detected: ${grade} | ${subject}</div>`;
        }

        // Parse Markdown for bot
        let contentHtml = text;
        if (sender === 'bot') {
            contentHtml = marked.parse(text);
        }

        div.innerHTML = `
            <div class="avatar-icon">${icon}</div>
            <div class="content">
                ${metadataHtml}
                ${contentHtml}
            </div>
        `;

        messagesContainer.appendChild(div);
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
    }

    function addLoadingMessage() {
        const id = 'loading-' + Date.now();
        const div = document.createElement('div');
        div.className = 'message bot-message';
        div.id = id;
        div.innerHTML = `
            <div class="avatar-icon"><i class="fa-solid fa-robot"></i></div>
            <div class="content">
                <i class="fa-solid fa-circle-notch fa-spin"></i> Thinking...
            </div>
        `;
        messagesContainer.appendChild(div);
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
        return id;
    }

    function removeMessage(id) {
        const element = document.getElementById(id);
        if (element) element.remove();
    }
});
