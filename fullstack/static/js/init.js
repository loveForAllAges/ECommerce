function getCookie(data='csrftoken') {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            if (cookie.substring(0, data.length + 1) === (data + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(data.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}


function showMessage(message) {
    const is_exists = document.getElementById('message');
    const body = document.getElementById('body');
    if (is_exists) {
        is_exists.remove();
    }
    const new_message = document.createElement('div');
    new_message.innerHTML = `
        <div id="message">
            <div class="pointer-events-none fixed inset-0 flex items-center justify-center z-50">
                <div class="max-w-sm pointer-events-auto cursor-default bg-black text-white text-sm py-1 px-2 rounded-lg shadow bg-opacity-75">
                    <p>${message}</p>
                </div>
            </div>
        </div>
    `;
    body.appendChild(new_message);

    setTimeout(() => {
        body.removeChild(new_message);
    }, 3000)
}


function renderHeaderCategories(categories) {
    categories.forEach(category => {
        $('#mainCategoryHeader').append(
            `
            <a href="/catalog?category=${ category.id }" class="flex items-center text-sm duration-150 text-black hover:text-blue-700">${ category.name }</a>
            `
        )
    })
}

var authToken = localStorage.getItem('token');
const csrftoken = getCookie();
const sessionid = getCookie('sessionid');
var cartData;


var productCardPreloader = `
<div class="relative group animate-pulse">
    <div class="space-y-3">
        <div class="aspect-w-1 aspect-h-1 overflow-hidden rounded-xl">
            <div class="flex items-center justify-center w-full h-full bg-gray-300 rounded-xl">
                <svg class="w-10 h-10 text-gray-200 dark:text-gray-600" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="currentColor" viewBox="0 0 20 18">
                    <path d="M18 0H2a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2V2a2 2 0 0 0-2-2Zm-5.5 4a1.5 1.5 0 1 1 0 3 1.5 1.5 0 0 1 0-3Zm4.376 10.481A1 1 0 0 1 16 15H4a1 1 0 0 1-.895-1.447l3.5-7A1 1 0 0 1 7.468 6a.965.965 0 0 1 .9.5l2.775 4.757 1.546-1.887a1 1 0 0 1 1.618.1l2.541 4a1 1 0 0 1 .028 1.011Z"/>
                </svg>
            </div>
        </div>
        <div class="block text-gray-900 group-hover:text-blue-600 text-sm duration-150">
            <div class="my-1 h-3 bg-gray-200 rounded-full"></div>
        </div>
        <div>
            <div class="my-1 h-4 bg-gray-300 rounded-full w-24"></div>
        </div>
    </div>
</div>
`;


function showLoading() {
    $('#body').append(`
    <div class="fixed inset-0 flex items-center justify-center z-50 bg-black/30 backdrop-blur-sm" id="loading">
        <div class="relative h-12 w-12 flex items-center justify-center">
            <div class="animate-spin left-2 top-2 absolute border-l-2 border-white w-[calc(100%-16px)] h-[calc(100%-16px)] rounded-full"></div>
            <div class="animate-spin-left left-3 top-3 absolute border-r-2 border-white w-[calc(100%-24px)] h-[calc(100%-24px)] rounded-full"></div>
            <div class="animate-spin left-4 top-4 absolute border-l-2 border-white w-[calc(100%-32px)] h-[calc(100%-32px)] rounded-full"></div>
        </div>
    </div>
    `);
}


function hideLoading() {
    $('#loading').remove();
}


function generateWishBtn(product) {
    var color = (product.in_wishlist) ? 'rose' : 'gray'
    var method = (product.in_wishlist) ? 'DELETE' : 'POST';
    return `
    <button type="button" onclick="updateWishStatus('${ method }', ${ product.id })" class="text-${ color }-500 hover:text-${ color }-600 p-2 -m-2 isolate">
        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-5 h-5">
            <path stroke-linecap="round" stroke-linejoin="round" d="M21 8.25c0-2.485-2.099-4.5-4.688-4.5-1.935 0-3.597 1.126-4.312 2.733-.715-1.607-2.377-2.733-4.313-2.733C5.1 3.75 3 5.765 3 8.25c0 7.22 9 12 9 12s9-4.78 9-12z"></path>
        </svg>
    </button>
    `;
}


function generateProductCard(product) {

    var card = `
        <div class="relative group" data-product-card="${ product.id }">
            <div>
                <div class="aspect-w-1 aspect-h-1 overflow-hidden rounded-xl">
                    <img src="${ product.images[0] }" class="h-full w-full object-cover object-center">
                </div>
                <a href="${ product.url }" class="block mt-2 text-gray-900 group-hover:text-blue-600 text-sm duration-150">
                    <span aria-hidden="true" class="absolute inset-0"></span>
                    ${ product.name }
                </a>
                <p class="mt-1 text-gray-900 font-medium">${ product.price.toLocaleString('ru-RU') } ₽</p>
            </div>
            <div class="absolute top-0 right-0 flex overflow-hidden pt-2 pr-2">${ generateWishBtn(product) }</div>
        </div>
    `
    return card;
}


function renderProductCard(productData, list) {
    list.append(generateProductCard(productData));
}


function updateWishStatus(HTTPmethod, productId) {
    if (!authToken) {
        showMessage('Необходимо авторизоваться');
        return;
    }
    function onBtn(obj) {
        obj.classList.add(`text-rose-500`)
        obj.classList.add(`hover:text-rose-600`)
        obj.classList.remove(`text-gray-400`)
        obj.classList.remove(`hover:text-gray-500`)
    }
    function offBtn(obj) {
        obj.classList.add(`text-gray-400`)
        obj.classList.add(`hover:text-gray-500`)
        obj.classList.remove(`text-rose-500`)
        obj.classList.remove(`hover:text-rose-600`)
    }

    fetch('/api/products/wish', {
        method: HTTPmethod,
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
            'Authorization': authToken,
        },
        body: JSON.stringify({'product_id': productId})
    })
    .then(response => {
        return response.json()
    })
    .then(product => {
        if (product.in_wishlist) {

            var btns = document.querySelectorAll(`div[data-product-card="${productId}"] div button`);
            btns.forEach(btn => {
                offBtn(btn);
                btn.onclick = function() {updateWishStatus('POST', product.id)};
            })

            if ($('#wishList')[0]) {
                document.querySelector(`div[data-product-card="${ productId }"]`).remove();

                if ($('#wishList')[0].childElementCount === 0) {
                    $('#wishList').html(emptyWishListHTML);
                }
            }
        } else {
            var btns = document.querySelectorAll(`div[data-product-card="${productId}"] div button`);
            btns.forEach(btn => {
                onBtn(btn);
                btn.onclick = function() {updateWishStatus('DELETE', product.id)};
            })

            if ($('#wishList')[0]) {
                $('#wishListEmpty').addClass('hidden');
                product.in_wishlist = true;
                renderProductCard(product, $("#wishList"));
            }
        }
    })
}


function getSimplePageData() {
    $.ajax({
        url: '/api/auth/init',
        success: function(data) {
            renderCart(data.cart);
            renderHeaderCategories(data.categories);
        },
        error: function(error) {
        }
    })
}


function renderCart(data) {
    cartData = data;
    $("#cartItems").empty();
    $(".cartSize").text(data.size);
    if (data.goods.length === 0) {
        $("#cartEmpty").removeClass('hidden');
        $("#cartCheckout").addClass('hidden');
    } else {
        $("#cartEmpty").addClass('hidden');
        $("#cartCheckout").removeClass('hidden');
        $("#cartTotalPrice").text(`${data.total_price.toLocaleString('ru-RU')} ₽`);
        data.goods.forEach(item => {
            if (item.quantity > 1) {
                var price_per_once = `<p class="text-xs text-gray-500">1 шт / ${ item.product.price.toLocaleString('ru-RU') } ₽</p>`
            } else {
                var price_per_once = ''
            }

            if (item.size) {
                sizeHTML = `<div class="mt-1 text-sm text-gray-500">${ item.size.name } размер</div>`
                itemSize = item.size.id
            } else {
                sizeHTML = ''
                itemSize = ''
            }

            $("#cartItems").append(
                `
                <li class="flex group p-4 relative">
                    <div class="w-20 h-20 sm:h-24 sm:w-24 flex-shrink-0 overflow-hidden rounded-md">
                        <img src="${ item.product.images[0] }" class="h-full w-full object-cover object-center">
                    </div>
                    <div class="flex flex-col flex-1 space-y-1 justify-between">
                        <a href="${ item.product.url }" class="flex space-x-4">
                            <span aria-hidden="true" class="absolute inset-0"></span>
                            <div class="flex flex-col">
                                <div class="duration-150 text-sm group-hover:text-blue-600">${ item.product.name }</div>
                                ${sizeHTML}
                            </div>
                        </a>
                        <div class="ml-4">
                            <span class="isolate inline-flex rounded-md border border-gray-200">
                                <button type="button" onclick="updateCart('PUT', ${ item.product.id }, ${ itemSize })" class="relative inline-flex items-center justify-center p-1 text-gray-400 hover:text-gray-500 duration-150">
                                    <svg class="h-5 w-5" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor">
                                        <path stroke-linecap="round" stroke-linejoin="round" d="M19.5 12h-15" />
                                    </svg>
                                </button>
                                <div class="relative justify-center cursor-default inline-flex items-center w-7 h-7 text-sm text-gray-900">${ item.quantity }</div>
                                <button type="button" onclick="updateCart('POST', ${ item.product.id }, ${ itemSize })" class="relative inline-flex items-center justify-center p-1 text-gray-400 hover:text-gray-500 duration-150">
                                    <svg class="h-5 w-5" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor">
                                        <path stroke-linecap="round" stroke-linejoin="round" d="M12 4.5v15m7.5-7.5h-15" />
                                    </svg>
                                </button>
                            </span>
                        </div>
                    </div>
                    
                    <div class="flex flex-col justify-between items-end" data-product-card=${ item.product.id }>
                        <div class="ml-4 flex flex-col justify-between items-end">
                            <p class="font-medium">${ item.total_price.toLocaleString('ru-RU') } ₽</p>
                            ${ price_per_once }
                        </div>
                        <div>${ generateWishBtn(item.product) }</div>
                    </div>
                </li>
                `
            );
        })
    }
}


function updateCart(HTTPmethod, productId, sizeId, detailPage=false) {
    showLoading();
    $.ajax({
        url: '/api/cart/',
        headers: {
            'X-CSRFToken': csrftoken,
        },
        type: HTTPmethod,
        data: {
            'product': productId, 'size': sizeId
        },
        success: function(data) {
            renderCart(data.content);
            if ($('#productDetailName')[0] && productId == window.location.pathname.split('/')[2]) renderProductBtns(sizeId);
            hideLoading();
            showMessage(data.message);
        },
        error: function(error) {
            hideLoading();
            showMessage(error.responseJSON.message);
        }
    })
}


function disableButton(button) {
    button.attr('disabled', true);
    button.addClass('disabled:cursor-not-allowed disabled:shadow-none disabled:bg-blue-400');
}


function enableButton(button) {
    button.attr('disabled', false);
    button.removeClass('disabled:cursor-not-allowed disabled:shadow-none disabled:bg-blue-400');
}
