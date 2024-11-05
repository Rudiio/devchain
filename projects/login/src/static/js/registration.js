class Feedback {
    constructor() {
        this.feedbackElement = document.getElementById('feedback');
    }

    showSuccess(message) {
        this.feedbackElement.textContent = message;
        this.feedbackElement.classList.add('alert', 'alert-success');
        this.feedbackElement.classList.remove('d-none');
    }

    showError(message) {
        this.feedbackElement.textContent = message;
        this.feedbackElement.classList.add('alert', 'alert-danger');
        this.feedbackElement.classList.remove('d-none');
    }

    hide() {
        this.feedbackElement.classList.add('d-none');
    }
}

class Registration {
    constructor() {
        this.form = document.getElementById('registration-form');
        this.usernameInput = document.getElementById('input-username');
        this.emailInput = document.getElementById('input-email');
        this.passwordInput = document.getElementById('input-password');
        this.confirmPasswordInput = document.getElementById('input-password-confirm');
        this.feedback = new Feedback();

        this.form.addEventListener('submit', this.handleRegister.bind(this));
    }

    handleRegister(event) {
        event.preventDefault();
        const username = this.usernameInput.value.trim();
        const email = this.emailInput.value.trim();
        const password = this.passwordInput.value;
        const confirmPassword = this.confirmPasswordInput.value;

        if (this.validateForm(username, email, password, confirmPassword)) {
            this.hashPassword(password).then(hashedPassword => {
                const user = {
                    username: username,
                    email: email,
                    password: hashedPassword
                };
                this.storeUserCredentials(user);
                this.feedback.showSuccess('Registration successful!');
                this.form.reset();
            }).catch(error => {
                this.feedback.showError('An error occurred during registration.');
            });
        }
    }

    async hashPassword(password) {
        const encoder = new TextEncoder();
        const data = encoder.encode(password);
        const hashBuffer = await crypto.subtle.digest('SHA-256', data);
        const hashArray = Array.from(new Uint8Array(hashBuffer));
        const hashHex = hashArray.map(b => b.toString(16).padStart(2, '0')).join('');
        return hashHex;
    }

    validateForm(username, email, password, confirmPassword) {
        if (!username || !email || !password || !confirmPassword) {
            this.feedback.showError('All fields are required.');
            return false;
        }
        if (password !== confirmPassword) {
            this.feedback.showError('Passwords do not match.');
            return false;
        }
        if (!this.validateEmail(email)) {
            this.feedback.showError('Please enter a valid email address.');
            return false;
        }
        if (!this.validatePassword(password)) {
            this.feedback.showError('Password must be at least 8 characters long, contain a number, and a special character.');
            return false;
        }
        return true;
    }

    validateEmail(email) {
        const re = /^(([^<>()\]\\.,;:\s@"]+(\.[^<>()\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
        return re.test(email.toLowerCase());
    }

    validatePassword(password) {
        const re = /^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,}$/;
        return re.test(password);
    }

    storeUserCredentials(user) {
        let users = JSON.parse(localStorage.getItem('users')) || [];
        users.push(user);
        localStorage.setItem('users', JSON.stringify(users));
    }
}

document.addEventListener('DOMContentLoaded', () => {
    new Registration();
});
