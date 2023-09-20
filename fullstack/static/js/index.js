$(document).ready(function(){
    var btns = document.getElementsByClassName('addToCart');
    var deleteAddressBtns = document.getElementsByClassName('deleteAddress');
    var mainAddressBtns = document.getElementsByClassName('mainAddress');
    
    for(var i = 0; i < btns.length; i++){
        btns[i].addEventListener('click', function(){
            var productId = this.dataset.product;
            var action = this.dataset.action;

            updateCart(productId, action);
        })
    }

    function updateCart(productId, action) {
        fetch(`/cart/update/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken,
            },
            body: JSON.stringify({
                'productId': productId,
                'action': action
            })
        })

        .then(() =>{
            location.reload()
        })
    }

    for(var i = 0; i < deleteAddressBtns.length; i++){
        deleteAddressBtns[i].addEventListener('click', function(){
            var addressId = this.dataset.address;
            var listItem = this.parentNode;
            
            fetch(`/address/delete/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrftoken,
                },
                body: JSON.stringify({
                    'addressId': addressId,
                })
            })
    
            .then(() =>{
                listItem.remove();
            })            
        })
    }

    for(var i = 0; i < mainAddressBtns.length; i++){
        mainAddressBtns[i].addEventListener('click', function(){
            var addressId = this.dataset.address;
            var listItem = this.parentNode;
            
            fetch(`/address/make-main/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrftoken,
                },
                body: JSON.stringify({
                    'addressId': addressId,
                })
            })
    
            .then(() =>{
                location.reload()
            })            
        })
    }
})