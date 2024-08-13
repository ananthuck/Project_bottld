document.addEventListener('DOMContentLoaded', function() {
    const inputBox = document.getElementById('inputbox');
    const suggestionsBox = document.getElementById('suggestions');

    inputBox.addEventListener('input', function() {
        const query = inputBox.value;
        if (query.length > 0) {
            fetch(`/search/?q=${query}`)
                .then(response => response.json())
                .then(data => {
                    suggestionsBox.innerHTML = '';
                    if (data.length === 0) {
                        const li = document.createElement('li');
                        li.textContent = 'No product by that name';
                        suggestionsBox.appendChild(li);
                    } else {
                        data.forEach(product => {
                            const li = document.createElement('li');
                            li.textContent = product.name;
                            li.addEventListener('click', function() {
                                inputBox.value = product.name;
                                suggestionsBox.innerHTML = '';
                                window.location.href = `/viewproduct/${product.id}/`;
                            });
                            suggestionsBox.appendChild(li);
                        });
                    }
                })
                .catch(error => {
                    console.error('Error fetching search results:', error);
                });
        } else {
            suggestionsBox.innerHTML = '';
        }
    });

    document.querySelector('.searchbox').addEventListener('submit', function(event) {
        event.preventDefault();
        const query = inputBox.value;
        if (query.length > 0) {
            fetch(`/search/?q=${query}`)
                .then(response => response.json())
                .then(data => {
                    if (data.length > 0) {
                        window.location.href = `/viewproduct/${data[0].id}/`;
                    } else {
                        suggestionsBox.innerHTML = '<li>No product by that name</li>';
                    }
                })
                .catch(error => {
                    console.error('Error fetching search results:', error);
                });
        }
    });
});


document.addEventListener('DOMContentLoaded', function () {
    // Retrieve the URL from the data attribute
    const cartUrl = document.getElementById('cart-url').getAttribute('data-url');

    document.querySelectorAll('.plus, .minus').forEach(function (button) {
        button.addEventListener('click', function () {
            console.log('Button clicked!'); // Check if the button click is detected

            const cartItemId = this.getAttribute('data-id');
            const action = this.classList.contains('plus') ? 'increase' : 'decrease';
            
            console.log('Cart Item ID:', cartItemId); // Log the cart item ID
            console.log('Action:', action); // Log the action (increase or decrease)

            fetch(cartUrl, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': '{{ csrf_token }}',  // Ensure this is rendered correctly
                    'Content-Type': 'application/x-www-form-urlencoded',
                },
                
                body: new URLSearchParams({
                    id: cartItemId,
                    action: action,
                })
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok.');
                }
                return response.json();
            })
            .then(data => {
                if (data.error) {
                    console.error('Error:', data.error); // Log any error returned by the server
                } else {
                    document.getElementById(`quantity-${cartItemId}`).textContent = data.quantity;
                    console.log('Quantity updated:', data.quantity); // Log the updated quantity
                }
            })
            .catch(error => console.error('AJAX Error:', error)); // Log any AJAX request errors
        });
    });
});
