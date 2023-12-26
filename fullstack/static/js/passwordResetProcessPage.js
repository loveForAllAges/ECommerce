function passwordResetProcess(e) {
    e.preventDefault();
    showLoading();
    var formData = $(this).serialize();
    var uidb64 = location.pathname.split('/')[2];
    var token = location.pathname.split('/')[3];
    $.ajax({
        url: `/api/auth/password_reset/${uidb64}/${token}/`,
        headers: {
            'X-CSRFToken': csrftoken,
        },
        type: 'POST',
        data: formData,
        success: function(data) {
            hideLoading();
            console.log('data', data);
            location.replace(data.redirect_url);
            // $("#successReset").removeClass('hidden');
            // $("#passwordResetForm").addClass('hidden');
        },
        error: function(error) {
            console.log(error);
        }
    })
}


$(document).ready(function() {
    getSimplePageData();
    $('#passwordResetProcessForm').submit(passwordResetProcess);
})