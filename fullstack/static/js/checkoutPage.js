function getPageData() {
    $.ajax({
        url: '/api/orders/checkout/',
        success: function(data) {
            console.log(data);
            renderCart(data.cart);
            renderHeaderCategories(data.categories);
            renderDeliveries(data.deliveries);
            renderPage(data.cart);
            renderForm(data.customer);
        },
        error: function(error) {
        }
    })
}


function renderForm(data) {
    if (data.email) {
        for (var key in data) {
            $(`#customerForm input[name='${ key }']`).val(data[key]);

        }
        $(`#customerForm input`).addClass('disabled:cursor-not-allowed disabled:border-gray-200 disabled:bg-gray-50 disabled:text-gray-500');
        $(`#customerForm input`).attr('disabled', true);
    }
}


function renderPage(data) {
    $("#pageTitle").text('Оформление заказа');
    $("#customerDataTitle").text('Персональные данные');
    $("#totalAmount").text('Итоговая стоимость');
    $("#checkoutDeliveryPrice").text(`0 ₽`);
    $("#checkoutSalePrice").text(`0 ₽`);
    $('#checkoutItems').empty();
    $(".checkoutTotalPriceValues").text(`${data.total_price.toLocaleString('ru-RU')} ₽`);
    $("#checkoutTotalPrice").attr("data-price", data.total_price);
    $("#checkoutAllItemsPrice").text(`${data.total_price.toLocaleString('ru-RU')} ₽`);
    data.goods.forEach(item => {
        if (item.quantity > 1) {
            var price_per_once = `<p class="text-sm text-gray-500">1 шт / ${ item.product.price.toLocaleString('ru-RU') } ₽</p>`
        } else {
            var price_per_once = ''
        }

        if (item.size) {
            sizeHTML = `<p class="mt-1 text-sm text-gray-500">${ item.size.name } размер</p>`
        } else {
            sizeHTML = ''
        }

        $("#checkoutItems").append(
            `
            <li class="flex group py-4 relative">
                <div class="h-20 w-20 flex-shrink-0 overflow-hidden rounded-md">
                    <img src="${ item.product.images[0] }" class="h-full w-full object-cover object-center">
                </div>
                <div class="flex flex-col flex-1 space-y-1 justify-between">
                    <a href="${ item.product.url }" class="flex space-x-4">
                        <span aria-hidden="true" class="absolute inset-0"></span>
                        <div class="flex flex-col">
                            <p class="duration-150 text-sm group-hover:text-blue-600">${ item.product.name }</p>
                            ${ sizeHTML }
                            <p class="text-sm text-gray-500">${ item.quantity } шт</p>
                        </div>
                    </a>
                </div>
                
                <div data-product-card="${ item.product.id }" class="flex flex-col justify-between items-end">
                    <div class="ml-4 flex flex-col justify-between items-end">
                        <p class="font-medium">${ item.total_price.toLocaleString('ru-RU') } ₽</p>
                        ${ price_per_once }
                    </div>
                    <div class="flex justify-between">${ generateWishBtn(item.product) }</div>
                </div>
            </li>
            `
        )
    })
}


function renderDeliveries(data) {
    data.forEach((element, key) => {
        var isChecked = (element.slug === 'pickup') ? 'checked' : '';
        var price = (element.info) ? element.info : element.price + ' ₽';
        var angles = '';
        if (key === 0) angles = 'rounded-tl-md rounded-tr-md';
        else if (key === data.length - 1) angles = 'rounded-bl-md rounded-br-md';
        $('#checkoutDeliveryLabels').append(
            `
            <label for="delivery-${ element.id }" class="${ angles } duration-150 relative border p-4 flex cursor-pointer focus:outline-none hover:bg-gray-50 peer-checked:bg-gray-50">
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
}


function deliveryClicked() {
    if ($(this).is(':checked')) {
        var price = parseFloat(this.dataset.price);
        var totalPrice = parseFloat($("#checkoutTotalPrice").data("price"));
        $("#checkoutDeliveryPrice").text(price + ' ₽');
        $('.checkoutTotalPriceValues').text((totalPrice + price).toLocaleString('ru-RU') + ' ₽');

        if ($(this).val() === 'pickup') {
            $('#checkoutAddressForm').addClass('hidden');
        } else {
            $('#checkoutAddressForm').removeClass('hidden');
        }
    }
}


$(document).ready(function() {
    getPageData();
    $('#checkoutDeliveryLabels').on('change', '.checkoutDeliveryInput', deliveryClicked);
})


$(document).ready(function(){
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
        .then(response => {
            if (response.ok) {
                return response.json()
            } else {
                showMessage('Введены неверные данные')
                throw new Error()
            }
        })
        .then(data => {
            window.location.href = data.url;
        }) 
        .catch(error => {
        })
    })
})
