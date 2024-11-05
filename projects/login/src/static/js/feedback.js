document.addEventListener('DOMContentLoaded', function() {
    class Feedback {
        constructor(successSelector, errorSelector) {
            this.successElement = document.querySelector(successSelector);
            this.errorElement = document.querySelector(errorSelector);
        }

        showSuccess(message) {
            if (this.successElement) {
                this.clearFeedback();
                this.successElement.textContent = message;
                this.successElement.classList.remove('d-none');
            }
        }

        showError(message) {
            if (this.errorElement) {
                this.clearFeedback();
                this.errorElement.textContent = message;
                this.errorElement.classList.remove('d-none');
            }
        }

        clearFeedback() {
            if (this.successElement && this.errorElement) {
                this.successElement.classList.add('d-none');
                this.errorElement.classList.add('d-none');
                this.successElement.textContent = '';
                this.errorElement.textContent = '';
            }
        }
    }

    class Registration {
        constructor(feedback) {
            this.form = document.getElementById('registration-form');
            this.usernameInput = document.getElementById('input-username');
            this.emailInput = document.getElementById('input-email');
            this.passwordInput = document.getElementById('input-password');
            this.confirmPasswordInput = document.getElementById('input-password-confirm');
            this.feedback = feedback;
            this.form.addEventListener('submit', this.handleRegister.bind(this));
        }

        handleRegister(event) {
            event.preventDefault();
            const username = this.usernameInput.value.trim();
            const email = this.emailInput.value.trim();
            const password = this.passwordInput.value;
            const confirmPassword = this.confirmPasswordInput.value;
            if (this.validateForm(username, email, password, confirmPassword)) {
                const user = {
                    username: username,
                    email: email,
                    password: password
                };
                this.storeUserCredentials(user);
                this.feedback.showSuccess('Registration successful!');
                this.form.reset();
            }
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
            return true;
        }

        validateEmail(email) {
            const re = /^(([^<>()\]\\.,;:\s@"]+(\.[^<>()\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
            return re.test(email.toLowerCase());
        }

        storeUserCredentials(user) {
            let users = JSON.parse(localStorage.getItem('users')) || [];
            users.push(user);
            localStorage.setItem('users', JSON.stringify(users));
        }
    }

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
            const users = JSON.parse(localStorage.getItem('users')) || [];
            const user = users.find(user => user.email === email);
            if (user && user.password === password) {
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
                    window.location.href = '/welcome.html';
                }
            }
        }
    }

    // Updated the selectors to match the actual IDs of the DOM elements in '/templates/index.html'
    const feedback = new Feedback('#feedback-success', '#feedback-error');
    const registration = new Registration(feedback);
    const login = new Login(feedback);
});
