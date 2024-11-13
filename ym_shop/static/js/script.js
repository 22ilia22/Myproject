document.addEventListener('DOMContentLoaded', () => {
    const registerBtn = document.querySelector('button[type="submit"]');
    registerBtn.addEventListener('click', (event) => {
        alert('Форма регистрации отправлена');
    });
});