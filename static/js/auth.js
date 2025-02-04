document.getElementById('login-button').addEventListener('click', function(event) {
    event.preventDefault();
    document.getElementById('login-modal').classList.remove('hidden');
});

document.getElementById('toggle-auth-form').addEventListener('click', function(event) {
    event.preventDefault();
    const loginForm = document.getElementById('login-form');
    const registerForm = document.getElementById('register-form');
    const modalTitle = document.getElementById('modal-title');
    if (loginForm.classList.contains('hidden')) {
        loginForm.classList.remove('hidden');
        registerForm.classList.add('hidden');
        modalTitle.textContent = 'Login';
        this.textContent = 'Create new account';
    } else {
        loginForm.classList.add('hidden');
        registerForm.classList.remove('hidden');
        modalTitle.textContent = 'Create Account';
        this.textContent = 'Already have an account? Sign in';
    }
});

function closeModal() {
    document.getElementById('login-modal').classList.add('hidden');
}