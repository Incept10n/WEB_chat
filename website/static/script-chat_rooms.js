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

async function createChat(event) {
    event.preventDefault();
    nameOfChat = document.getElementById('nameOfChat').value;
    const showName = document.getElementById('createChat');
    const createChatButton = document.getElementById('createChatButton');
    const createChatMessage = document.getElementById('createChatMessage');

    showName.style.display = 'none';
    createChatButton.style.display = 'block'


    if (nameOfChat) {
        const response = await fetch('/create_chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ name: nameOfChat })
        });

        if (response.ok) {
            messageJson = await response.json();
            createChatMessage.textContent = messageJson.message;
            createChatMessage.style.color = 'green';
            await getOwnerChats();
            setTimeout(() => {
                createChatMessage.textContent = '';
            }, 5000)

        } else {
            const error = await response.json();
            createChatMessage.textContent = error.detail;
            createChatMessage.style.color = 'red';
            setTimeout(() => {
                createChatMessage.textContent = '';
            }, 5000)
        }
    }
}

async function deleteChat(nameOfChat) {
    if (nameOfChat) {
        const response = await fetch('/delete_chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ name: nameOfChat })
        });

        if (response.ok) {
            messageJson = await response.json();
            deleteChatMessage.textContent = messageJson.message;
            deleteChatMessage.style.color = 'green';
            await getOwnerChats();

            setTimeout(() => {
                deleteChatMessage.textContent = '';
            }, 5000)

        } else {
            const error = await response.json();
            deleteChatMessage.textContent = error.detail;
            deleteChatMessage.style.color = 'red';

            setTimeout(() => {
                deleteChatMessage.textContent = '';
            }, 5000)
        }
    }
}

async function showInsertName() {
    const showName = document.getElementById('createChat');
    const createChatButton = document.getElementById('createChatButton')

    showName.style.display = 'block';
    createChatButton.style.display = 'none'
}

async function searchChats() {
    const showCreateName = document.getElementById('createChat');
    const createChatButton = document.getElementById('createChatButton')

    showCreateName.style.display = 'none';
    createChatButton.style.display = 'inline';

    const sequence = document.getElementById('search').value;

    if(sequence.length >= 6) {
        const response = await fetch(`/chat_rooms/?sequence=${sequence}`);
        const data = await response.json();
        const chatList = document.getElementById('chatList');
        chatList.innerHTML = '';


        data.rooms.forEach(roomName => {
            const listItem = document.createElement('li');
            const divItem = document.createElement('div');
            const joinRoomBtn = document.createElement('button')
            
            

            listItem.appendChild(divItem);
            listItem.appendChild(joinRoomBtn);

            listItem.style.display = 'flex';
            listItem.style.alignItems = 'center';
            
            divItem.innerHTML = roomName;
            divItem.style.marginRight = '20px';

            joinRoomBtn.innerHTML = 'join';
            joinRoomBtn.style.cursor = 'pointer';
            joinRoomBtn.style.marginRight = '10px';
            joinRoomBtn.onclick = () => window.location.href = `/static/chat.html?name=${roomName}`;

            chatList.appendChild(listItem);
        });
    }
    else {
        searchError = document.getElementById('searchError');

        searchError.innerHTML = "Please, type at least 6 characters"
        searchError.style.color = 'red'
        searchError.style.marginTop = '10px'
        setTimeout(() => {
            searchError.innerHTML = ""
        }, 5000)
        
    }


}

async function getOwnerChats() {

    const response = await fetch('/owner_chat_rooms');
        if (response.ok) {
            const data = await response.json();
            const chatList = document.getElementById('ownerChatList');
            chatList.innerHTML = '';

            data.owner_rooms.forEach(roomName => {
                const listItem = document.createElement('li');
                const divItem = document.createElement('div');
                const joinRoomBtn = document.createElement('button')
                const delRoomBtn = document.createElement('button')
                
                

                listItem.appendChild(divItem);
                listItem.appendChild(joinRoomBtn);
                listItem.appendChild(delRoomBtn);

                listItem.style.display = 'flex';
                listItem.style.alignItems = 'center';
                
                divItem.innerHTML = roomName;
                divItem.style.marginRight = '20px';

                joinRoomBtn.innerHTML = 'join';
                joinRoomBtn.style.cursor = 'pointer';
                joinRoomBtn.style.marginRight = '10px';
                joinRoomBtn.onclick = () => window.location.href = `/static/chat.html?name=${roomName}`;


                delRoomBtn.innerHTML = 'delete';
                delRoomBtn.style.cursor = 'pointer';
                delRoomBtn.onclick = () => deleteChat(roomName);
                
                chatList.appendChild(listItem);
            });
        } else {
            const error = await response.json();
            document.body.innerHTML = '';
            
            const message = document.createElement('div');
            message.innerText = 'You are not authorized, please, login to your account';
            message.style.fontSize = '24px';
            message.style.color = 'red';
            message.style.textAlign = 'center';
            message.style.marginTop = '20%';

            document.body.appendChild(message);
        }
}


