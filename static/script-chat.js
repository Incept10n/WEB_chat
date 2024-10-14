const params = new URLSearchParams(window.location.search);
const chatName = params.get('name');
document.getElementById('chatTitle').textContent = chatName;

const socket = new WebSocket(`ws://${window.location.host}/ws/${chatName}`);

socket.onmessage = function(event) {
    const chatMessages = document.getElementById('chatMessages');
    const message = document.createElement('div');
    message.textContent = event.data;
    chatMessages.appendChild(message);
};

function sendMessage() {
    const messageInput = document.getElementById('message');
    const message = messageInput.value;
    socket.send(message);
    messageInput.value = '';
}
