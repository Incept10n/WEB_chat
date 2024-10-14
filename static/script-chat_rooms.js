document.addEventListener('DOMContentLoaded', async () => {
    await loadChatRooms();
});

async function loadChatRooms() {
    const response = await fetch('/chat_rooms/');
    const data = await response.json();
    const chatList = document.getElementById('chatList');
    chatList.innerHTML = '';

    data.rooms.forEach(roomName => {
        const listItem = document.createElement('li');
        listItem.textContent = roomName;
        listItem.onclick = () => window.location.href = `/static/chat.html?name=${roomName}`;
        chatList.appendChild(listItem);
    });
}

async function createChat() {
    const name = prompt('Введите название чата:');
    if (name) {
        const response = await fetch('/create_chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${getCookie('access_token')}`
            },
            body: JSON.stringify({ name })
        });

        if (response.ok) {
            alert('Чат успешно создан!');
            await loadChatRooms();
        } else {
            const error = await response.json();
            alert(error.detail);
        }
    }
}

async function searchChats() {
    const sequence = document.getElementById('search').value;
    const response = await fetch(`/chat_rooms/?sequence=${sequence}`);
    const data = await response.json();
    const chatList = document.getElementById('chatList');
    chatList.innerHTML = '';

    data.rooms.forEach(roomName => {
        const listItem = document.createElement('li');
        listItem.textContent = roomName;
        listItem.onclick = () => window.location.href = `/static/chat.html?name=${roomName}`;
        chatList.appendChild(listItem);
    });
}

function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
}
