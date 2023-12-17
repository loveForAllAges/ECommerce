function updateWishlist() {
    const productId = this.dataset.product;
    
    fetch('/api/wishlist/', {
        method: "POST",
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken
        },
        body: JSON.stringify({'product_id': productId})
    })
    .then(response => {
        if (response.status == 200) {
            return response.json()
        } else {
            throw new Error('err')
        }
    })
    .then(product => {
        var wishWindow = document.querySelector('#wishlistWindow');
        var wishList = document.getElementById('wishList');
        var wishListEmpty = document.getElementById('wishListEmpty');

        if (product.in_wishlist) {
            this.classList.add('text-rose-500')
            this.classList.add('hover:text-rose-600')
            this.classList.remove('text-gray-400')
            this.classList.remove('hover:text-gray-500')

            if (wishWindow) {
                wishListEmpty.classList.add('hidden');
                addProductCard(product, $("#wishList"));
            }

            var otherItemsInCart = document.querySelectorAll(`.wishlistBtn[data-product="${productId}"]`);
            otherItemsInCart.forEach(element => {
                element.classList.add('text-rose-500')
                element.classList.add('hover:text-rose-600')
                element.classList.remove('text-gray-400')
                element.classList.remove('hover:text-gray-500')    
            })
            showMessage('Добавлено в избранное');
        } else {
            this.classList.remove('text-rose-500')
            this.classList.remove('hover:text-rose-600')
            this.classList.add('text-gray-400')
            this.classList.add('hover:text-gray-500')

            if (wishWindow) {
                document.querySelector(`div[data-product-card="${ productId }"]`).remove();

                if (wishList.childElementCount === 0) {
                    wishListEmpty.classList.remove('hidden')
                }
            }

            var otherItemsInCart = document.querySelectorAll(`.wishlistBtn[data-product="${ productId }"]`);
            otherItemsInCart.forEach(element => {
                element.classList.remove('text-rose-500')
                element.classList.remove('hover:text-rose-600')
                element.classList.add('text-gray-400')
                element.classList.add('hover:text-gray-500')     
            })
            showMessage('Убрано из избранного');
        }
    })
}
