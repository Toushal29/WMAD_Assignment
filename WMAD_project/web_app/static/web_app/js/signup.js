document.addEventListener('DOMContentLoaded', () => {
    const toggle = (fieldId, iconId) => {
        const field = document.getElementById(fieldId);
        const icon  = document.getElementById(iconId);
        icon.addEventListener('click', () => {
            const isPwd = field.type === 'password';
            field.type = isPwd ? 'text' : 'password';
            icon.classList.toggle('fa-eye', !isPwd);
            icon.classList.toggle('fa-eye-slash', isPwd);
        });
    };
    toggle('id_password1', 'togglePwd1');
    toggle('id_password2', 'togglePwd2');
});