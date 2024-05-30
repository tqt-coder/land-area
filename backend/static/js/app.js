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