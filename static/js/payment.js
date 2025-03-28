
const stripe = Stripe('your_publishable_key');
const elements = stripe.elements();
const card = elements.create('card');
card.mount('#card-element');

const form = document.getElementById('payment-form');
form.addEventListener('submit', async (event) => {
    event.preventDefault();
    const {token, error} = await stripe.createToken(card);
    
    if (error) {
        const errorElement = document.getElementById('card-errors');
        errorElement.textContent = error.message;
    } else {
        const response = await fetch('/api/process-payment', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({token: token.id})
        });
        
        const result = await response.json();
        if (result.success) {
            window.location.href = '/payment-success';
        } else {
            const errorElement = document.getElementById('card-errors');
            errorElement.textContent = result.error;
        }
    }
});
