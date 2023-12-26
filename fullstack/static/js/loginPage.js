function login(e) {
    e.preventDefault();
    showLoading();
    var formData = $(this).serialize();
    $.ajax({
        url: '/api/auth/login',
        headers: {
            'X-CSRFToken': csrftoken,
        },
        type: 'POST',
        data: formData,
        success: function(data) {
            if (data.error) {
                hideLoading();
                showMessage(data.error);
            } else {
                authToken = data.token;
                location.replace(data.redirect_url);
            }
        },
        error: function(error) {
            hideLoading();
            console.log(error);
        }
    })
}


$(document).ready(function() {
    getSimplePageData();

    $('#login').submit(login);
})