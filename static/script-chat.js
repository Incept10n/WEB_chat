const params = new URLSearchParams(window.location.search);
const chatName = params.get('name');
document.getElementById('chatTitle').textContent = chatName;

const socket = new WebSocket(`ws://${window.location.host}/ws/${chatName}`);

socket.onerror = function() {
    document.body.innerHTML = '';

    const message = document.createElement('div');
    message.innerText = 'You are not authorized to chat';
    message.style.fontSize = '24px';
    message.style.color = 'red';
    message.style.textAlign = 'center';
    message.style.marginTop = '20%';
    
    document.body.appendChild(message);
};

socket.onmessage = function(event) {
    const chatMessages = document.getElementById('chatMessages');
    const message = document.createElement('div');
    message.textContent = event.data;
    chatMessages.appendChild(message);
    chatMessages.scrollTop = chatMessages.scrollHeight;
};

function sendMessage() {
    const messageInput = document.getElementById('message');
    const message = messageInput.value;
    socket.send(message);
    messageInput.value = '';
}
