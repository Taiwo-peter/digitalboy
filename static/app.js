document.addEventListener('DOMContentLoaded', () => {
    // Handle the mobile menu toggle
    const menu = document.querySelector('#mobile-menu');
    const menuLinks = document.querySelector('.navbar__menu');

    if (menu) {
        menu.addEventListener('click', () => {
            menu.classList.toggle('is-active');
            menuLinks.classList.toggle('active');
        });
    }

    // Handle contact form submission
    const contactForm = document.getElementById('contactForm');
    if (contactForm) {
        contactForm.addEventListener('submit', async function (event) {
            event.preventDefault(); // Prevent default form submission

            // Gather form data
            const name = document.getElementById('name').value;
            const email = document.getElementById('email').value;
            const message = document.getElementById('message').value;

            // Basic validation
            if (!name || !email || !message) {
                alert('Please fill in all fields');
                return;
            }

            try {
                // Send a POST request to the backend API
                const response = await fetch('/api/contact', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json', // Specify JSON format
                    },
                    body: JSON.stringify({ name, email, message }), // Convert data object to JSON string
                });

                // Parse the response from the server
                const result = await response.json();

                if (response.ok) {
                    // If the request was successful, display the server message
                    alert(result.message || 'Your message was sent successfully.');
                    contactForm.reset(); // Clear the form fields
                } else {
                    // If the server responds with an error, display it
                    alert(result.error || 'There was an issue sending your message.');
                }
            } catch (error) {
                // Handle any network or unexpected errors
                console.error('Error:', error);
                alert('An unexpected error occurred. Please try again.');
            }
        });
    }

    // Handle authentication UI (Signup and Login tabs)
    const signupTab = document.getElementById('signupTab');
    const loginTab = document.getElementById('loginTab');
    const signupFormContainer = document.getElementById('signupFormContainer');
    const loginFormContainer = document.getElementById('loginFormContainer');
    const switchToLogin = document.getElementById('switchToLogin');
    const switchToSignup = document.getElementById('switchToSignup');
    const formMessage = document.getElementById('formMessage');

    // Function to switch between signup and login views
    function toggleAuthForms(showSignup) {
        if (showSignup) {
            signupFormContainer.style.display = 'block';
            loginFormContainer.style.display = 'none';
            signupTab.classList.add('active');
            loginTab.classList.remove('active');
        } else {
            signupFormContainer.style.display = 'none';
            loginFormContainer.style.display = 'block';
            loginTab.classList.add('active');
            signupTab.classList.remove('active');
        }
        formMessage.style.display = 'none';
    }

    // Tab click handlers
    if (signupTab) {
        signupTab.addEventListener('click', () => toggleAuthForms(true));
    }
    
    if (loginTab) {
        loginTab.addEventListener('click', () => toggleAuthForms(false));
    }
    
    // Link click handlers
    if (switchToLogin) {
        switchToLogin.addEventListener('click', () => toggleAuthForms(false));
    }
    
    if (switchToSignup) {
        switchToSignup.addEventListener('click', () => toggleAuthForms(true));
    }

    // Handle signup form submission
    const signupForm = document.getElementById('signupForm');
    if (signupForm) {
        signupForm.addEventListener('submit', async (e) => {
            e.preventDefault();

            const email = document.getElementById('signupEmail').value;
            const password = document.getElementById('signupPassword').value;

            // Reset previous error messages
            document.getElementById('signupEmailError').style.display = 'none';
            document.getElementById('signupPasswordError').style.display = 'none';
            formMessage.style.display = 'none';

            // Basic validation
            let hasError = false;
            
            if (!email) {
                const emailError = document.getElementById('signupEmailError');
                emailError.textContent = 'Email is required';
                emailError.style.display = 'block';
                hasError = true;
            }
            
            if (!password) {
                const passwordError = document.getElementById('signupPasswordError');
                passwordError.textContent = 'Password is required';
                passwordError.style.display = 'block';
                hasError = true;
            } else if (password.length < 6) {
                const passwordError = document.getElementById('signupPasswordError');
                passwordError.textContent = 'Password must be at least 6 characters';
                passwordError.style.display = 'block';
                hasError = true;
            }
            
            if (hasError) return;

            try {
                const response = await fetch('/api/signup', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ email, password }),
                });

                const result = await response.json();

                if (response.ok) {
                    formMessage.textContent = result.message;
                    formMessage.style.backgroundColor = '#1e392a';
                    formMessage.style.color = '#7affa7';
                    formMessage.style.display = 'block';
                    signupForm.reset(); // Clear the form
                } else {
                    formMessage.textContent = result.error || 'An error occurred.';
                    formMessage.style.backgroundColor = '#391e1e';
                    formMessage.style.color = '#ff7a7a';
                    formMessage.style.display = 'block';
                }
            } catch (error) {
                formMessage.textContent = 'Failed to communicate with the server. Please try again later.';
                formMessage.style.backgroundColor = '#391e1e';
                formMessage.style.color = '#ff7a7a';
                formMessage.style.display = 'block';
            }
        });
    }
    
    // Handle login form submission
    const loginForm = document.getElementById('loginForm');
    if (loginForm) {
        loginForm.addEventListener('submit', async (e) => {
            e.preventDefault();

            const email = document.getElementById('loginEmail').value;
            const password = document.getElementById('loginPassword').value;

            // Reset previous error messages
            document.getElementById('loginEmailError').style.display = 'none';
            document.getElementById('loginPasswordError').style.display = 'none';
            formMessage.style.display = 'none';

            // Basic validation
            let hasError = false;
            
            if (!email) {
                const emailError = document.getElementById('loginEmailError');
                emailError.textContent = 'Email is required';
                emailError.style.display = 'block';
                hasError = true;
            }
            
            if (!password) {
                const passwordError = document.getElementById('loginPasswordError');
                passwordError.textContent = 'Password is required';
                passwordError.style.display = 'block';
                hasError = true;
            }
            
            if (hasError) return;

            try {
                const response = await fetch('/api/login', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ email, password }),
                });

                const result = await response.json();

                if (response.ok) {
                    formMessage.textContent = 'Login successful! Redirecting...';
                    formMessage.style.backgroundColor = '#1e392a';
                    formMessage.style.color = '#7affa7';
                    formMessage.style.display = 'block';
                    
                    // Redirect to home page after successful login
                    setTimeout(() => {
                        window.location.href = '/services.html';
                    }, 1500);
                } else {
                    formMessage.textContent = result.error || 'Login failed. Please check your credentials.';
                    formMessage.style.backgroundColor = '#391e1e';
                    formMessage.style.color = '#ff7a7a';
                    formMessage.style.display = 'block';
                }
            } catch (error) {
                formMessage.textContent = 'Failed to communicate with the server. Please try again later.';
                formMessage.style.backgroundColor = '#391e1e';
                formMessage.style.color = '#ff7a7a';
                formMessage.style.display = 'block';
            }
        });
    }
});
