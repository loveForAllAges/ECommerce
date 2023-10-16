$(document).ready(function(){
    $('input[name="delivery"]').change(function() {
        if($(this).is(':checked')) {
            if($(this).attr('id') === 'delivery-1') {
                $('#address-form-part').hide();
            } else {
                $('#address-form-part').show();
            }
        }
    });
})
