const sign_in_btn = document.querySelector("#sign-in-btn");
const sign_up_btn = document.querySelector("#sign-up-btn");
const container = document.querySelector(".container");

sign_up_btn.addEventListener('click', () =>{
    container.classList.add("sign-up-mode");
});

sign_in_btn.addEventListener('click', () =>{
    container.classList.remove("sign-up-mode");
});
setTimeout(function() {
    const flashMessages = document.getElementById('flash-messages');
    if (flashMessages) {
        flashMessages.style.transition = 'opacity 0.5s ease-out';
        flashMessages.style.opacity = '0';
        setTimeout(function() {
            flashMessages.remove();
        }, 500);
    }
}, 2000);

document.getElementById('login-form').addEventListener('submit', async function (e) {
    e.preventDefault();
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;
    let res = {
        'email': email,
        'password': password
    }
    const response = await fetch('/login', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(res)
    });

    const data = await response.json();
    if (data.status === 200) {
        localStorage.setItem('token', data.token);
        window.location.href = 'http://localhost:3000/admin/map'; // Adjust the URL as needed
    } else {
        alert(data.message);
    }
});