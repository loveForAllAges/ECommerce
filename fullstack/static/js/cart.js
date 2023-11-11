
function putCart() {
    var productId = this.dataset.product;
    var action = this.dataset.action;
    var sizeId = this.dataset.size;

    fetch('/cart/', {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify({
            'product_id': productId,
            'action': action,
            'size_id': sizeId,
        })
    })

    .then(response => response.json())
    .then(data => {
        updateCart(data);

        const checkoutItems = document.querySelector("#checkoutItems");
        if (checkoutItems) {
            checkoutPage(data);
        }
    })
    .catch(error => {
        console.log('err', error)
    })
}

function getCart() {
    fetch('/cart/', {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
        },
    })
    .then(response => response.json())
    .then(data => {
        updateCart(data);

        const checkoutItems = document.querySelector("#checkoutItems");
        if (checkoutItems) {
            checkoutPage(data);
        }
    })
    .catch(error => {
        console.log('err', error)
    })
}

function updateCart(data) {
    $("#cartItems").empty();
    $("#cartSize").text(data.size);
    $("#cartSize_m").text(data.size);
    if (data.goods.length === 0) {
        $("#cartEmpty").removeClass('hidden');
        $("#cartCheckout").addClass('hidden');
    } else {
        $("#cartEmpty").addClass('hidden');
        $("#cartCheckout").removeClass('hidden');
        $("#cartTotalPrice").text(`${data.total_price.toLocaleString('ru-RU')} ₽`);
        data.goods.forEach(item => {
            if (item.quantity > 1) {
                var price_per_once = `<p class="text-sm text-gray-500">1 шт / ${ item.product.price.toLocaleString('ru-RU') } ₽</p>`
            } else {
                var price_per_once = ''
            }
            if (item.product.in_wishlist) {
                var wishlistBtnColor = 'text-rose-500 hover:text-rose-600'
            } else {
                var wishlistBtnColor = 'text-gray-500 hover:text-gray-600'
            }
            var itemsArray = Object.values(item.product.images);
            var img = itemsArray.find(item => item.is_main);

            $("#cartItems").append(
                `
                <li class="flex group p-4 relative">
                    <div class="w-20 h-20 sm:h-24 sm:w-24 flex-shrink-0 overflow-hidden rounded-md">
                        <img src="${ img.image }" class="h-full w-full object-cover object-center">
                    </div>
                    <div class="flex flex-col flex-1 space-y-1 justify-between">
                        <a href="${ item.product.id }" class="flex space-x-4">
                            <span aria-hidden="true" class="absolute inset-0"></span>
                            <div class="flex flex-col">
                                <div class="duration-150 text-sm group-hover:text-blue-600">${ item.product.name }</div>
                                <div class="mt-1 text-sm text-gray-500">${ item.size.name } размер</div>
                            </div>
                        </a>
                        <div class="ml-4">
                            <span class="isolate inline-flex rounded-md border border-gray-200">
                                <button type="button" data-product="${ item.product.id }" data-action="minus" data-size="${ item.size.id }" class="cartBtn relative inline-flex items-center justify-center p-1 text-gray-400 hover:text-gray-500 duration-150">
                                    <svg class="h-5 w-5" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor">
                                        <path stroke-linecap="round" stroke-linejoin="round" d="M19.5 12h-15" />
                                    </svg>
                                </button>
                                <div class="relative justify-center cursor-default inline-flex items-center w-7 h-7 text-sm text-gray-900">${ item.quantity }</div>
                                <button type="button" data-product="${ item.product.id }" data-action="plus" data-size="${ item.size.id }" class="cartBtn relative inline-flex items-center justify-center p-1 text-gray-400 hover:text-gray-500 duration-150">
                                    <svg class="h-5 w-5" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor">
                                        <path stroke-linecap="round" stroke-linejoin="round" d="M12 4.5v15m7.5-7.5h-15" />
                                    </svg>
                                </button>
                            </span>
                        </div>
                    </div>
                    
                    <div class="flex flex-col justify-between items-end">
                        <div class="ml-4 flex flex-col justify-between items-end">
                            <p class="font-medium">${ item.total_price.toLocaleString('ru-RU') } ₽</p>
                            ${ price_per_once }
                        </div>
                        <div class="flex justify-between">
                            <button type="button" data-product="${ item.product.id }" class="${ wishlistBtnColor } isolate wishlistBtn flex items-center justify-center bg-white p-1">
                                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-5 h-5">
                                    <path stroke-linecap="round" stroke-linejoin="round" d="M21 8.25c0-2.485-2.099-4.5-4.688-4.5-1.935 0-3.597 1.126-4.312 2.733-.715-1.607-2.377-2.733-4.313-2.733C5.1 3.75 3 5.765 3 8.25c0 7.22 9 12 9 12s9-4.78 9-12z"></path>
                                </svg>
                            </button>
                        </div>
                    </div>
                </li>
                `
            );
        })
    }

    wishlistBtns = document.querySelectorAll('.wishlistBtn');
    wishlistBtns.forEach(button => {
        button.addEventListener('click', updateWishlist)
    })

    var cartBtns = document.querySelectorAll('.cartBtn');
    cartBtns.forEach(button => {
        button.addEventListener('click', putCart)
    })
}