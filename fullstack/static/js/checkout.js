$(document).ready(function(){
    $('input[name="delivery"]').change(function() {
        if($(this).is(':checked')) {
            if($(this).attr('id') === 'delivery-1') {
                $('#checkoutAddressForm').hide();
            } else {
                $('#checkoutAddressForm').show();
            }
        }
    });

    const checkoutDeliveryLabels = document.querySelector("#checkoutDeliveryLabels");
})
