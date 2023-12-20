function getPageData() {
    productId = window.location.pathname.split('/')[2];
    $.ajax({
        url: 'api/products/' + productId,
        success: function(data) {
            console.log('data', data);
        },
        error: function(error) {
            console.log('error');
        }
    })
}


function renderPage() {
    $('#productDetailName').html('PRODUCT NAME');
    $('#productDetailPrice').html('PRODUCT PRICE');
    $('#productDetailDescription').html('PRODUCT DESC');
    $('#productDetailWishBtn').html(
        `
        <button type="button" data-product="{{ object.id }}" data-is-in-wishlist="true" class="wishlistBtn inline-flex items-center rounded-xl p-1 text-rose-500 hover:text-rose-600">
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-5 h-5">
                <path stroke-linecap="round" stroke-linejoin="round" d="M21 8.25c0-2.485-2.099-4.5-4.688-4.5-1.935 0-3.597 1.126-4.312 2.733-.715-1.607-2.377-2.733-4.313-2.733C5.1 3.75 3 5.765 3 8.25c0 7.22 9 12 9 12s9-4.78 9-12z"></path>
            </svg>
        </button>
        `
    )

    // Если есть размеры
    $('#addToCartForm').html(
        `
        <div class="flex items-center justify-between">
            <h3 class="text-sm text-gray-900 font-medium">Размер</h3>
            <a href="#" class="group inline-flex text-sm text-gray-500 duration-150 hover:text-gray-600">
                <span>Таблица размеров</span>
                <svg class="ml-2 h-5 w-5 flex-shrink-0 duration-150 text-gray-400 group-hover:text-gray-500" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
                    <path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zM8.94 6.94a.75.75 0 11-1.061-1.061 3 3 0 112.871 5.026v.345a.75.75 0 01-1.5 0v-.5c0-.72.57-1.172 1.081-1.287A1.5 1.5 0 108.94 6.94zM10 15a1 1 0 100-2 1 1 0 000 2z" clip-rule="evenodd"></path>
                </svg>
            </a>
        </div>
        <div id="productSizes" class="mt-3 grid gap-4 grid-cols-4 sm:grid-cols-6">
        </div>
        `
    )
    // Цикл загрузки размеров
    $('#productSizes').append(
        `
        <div>
            <input type="radio" id="size-{{ size.slug }}" name="size" value="{{ size.id }}" class="hidden peer" required {% if forloop.counter == 1 %}checked{% endif %}>
            <label for="size-{{ size.slug }}" class="duration-150 border rounded-md px-4 py-2 flex items-center justify-center text-sm font-medium uppercase sm:flex-1 cursor-pointer focus:outline-none bg-white border-gray-200 text-gray-900 hover:bg-gray-50 peer-checked:ring-blue-600 peer-checked:ring-2">
                {{ size.name }}
            </label>
        </div>
        `
    )

    $('#productDetailBtns').append(
        `
        <button type="submit" id="addToCartBtn" class="w-full sm:w-auto justify-center inline-flex items-center rounded-md border border-transparent bg-blue-600 px-4 py-2 text-sm font-medium text-white duration-150 hover:bg-blue-700">
            Добавить в корзину
        </button>
        <!-- <a href="#" class="w-full sm:w-auto justify-center inline-flex items-center rounded-md border border-transparent bg-black px-4 py-2 text-sm font-medium text-white shadow-sm hover:bg-gray-900 duration-150 focus:outline-none focus:ring-2 focus:ring-black focus:ring-offset-2">
            Купить сейчас
        </a> -->
        `
    )

    // Цикл загрузки фото
    images.forEach(image => {
        // Установить первое изображение
        $('#productImages').html(
            `
            <button id="productImages-{{ forloop.counter }}-tab" data-tabs-target="#productImages-{{ forloop.counter }}" type="button" role="tab" aria-controls="productImages-{{ forloop.counter }}" aria-selected="false" class="duration-150 aria-selected:ring-2 aria-selected:ring-offset-1 aria-selected:ring-black aspect-w-1 aspect-h-1 cursor-pointer rounded-lg focus:outline-none focus:ring-2 focus:ring-black focus:ring-offset-2">
                <span class="absolute inset-0 overflow-hidden rounded-lg">
                    <img src="{{ image.image.url }}" alt="" class="h-full w-full object-cover object-center">
                </span>
            </button>
            `
        )
        
        $('#productImagesMenu').append(
            `
            <div role="tabpanel" id="productImages-{{ forloop.counter }}" role="tabpanel" aria-labelledby="productImages-{{ forloop.counter }}-tab">
                <img src="{{ image.image.url }}" class="h-full w-full object-cover object-center rounded-xl">
            </div>
            `
        )
    })
}


function renderRecomendations() {
    renderProductCard(data, $('#recomendations'));
}


$(document).ready(function(){
    var addToCartForm = document.querySelector('#addToCartForm');

    addToCartForm.addEventListener('submit', function(event) {
        event.preventDefault();
        const formData = new FormData(addToCartForm);
        fetch('/cart/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken,
            },
            body: JSON.stringify({
                'product_id': formData.get('product'),
                'size_id': formData.get('size'),
            })
        })
        .then(response => response.json())
        .then(data => {
            console.log(data)
            updateCart(data);
            showMessage('Товар добавлен в корзину');
        })
        .catch(error => {
            console.log('addToCartForm err', error)
        })
    })
})

$(document).ready(function() {
    getPageData();
})