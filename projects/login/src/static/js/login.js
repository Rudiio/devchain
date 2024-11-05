class Login {
    constructor(feedback) {
        this.form = document.getElementById('login-form');
        this.emailInput = document.getElementById('login-input-email');
        this.passwordInput = document.getElementById('login-input-password');
        this.feedback = feedback;
        this.form.addEventListener('submit', this.handleLogin.bind(this));
    }

    validateInputs() {
        const email = this.emailInput.value.trim();
        const password = this.passwordInput.value.trim();
        if (email === '' || password === '') {
            this.feedback.showError('Please fill in both email and password.');
            return false;
        }
        return true;
    }

    verifyCredentials(email, password) {
        const storedCredentials = JSON.parse(localStorage.getItem(email));
        if (storedCredentials && storedCredentials.password === password) {
            return true;
        }
        this.feedback.showError('Invalid email or password.');
        return false;
    }

    handleLogin(event) {
        event.preventDefault();
        if (this.validateInputs()) {
            const email = this.emailInput.value.trim();
            const password = this.passwordInput.value.trim();
            if (this.verifyCredentials(email, password)) {
                localStorage.setItem('loggedIn', true);
                window.location.href = '/welcome'; // Corrected the redirection URL
            }
        }
    }
}

// Initialize the login process when the script loads
document.addEventListener('DOMContentLoaded', function() {
    const feedback = new Feedback();
    new Login(feedback);
});
