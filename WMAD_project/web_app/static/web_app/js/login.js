document.addEventListener('DOMContentLoaded', () => {
    const pwdField = document.getElementById('id_password');
    const toggle   = document.getElementById('togglePwd');

    toggle.addEventListener('click', () => {
        const isPassword = pwdField.type === 'password';
        pwdField.type = isPassword ? 'text' : 'password';
        toggle.classList.toggle('fa-eye', !isPassword);
        toggle.classList.toggle('fa-eye-slash', isPassword);
    });

    const usernameField = document.querySelector('input[name="username"]');
    const loginBtn      = document.querySelector('.button button');

    const check = () => {
        const ready = usernameField.value.trim() && pwdField.value.trim();
        loginBtn.classList.toggle('ready', ready);
    };
    usernameField.addEventListener('input', check);
    pwdField.addEventListener('input', check);
});