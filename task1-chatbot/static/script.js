const messagesDiv = document.getElementById('messages');
const inputEl = document.getElementById('user-input');

// Show welcome message on load
window.onload = () => {
  addMessage("Hi! I'm RuleBot 🤖 I use rule-based pattern matching to chat. Type 'help' to see what I can do!", 'bot');
};

function addMessage(text, type) {
  const wrap = document.createElement('div');
  wrap.className = `message ${type}`;

  const av = document.createElement('div');
  av.className = 'msg-avatar';
  av.textContent = type === 'bot' ? 'R' : 'U';

  const bubble = document.createElement('div');
  bubble.className = 'bubble';
  bubble.textContent = text;

  wrap.appendChild(av);
  wrap.appendChild(bubble);
  messagesDiv.appendChild(wrap);
  messagesDiv.scrollTop = messagesDiv.scrollHeight;
}

function showTyping() {
  const wrap = document.createElement('div');
  wrap.className = 'message bot'; wrap.id = 'typing';
  wrap.innerHTML = `<div class="msg-avatar">R</div>
    <div class="bubble typing-dots">
      <span></span><span></span><span></span>
    </div>`;
  messagesDiv.appendChild(wrap);
  messagesDiv.scrollTop = messagesDiv.scrollHeight;
}

function removeTyping() {
  const t = document.getElementById('typing');
  if (t) t.remove();
}

async function sendMessage() {
  const text = inputEl.value.trim();
  if (!text) return;
  addMessage(text, 'user');
  inputEl.value = '';
  showTyping();

  try {
    const res = await fetch('/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ message: text })
    });
    const data = await res.json();
    setTimeout(() => {
      removeTyping();
      addMessage(data.response, 'bot');
    }, 600);
  } catch (e) {
    removeTyping();
    addMessage("Error connecting to server!", 'bot');
  }
}

function sendSuggestion(text) {
  inputEl.value = text;
  sendMessage();
}

inputEl.addEventListener('keydown', e => { if (e.key === 'Enter') sendMessage(); });
