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
        } else {
            var wishlistBtnColor = 'text-gray-500 hover:text-gray-600'
        }
        $('#checkoutItems').empty();
        $("#checkoutItems").append(
            `
            <li class="flex group py-4 relative">
                <div class="h-20 w-20 flex-shrink-0 overflow-hidden rounded-md">
                    <img src="${ img.image }" class="h-full w-full object-cover object-center">
                </div>
                <div class="flex flex-col flex-1 space-y-1 justify-between">
                    <a href="${ item.product.id }" class="flex space-x-4">
                        <span aria-hidden="true" class="absolute inset-0"></span>
                        <div class="flex flex-col">
                            <p class="duration-150 text-sm group-hover:text-blue-600">${ item.product.name }</p>
                            <p class="mt-1 text-sm text-gray-500">${ item.size.name } размер</p>
                            <p class="text-sm text-gray-500">${ item.quantity } шт</p>
                        </div>
                    </a>
                </div>
                
                <div class="flex flex-col justify-between items-end">
                    <div class="ml-4 flex flex-col justify-between items-end">
                        <p class="font-medium">${ item.total_price } ₽</p>
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
        )
    })

    wishlistBtns = document.querySelectorAll('.wishlistBtn');
    wishlistBtns.forEach(button => {
        button.addEventListener('click', updateWishlist)
    })
}

$(document).ready(function(){
    function getDeliveryList() {
        fetch('/api/delivery/', {
            method: 'GET',
        })
        .then(response => response.json())
        .then(data => {
            data.forEach(element => {
                var isChecked = (element.slug === 'pickup') ? 'checked' : '';
                var price = (element.info) ? element.info : element.price + ' ₽';
                $('#checkoutDeliveryLabels').append(
                    `
                    <label for="delivery-${ element.id }" class="rounded-tl-md rounded-tr-md duration-150 relative border p-4 flex cursor-pointer focus:outline-none hover:bg-gray-50 peer-checked:bg-gray-50">
                        <input type="radio" data-price=${ element.price } required id="delivery-${ element.id }" ${isChecked} name="delivery" value="${ element.slug }" class="checkoutDeliveryInput duration-150 mt-0.5 h-4 w-4 shrink-0 cursor-pointer text-blue-600 border-gray-300 focus:ring-blue-600">
                        <span class="ml-3 w-full">
                            <div class="flex justify-between text-sm">
                                <div class="font-medium">${ element.name }</div>
                                <div class="text-gray-500">${ price }</div>
                            </div>
                            <span class="text-sm text-gray-500">${ element.description }</span>
                        </span>
                    </label>
                    `
                )
            });

            $('.checkoutDeliveryInput').change(function() {
                if ($(this).is(':checked')) {
                    var price = parseFloat(this.dataset.price);
                    var totalPrice = parseFloat($("#checkoutTotalPrice").data("price"));
                    $("#checkoutDeliveryPrice").text(price + ' ₽');
                    var checkoutTotalPriceValues = document.querySelectorAll('.checkoutTotalPriceValues');
                    checkoutTotalPriceValues.forEach(function(element) {
                        element.textContent = (totalPrice + price).toLocaleString('ru-RU') + ' ₽';
                    })

                    if ($(this).val() === 'pickup') {
                        $('#checkoutAddressForm').addClass('hidden');
                    } else {
                        $('#checkoutAddressForm').removeClass('hidden');
                    }
                }
            });
        })
        .catch(error => {
            console.log('err', error)
        })
    }

    getDeliveryList()

    const checkoutForm = document.querySelector('#checkoutForm');

    checkoutForm.addEventListener('submit', function(event) {
        event.preventDefault();
        const checkoutFormData = new FormData(checkoutForm);
        
        fetch('/api/orders/', {
            method: 'POST',
            headers: {
                'X-CSRFToken': csrftoken,
            },
            body: checkoutFormData
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                window.location.href = data.data.url;
            }
        })
        .catch(error => {
            console.log('err')
        })
    })
})
