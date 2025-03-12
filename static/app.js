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

    // Handle signup form submission
    const signupForm = document.getElementById('signupForm');
    if (signupForm) {
        signupForm.addEventListener('submit', async (e) => {
            e.preventDefault();

            const email = document.getElementById('email').value;
            const password = document.getElementById('password').value;
            const formMessage = document.getElementById('formMessage');

            // Reset previous error messages
            document.getElementById('emailError').style.display = 'none';
            document.getElementById('passwordError').style.display = 'none';
            formMessage.style.display = 'none';

            // Basic validation
            let hasError = false;
            
            if (!email) {
                const emailError = document.getElementById('emailError');
                emailError.textContent = 'Email is required';
                emailError.style.display = 'block';
                hasError = true;
            }
            
            if (!password) {
                const passwordError = document.getElementById('passwordError');
                passwordError.textContent = 'Password is required';
                passwordError.style.display = 'block';
                hasError = true;
            } else if (password.length < 6) {
                const passwordError = document.getElementById('passwordError');
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
                    formMessage.style.color = 'green';
                    formMessage.style.display = 'block';
                    signupForm.reset(); // Clear the form
                } else {
                    formMessage.textContent = result.error || 'An error occurred.';
                    formMessage.style.color = 'red';
                    formMessage.style.display = 'block';
                }
            } catch (error) {
                formMessage.textContent = 'Failed to communicate with the server. Please try again later.';
                formMessage.style.color = 'red';
                formMessage.style.display = 'block';
            }
        });
    }
});
