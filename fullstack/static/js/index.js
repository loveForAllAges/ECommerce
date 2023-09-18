$(document).ready(function(){
    console.log('loaded');
    var btns = document.getElementsByClassName('addToCart');
    console.log(btns);

    for(var i = 0; i < btns.length; i++){
        btns[i].addEventListener('click', function(){
            var productId = this.dataset.product;
            var action = this.dataset.action;
            console.log('productId:', productId, 'Action:', action);

            console.log('USER:', user);
            // if(user == 'AnonymousUser'){
            //     addCookieItem(productId, action);
            // }else{
            //     updateUserOrder(productId, action);
            // }
        })
    }
})