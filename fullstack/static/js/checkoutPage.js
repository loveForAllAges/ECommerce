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
            loadPage();
        },
        error: function(error) {
        }
    })
}


function renderForm(data) {
    if (data.email) {
        console.log(data)
        for (var key in data) {
            $(`input[name='${ key }']`).val(data[key]);
        }
        $(`#customerForm input`).addClass('disabled:cursor-not-allowed disabled:shadow-none disabled:ring-gray-200 disabled:bg-gray-50 disabled:text-gray-500');
        $(`#customerForm input`).attr('disabled', true);

    }
}


// TODO - TEST FUNC
function loadPage() {
    if ($('.loadedContent').hasClass('hidden')) {
        $('.loadedContent').removeClass('hidden');
        $('.preloadedContent').addClass('hidden');
    } else {
        $('.loadedContent').addClass('hidden');
        $('.preloadedContent').removeClass('hidden');
    }
}


function renderPage(data) {
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
            sizeHTML = `<p class="text-sm text-gray-500">${ item.size.name } размер</p>`
        } else {
            sizeHTML = ''
        }

        $("#checkoutItems").append(
            `
            <div class="flex group py-4 relative">
                <div class="h-20 w-20 flex-shrink-0 overflow-hidden rounded-xl">
                    <img src="${ item.product.images[0] }" class="h-full w-full object-cover object-center">
                </div>
                <div class="flex flex-col flex-1 space-y-1 justify-between">
                    <a href="${ item.product.url }" class="flex space-x-4">
                        <span aria-hidden="true" class="absolute inset-0"></span>
                        <div class="flex flex-col">
                            <p class="duration-150 text-sm group-hover:text-blue-600">${ item.product.name }</p>
                            <div class="mt-1">
                                ${ sizeHTML }
                                <p class="text-sm text-gray-500">${ item.quantity } шт</p>
                            </div>
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
            </div>
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
        $("#checkoutDeliveryPrice").text(price + ' ₽');
        $('.checkoutTotalPriceValues').text((cartData.total_price + price).toLocaleString('ru-RU') + ' ₽');

        if ($(this).val() === 'pickup') {
            $('#checkoutAddressForm').addClass('hidden');
        } else {
            $('#checkoutAddressForm').removeClass('hidden');
        }
    }
}


function invalidField(fieldName, message='') {
    $(`#${fieldName}Field div input`).addClass('ring-2 focus:ring-red-500 ring-red-500 placeholder:text-red-400 text-red-900');
    $(`#${fieldName}Field p`).text(message);
    $(`#${fieldName}Field div div`).html(`
    <div class="pointer-events-none absolute inset-y-0 right-0 flex items-center pr-3">
        <svg class="h-5 w-5 text-red-500" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
            <path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-8-5a.75.75 0 01.75.75v4.5a.75.75 0 01-1.5 0v-4.5A.75.75 0 0110 5zm0 10a1 1 0 100-2 1 1 0 000 2z" clip-rule="evenodd"></path>
        </svg>
    </div>
    `);
}


function validField(fieldName) {
    $(`#${fieldName}Field div input`).removeClass('ring-2 focus:ring-red-500 ring-red-500 placeholder:text-red-400 text-red-900');
    $(`#${fieldName}Field p`).text('');
    $(`#${fieldName}Field div div`).html('');
}


function validateEmailField(data, fieldName) {
    const emailRegex = /^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}$/;
    const result = data.trim() !== '' && emailRegex.test(data);
    if (result) {
        validField(fieldName);
    } else {
        invalidField(fieldName, 'Неверный формат почты');
    }
    return result;
}


function validatePhoneField(data, fieldName) {
    const phoneRegex = /^(\+7|8)[0-9]{10}$/;
    const cleanPhoneNumber = data.replace(/\D/g, '');
    const result = data.trim() !== '' && phoneRegex.test(cleanPhoneNumber);
    if (result) {
        validField(fieldName);
    } else {
        invalidField(fieldName, 'Неверный формат номера телефона');
    }
    return result;
}


function validateTextField(data, fieldName) {
    const result = data.trim() !== '';
    if (result) {
        validField(fieldName);
    } else {
        invalidField(fieldName, 'Это обязательное поле');
    }
    return result;
}


function createOrder(e) {
    showLoading();
    disableButton($("#checkoutButton"));
    e.preventDefault();
    
    var listData = $('#checkoutForm').serializeArray();
    var data = {};
    $.each(listData, function(index, field) {
        data[field.name] = field.value;
        validField(field.name);
    })

    var validated = true

    if (validated) {
        $.ajax({
            url: '/api/orders/checkout/',
            type: 'POST',
            headers: {
                'X-CSRFToken': csrftoken,
            },
            data: listData,
            success: function(data) {
                console.log('SUCCESS', data);
            },
            error: function(data) {
                var errors = data.responseJSON;

                for (var key in errors) {
                    invalidField(key, errors[key][0]);
                    // showMessage(errors[key]);
                }

            },
            complete: function() {
                enableButton($("#checkoutButton"));
                hideLoading();
            }
        })
    }

}


$(document).ready(function() {
    getPageData();
    $('#checkoutDeliveryLabels').on('change', '.checkoutDeliveryInput', deliveryClicked);
    $('#checkoutForm').submit(createOrder);
})
