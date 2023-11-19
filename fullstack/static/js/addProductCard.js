function addProductCard(data, list) {
    if (data.in_wishlist) {
        var wishlistBtnColor = 'text-rose-500 hover:text-rose-600'
    } else {
        var wishlistBtnColor = 'text-gray-500 hover:text-gray-600'
    }

    list.append(
        `
        <div class="relative group" data-product-card="${ data.id }">
            <div>
                <div class="aspect-w-1 aspect-h-1 overflow-hidden rounded-xl">
                    <img src="${ data.images[0].image }" class="h-full w-full object-cover object-center">
                </div>
                <a href="${ data.url }" class="block mt-2 text-gray-900 group-hover:text-blue-600 text-sm duration-150">
                    <span aria-hidden="true" class="absolute inset-0"></span>
                    ${ data.name }
                </a>
                <p class="mt-1 text-gray-900 font-medium">${ data.price.toLocaleString('ru-RU') } ₽</p>
            </div>
            <div class="absolute top-0 right-0 flex overflow-hidden -m-2 pt-2 pr-2">
                <button type="button" data-product="${ data.id }" class="${ wishlistBtnColor } wishlistBtn p-2">
                    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-5 h-5">
                        <path stroke-linecap="round" stroke-linejoin="round" d="M21 8.25c0-2.485-2.099-4.5-4.688-4.5-1.935 0-3.597 1.126-4.312 2.733-.715-1.607-2.377-2.733-4.313-2.733C5.1 3.75 3 5.765 3 8.25c0 7.22 9 12 9 12s9-4.78 9-12z"></path>
                    </svg>
                </button>
            </div>
        </div>
        `
    )
}

function findWishlistBtns() {
    var wishlistBtns = document.querySelectorAll('.wishlistBtn');
    wishlistBtns.forEach(button => {
        button.addEventListener('click', updateWishlist)
    })
}