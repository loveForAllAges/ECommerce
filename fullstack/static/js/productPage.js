var productId = window.location.pathname.split('/')[2];
var defaultSize;


function getPageData() {
    $.ajax({
        url: '/api/products/' + productId,
        success: function(data) {
            renderCart(data.cart);
            renderHeaderCategories(data.categories); 
            renderProduct(data.content);
            renderSimilar(data.similar);
            renderProductBtns();
        },
        error: function(error) {
            console.log(error);
        }
    })
}


function renderSimilar(data) {
    $('#similar').empty();
    data.forEach(function(product) {
        renderProductCard(product, $('#similar'))
    })
}


function renderProductBtns(size=defaultSize) {
    var cartItems = cartData.goods;
    console.log('cart', cartItems)
    var btnsHTML = `
    <button type="submit" id="addToCartBtn" class="w-full sm:w-auto justify-center inline-flex items-center rounded-md border border-transparent bg-blue-600 px-4 py-2 text-sm font-medium text-white duration-150 hover:bg-blue-700">
        Добавить в корзину
    </button>
    `;
    for (var i = 0; i < cartItems.length; i++) {
        console.log(cartItems[i].product.id, productId, cartItems[i].size.id, size)
        if (cartItems[i].product.id == productId && cartItems[i].size.id == size) {
            btnsHTML = `
            <span class="inline-flex rounded-md border border-gray-200">
                <button type="button" onclick="updateCart('PUT', ${ productId }, ${ size }, true)" class="relative inline-flex items-center justify-center p-2 text-gray-400 hover:text-gray-500 duration-150">
                    <svg class="h-5 w-5" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" d="M19.5 12h-15" />
                    </svg>
                </button>
                <div class="relative justify-center cursor-default inline-flex items-center w-9 h-9 text-sm text-gray-900">${ cartItems[i].quantity }</div>
                <button type="button" onclick="updateCart('POST', ${ productId }, ${ size }, true)" class="relative inline-flex items-center justify-center p-2 text-gray-400 hover:text-gray-500 duration-150">
                    <svg class="h-5 w-5" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" d="M12 4.5v15m7.5-7.5h-15" />
                    </svg>
                </button>
            </span>
            `
            break;
        }
    }
    $("#productBtns").html(btnsHTML);
}


function renderProduct(product) {
    $('#productDetailName').html(product.name);
    $('#productDetailPrice').html(product.price.toLocaleString('ru-RU') + ' ₽');
    $('#productDetailDescription').html(product.description);
    $('#productDetailWishBtn').html(generateWishBtn(product));
    $("#categoryTitle").html('Категория');
    $("#brandTitle").html('Бренд');
    $("#similarTitle").html('Похожие товары');
    $("#similarMore").html('Смотреть все');
    $("#productDetailId").attr('data-product-card', productId);

    var sizeList = '';
    for (var i = 0; i < product.size.length; i++) {
        defaultSize = product.size[0].id;
        var checked = (i == 0) ? 'checked' : ''
        sizeList += `
            <div>
                <input type="radio" id="size-${ product.size[i].id }" name="size" value="${ product.size[i].id }" class="hidden peer" required ${ checked }>
                <label onclick="renderProductBtns(${ product.size[i].id })" for="size-${ product.size[i].id }" class="duration-150 border rounded-md px-4 py-2 flex items-center justify-center text-sm font-medium uppercase cursor-pointer focus:outline-none bg-white border-gray-200 text-gray-900 hover:bg-gray-50 peer-checked:ring-blue-600 peer-checked:ring-2">
                    ${ product.size[i].name }
                </label>
            </div>
        `
    }

    if (product.size.length > 0) {
        $('#sizeFields').html(
            `
            <div class="flex items-center justify-between">
                <h3 class="text-sm text-gray-900 font-medium">Размер</h3>
                <a href="#" class="group inline-flex text-sm text-gray-500 duration-150 hover:text-gray-600">
                    <span>Таблица размеров</span>
                    <svg class="ml-2 h-5 w-5 duration-150 text-gray-400 group-hover:text-gray-500" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" d="m11.25 11.25.041-.02a.75.75 0 0 1 1.063.852l-.708 2.836a.75.75 0 0 0 1.063.853l.041-.021M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0Zm-9-3.75h.008v.008H12V8.25Z" />
                    </svg>
                </a>
            </div>
            <div id="productSizes" class="mt-3 grid gap-4 grid-cols-4 sm:grid-cols-6">${ sizeList }</div>
            `
        )
    }

    for (var i = 0; i < product.images.length; i++) {
        $('#productImages').empty();
        $('#productImages').append(
            `
            <button id="productImages-${ i }-tab" data-tabs-target="#productImages-${ i }" type="button" role="tab" aria-controls="productImages-${ i }" aria-selected="false" class="duration-150 aria-selected:ring-2 aria-selected:ring-offset-1 aria-selected:ring-blue-600 aspect-w-1 aspect-h-1 cursor-pointer rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-600 focus:ring-offset-2">
                <span class="absolute inset-0 overflow-hidden rounded-xl">
                    <img src="${ product.images[i] }" alt="" class="h-full w-full object-cover object-center">
                </span>
            </button>
            `
        )
        $('#productImagesMenu').empty();
        $('#productImagesMenu').append(
            `
            <div role="tabpanel" id="productImages-${ i }" role="tabpanel" aria-labelledby="productImages-${ i }-tab">
                <img src="${ product.images[i] }" class="h-full w-full object-cover object-center rounded-xl">
            </div>
            `
        )
    }

    $("#category").html(`<a href="${ product.category.url }" class="text-blue-600 hover:text-blue-700 duration-150 p-1 -m-1">${ product.category.name }</a>`);
    
    var brandListHTML = [];
    product.brand.forEach(brand => {
        brandListHTML.push(`<a href="${ brand.url }" class="text-blue-600 hover:text-blue-700 duration-150 p-1 -m-1">${brand.name}</a>`);
    })
    $("#brands").html(brandListHTML.join(', '));
}


function addToCart(e) {
    e.preventDefault();
    var sizeId = e.currentTarget.elements.size.value;
    updateCart('POST', productId, sizeId, true);
}


$(document).ready(function() {
    getPageData();
    $("#addToCartForm").submit(addToCart);
})
