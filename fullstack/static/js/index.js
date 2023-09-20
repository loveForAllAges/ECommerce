$(document).ready(function(){
    var btns = document.getElementsByClassName('addToCart');

    for(var i = 0; i < btns.length; i++){
        btns[i].addEventListener('click', function(){
            var productId = this.dataset.product;
            var action = this.dataset.action;

            updateCart(productId, action);
        })
    }

    function updateCart(itemId, action) {
        pass
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


    var deleteAddressBtns = document.getElementsByClassName('deleteAddress');

    for(var i = 0; i < deleteAddressBtns.length; i++){
        deleteAddressBtns[i].addEventListener('click', function(){
            var addressId = this.dataset.address;
            var listItem = this.parentNode;

            fetch(`/address/delete/${addressId}/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrftoken,
                }
            })
    
            .then(() =>{
                listItem.remove();
            })            
        })
    }
})