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


function passwordReset(e) {
    e.preventDefault();
    showLoading();
    var formData = $(this).serialize();
    $.ajax({
        url: '/api/auth/password_reset',
        headers: {
            'X-CSRFToken': csrftoken,
        },
        type: 'POST',
        data: formData,
        success: function(data) {
            hideLoading();
            $("#successReset").removeClass('hidden');
            $("#passwordResetForm").addClass('hidden');
        },
        error: function(error) {
            hideLoading();
            console.log(error);
        }
    })
}


function goToPasswordResetForm() {
    $("#loginForm").addClass('hidden');
    $("#passwordResetForm").removeClass('hidden');
}


function goToLoginForm() {
    $("#loginForm").removeClass('hidden');
    $("#passwordResetForm").addClass('hidden');
}


$(document).ready(function() {
    getSimplePageData();

    $('#loginForm').submit(login);
    $('#passwordResetForm').submit(passwordReset);
})