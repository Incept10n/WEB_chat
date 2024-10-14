function showRegisterForm() {
    document.getElementById('registerForm').style.display = 'block';
    document.getElementById('loginForm').style.display = 'none';
}

function showLoginForm() {
    document.getElementById('loginForm').style.display = 'block';
    document.getElementById('registerForm').style.display = 'none';
}

async function register(event) {
    event.preventDefault();
    const email = document.getElementById('regEmail').value;
    const password = document.getElementById('regPassword').value;

    const response = await fetch('/register', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ email, passwd: password })
    });

    if (response.ok) {
        alert('Успешно зарегистрирован!');
        showLoginForm();
    } else {
        const error = await response.json();
        alert(error.detail);
    }
}

async function login(event) {
    event.preventDefault();
    const email = document.getElementById('loginEmail').value;
    const password = document.getElementById('loginPassword').value;

    const response = await fetch('/login', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ email, passwd: password })
    });

    if (response.ok) {
        const data = await response.json();
        document.cookie = `access_token=${data.access_token}; path=/;`;
        window.location.href = '/static/chat_rooms.html';
    } else {
        const error = await response.json();
        alert(error.detail);
    }
}
