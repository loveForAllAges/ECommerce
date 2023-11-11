$(document).ready(function(){
    var addToCartForm = document.querySelector('#addToCartForm');

    addToCartForm.addEventListener('submit', function(event) {
        event.preventDefault();
        const formData = new FormData(addToCartForm);
        fetch('/cart/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken,
            },
            body: JSON.stringify({
                'product_id': formData.get('product'),
                'size_id': formData.get('size'),
            })
        })
        .then(response => response.json())
        .then(data => {
            console.log(data)
            updateCart(data);
        })
        .catch(error => {
            console.log('addToCartForm err', error)
        })
    })
})