const signUpButton = document.getElementById('signUp');
const signInButton = document.getElementById('signIn');
const container = document.getElementById('container');
const signUpForm = document.getElementById('signUpForm');
const signInForm = document.getElementById('signInForm');
const signUpEmailInput = document.getElementById('signupEmail');
const signInEmailInput = document.getElementById('signinEmail');

signUpButton.addEventListener('click', () => {
    container.classList.add("right-panel-active");
});

signInButton.addEventListener('click', () => {
    container.classList.remove("right-panel-active");
});

signUpForm.addEventListener('submit', (event) => {
    if (!signUpEmailInput.value.endsWith('@maine.edu')) {
        alert('Please use a valid Maine.edu email address for sign-up.');
        event.preventDefault();
    }
});

signInForm.addEventListener('submit', (event) => {
    if (!signInEmailInput.value.endsWith('@maine.edu')) {
        alert('Please use a valid Maine.edu email address for sign-in.');
        event.preventDefault();
    }
});
