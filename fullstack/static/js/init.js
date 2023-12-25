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
    const toastMessage = document.getElementById('toastMessage');
    if (toastMessage.childElementCount) {
        toastMessage.innerHTML = '';
    }
    let toast = document.createElement('div');
    toast.innerHTML = `
    <div class="pointer-events-none fixed inset-0 flex items-center justify-center z-50">
        <div class="max-w-sm pointer-events-auto cursor-default bg-black text-white text-sm py-1 px-2 rounded-lg shadow bg-opacity-75">
            <p>${message}</p>
        </div>
    </div>
    `
    toastMessage.appendChild(toast);

    setTimeout(() => {
        toast.remove();
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

// const token = '';
const token = 'Token e051d811b89793a27bc3c423736ef4165ffe42d5';
const csrftoken = getCookie();
const sessionid = getCookie('sessionid');


var productCardPreloader = `
<div class="relative group animate-pulse">
    <div class="space-y-3">
        <div class="aspect-w-1 aspect-h-1 overflow-hidden rounded-xl">
            <div class="flex items-center justify-center w-full h-full bg-gray-300 rounded">
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


function generateProductCard(product) {
    var color = (product.in_wishlist) ? 'rose' : 'gray'
    var method = (product.in_wishlist) ? 'DELETE' : 'POST';
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
            <div class="absolute top-0 right-0 flex overflow-hidden -m-2 pt-2 pr-2">
                <button type="button" onclick="updateWishStatus('${ method }', ${ product.id })" class="text-${ color }-500 hover:text-${ color }-600 p-2">
                    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-5 h-5">
                        <path stroke-linecap="round" stroke-linejoin="round" d="M21 8.25c0-2.485-2.099-4.5-4.688-4.5-1.935 0-3.597 1.126-4.312 2.733-.715-1.607-2.377-2.733-4.313-2.733C5.1 3.75 3 5.765 3 8.25c0 7.22 9 12 9 12s9-4.78 9-12z"></path>
                    </svg>
                </button>
            </div>
        </div>
    `
    return card;
}


function renderProductCard(productData, list) {
    list.append(generateProductCard(productData));
}


function updateWishStatus(HTTPmethod, productId) {
    if (!token) {
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
            'Authorization': token,
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
            // showMessage('Убрано из избранного');
        } else {
            var btns = document.querySelectorAll(`div[data-product-card="${productId}"] div button`);
            btns.forEach(btn => {
                onBtn(btn);
                btn.onclick = function() {updateWishStatus('DELETE', product.id)};
            })

            if ($('#wishList')[0]) {
                $('#wishListEmpty').classList.add('hidden');
                addProductCard(product, $("#wishList"));
            }
            // showMessage('Добавлено в избранное');
        }
    })
}
