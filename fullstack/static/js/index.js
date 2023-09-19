$(document).ready(function(){
    var btns = document.getElementsByClassName('addToCart');

    for(var i = 0; i < btns.length; i++){
        btns[i].addEventListener('click', function(){
            var productId = this.dataset.product;
            var action = this.dataset.action;

            if(user == 'AnonymousUser'){
                addCookieItem(productId, action);
            }else{
                updateOrder(productId, action);
            }
        })
    }

    function addCookieItem(productId, action){
        if (action == 'plus'){
            if (cart[productId] === undefined){
                cart[productId] = {'quantity': 1}
            }else{
                cart[productId]['quantity'] += 1
            }
        }

        if (action == 'minus'){
            cart[productId]['quantity'] -= 1

            if (cart[productId]['quantity'] <= 0){
                delete cart[productId]
            }
        }

        if (action == 'remove'){
            delete cart[productId]
        }

        console.log('Cart:', cart)
        document.cookie = 'cart=' + JSON.stringify(cart) + ';domain=;path=/'
        location.reload()
    }

    function updateOrder(productId, action){
        fetch('/cart/update/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken,
            },
            body: JSON.stringify({
                'productId': productId,
                'action': action,
            })
        })
        .then((response) =>{
            return response.json()
        })

        .then((data) =>{
            location.reload()
        })
    }
})