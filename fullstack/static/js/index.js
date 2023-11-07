$(document).ready(function(){
    const checkoutItems = document.querySelector("#checkoutItems");
    var wishlistBtns = document.querySelectorAll('.wishlistBtn');

    window.addEventListener("load", function () {
        var loader = document.getElementById("preloader");
        loader.style.display = "none";
    });

    $("#searchInput").on('input', function () {
        var query = $(this).val();

        if (query.length >= 2) {
            $.ajax({
                url: '/api/search/',
                data: { q: query },
                dataType: 'json',
                success: function (data) {
                    $('#searchResult').empty();
                    if (data.result.length !== 0) {
                        data.result.forEach(function (result) {
                            $('#searchResult').append('<li class="group duration-150 flex items-center rounded-xl px-3 py-2 hover:bg-gray-900 hover:bg-opacity-5 hover:text-gray-900"><a href="/category/?q='+ encodeURIComponent(result.request) +'" class="truncate flex-auto">' + result.request + '</a></li>');
                        });
                    }
                }
            });
        } else {
            $('#searchResult').empty();
        }
    });

    function updateWishlist() {
        const productId = this.dataset.product;
        const isInWishlist = this.dataset.isInWishlist === "true";
        
        fetch('/wishlist/', {
            method: isInWishlist ? "DELETE" :  "POST",
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken
            },
            body: JSON.stringify({'product_id': productId})
        })
        .then(response => response.json())
        .then(data => {
            if (isInWishlist) {
                this.dataset.isInWishlist = false
                this.classList.remove('text-rose-500')
                this.classList.remove('hover:text-rose-600')
                this.classList.add('text-gray-400')
                this.classList.add('hover:text-gray-500')

            } else {
                this.dataset.isInWishlist = true
                this.classList.add('text-rose-500')
                this.classList.add('hover:text-rose-600')
                this.classList.remove('text-gray-400')
                this.classList.remove('hover:text-gray-500')
            }
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
                    var isInWishlistBtn = true
                } else {
                    var wishlistBtnColor = 'text-gray-500 hover:text-gray-600'
                    var isInWishlistBtn = false
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
                            <a href="${ item.product.url }" class="flex space-x-4">
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
                                <button type="button" data-product="${ item.product.id }" data-is-in-wishlist="${ isInWishlistBtn }" class="${ wishlistBtnColor } isolate wishlistBtn flex items-center justify-center bg-white p-1">
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

            if (checkoutItems) {
                checkoutPage(data);
            }
        })
        .catch(error => {
            console.log('err', error)
        })
    }

    getCart();

    function checkoutPage(data) {
        $(".checkoutTotalPriceValues").text(`${data.total_price.toLocaleString('ru-RU')} ₽`);
        $("#checkoutTotalPrice").attr("data-price", data.total_price);
        
        $("#checkoutAllItemsPrice").text(`${data.total_price.toLocaleString('ru-RU')} ₽`);
        $("#checkoutDeliveryPrice").text(`0 ₽`);
        $("#checkoutSalePrice").text(`0 ₽`);
        // $("#checkoutSaleName").append(`<span class="ml-2 rounded-full bg-gray-200 py-0.5 px-2 text-xs text-gray-600"></span>`);
        data.goods.forEach(item => {
            if (item.quantity > 1) {
                var price_per_once = `<p class="text-sm text-gray-500">1 шт / ${ item.product.price.toLocaleString('ru-RU') } ₽</p>`
            } else {
                var price_per_once = ''
            }
            var itemsArray = Object.values(item.product.images);
            var img = itemsArray.find(item => item.is_main);
            if (item.product.in_wishlist) {
                var wishlistBtnColor = 'text-rose-500 hover:text-rose-600'
                var isInWishlistBtn = true
            } else {
                var wishlistBtnColor = 'text-gray-500 hover:text-gray-600'
                var isInWishlistBtn = false
            }
            $("#checkoutItems").append(
                `
                <li class="flex group py-4 relative">
                    <div class="h-20 w-20 flex-shrink-0 overflow-hidden rounded-md">
                        <img src="${ img.image }" class="h-full w-full object-cover object-center">
                    </div>
                    <div class="flex flex-col flex-1 space-y-1 justify-between">
                        <a href="${ item.product.url }" class="flex space-x-4">
                            <span aria-hidden="true" class="absolute inset-0"></span>
                            <div class="flex flex-col">
                                <p class="duration-150 text-sm group-hover:text-blue-600">${ item.product.name }</p>
                                <p class="mt-1 text-sm text-gray-500">${ item.size.name } размер</p>
                                <p class="mt-1 text-sm text-gray-500">${ item.quantity } шт</p>
                            </div>
                        </a>
                    </div>
                    
                    <div class="flex flex-col justify-between items-end">
                        <div class="ml-4 flex flex-col justify-between items-end">
                            <p class="font-medium">${ item.total_price } ₽</p>
                            ${ price_per_once }
                        </div>
                        <div class="flex justify-between">
                            <button type="button" data-product="${ item.product.id }" data-is-in-wishlist="${ isInWishlistBtn }" class="${ wishlistBtnColor } isolate wishlistBtn flex items-center justify-center bg-white p-1">
                                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-5 h-5">
                                    <path stroke-linecap="round" stroke-linejoin="round" d="M21 8.25c0-2.485-2.099-4.5-4.688-4.5-1.935 0-3.597 1.126-4.312 2.733-.715-1.607-2.377-2.733-4.313-2.733C5.1 3.75 3 5.765 3 8.25c0 7.22 9 12 9 12s9-4.78 9-12z"></path>
                                </svg>
                            </button>
                        </div>
                    </div>
                </li>
                `
            )
        })

        wishlistBtns = document.querySelectorAll('.wishlistBtn');
        wishlistBtns.forEach(button => {
            button.addEventListener('click', updateWishlist)
        })
    }

    wishlistBtns.forEach(button => {
        button.addEventListener('click', updateWishlist);
    })


    // $('#sortForm').on('change', 'input[type=radio]', function() {
    //     $('.products').hide();
    //     $('.waiting-products').show();

    //     var sortType = $('input[name=sort]:checked').val();

    //     $.ajax({
    //         url: '/api/products/',
    //         type: 'GET',
    //         data: { sortType: sortType },
    //         dataType: 'json',
    //         success: function(data) {
    //             console.log(data)
    //             var itemsDiv = $('.products');
    //             itemsDiv.empty();

    //             $.each(data, function(index, item) {
    //                 console.log(item);
    //                 var cardDiv = $('<div class="p"></div>').text(item.fields.name);
    //                 itemsDiv.append(cardDiv);
    //             });

    //             $('.waiting-products').hide();
    //             itemsDiv.show();
    //         },
    //         error: function() {
    //             console.log('Ошибка при запросе на сервер');
    //         }
    //     });
    // });
})
