async function login() {
    const id = document.getElementById('loginId').value;
    const pwd = document.getElementById('loginPwd').value;
    const res = await fetch('/api/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ voter_id: id, password: pwd })
    });
    if (res.ok) {
        localStorage.setItem('voterId', id);
        window.location.href = '/dashboard';
    } else {
        alert('Login failed. Verify your credentials.');
    }
}

async function register() {
    const id = document.getElementById('regId').value;
    const pwd = document.getElementById('regPwd').value;
    const name = document.getElementById('regName').value;
    const age = parseInt(document.getElementById('regAge').value);

    const res = await fetch('/api/register', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ voter_id: id, password: pwd, name: name, age: age })
    });

    if (res.ok) {
        alert('Registration successful. You may now log in.');
    } else {
        alert('Registration failed. Ensure you are 18+ and the ID is unique.');
    }
}