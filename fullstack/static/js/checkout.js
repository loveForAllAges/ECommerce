$(document).ready(function(){
    const checkoutDeliveryLabels = document.querySelector("#checkoutDeliveryLabels");

    function getDeliveryList() {
        fetch('/orders/delivery/', {
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
            console.log('delivery data', data)

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
        
        fetch('/orders/', {
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
            console.log('OK', data)
        })
        .catch(error => {
            console.log('err')
        })
    })
})
