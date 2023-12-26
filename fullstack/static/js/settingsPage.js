function renderPage(data) {
    $('#id_first_name').val(data.first_name);
    $('#id_last_name').val(data.last_name);
    $('#id_email').val(data.email);
    $('#id_phone').val(data.phone);
}


function getPageData() {
    $.ajax({
        url: '/api/auth/settings',
        headers: {
            'Authorization': authToken,
        },
        success: function(data) {
            console.log('data', data);
            renderCart(data.cart);
            renderHeaderCategories(data.categories);
            renderPage(data.content);
        },
        error: function(error) {
            console.log(error);
        }
    })
}


function settings(e) {
    e.preventDefault();
    showLoading();
    var formData = $(this).serialize();
    $.ajax({
        url: '/api/auth/settings',
        headers: {
            'X-CSRFToken': csrftoken,
        },
        type: 'POST',
        data: formData,
        success: function(data) {
            hideLoading();
            if (data.error) {
                showMessage(data.error);
            } else {
                showMessage(data.message);
            }
        },
        error: function(error) {
            hideLoading();
            var errorDict = error.responseJSON;
            console.log(errorDict);
            for (var key in errorDict) {
                showMessage(errorDict[key]);
            }
        }
    })
}


function changePasswordForm() {
    $("#changePasswordBlock").removeClass('hidden');
}


function changePassword(e) {
    e.preventDefault();
    showLoading();
    var formData = $(this).serialize();
    $.ajax({
        url: '/api/auth/change_password',
        headers: {
            'X-CSRFToken': csrftoken,
        },
        type: 'POST',
        data: formData,
        success: function(data) {
            hideLoading();
            if (data.error) {
                showMessage(data.error);
            } else {
                showMessage(data.message);
            }
        },
        error: function(error) {
            hideLoading();
            var errorDict = error.responseJSON;
            console.log(errorDict);
            for (var key in errorDict) {
                showMessage(errorDict[key]);
            }
        }
    })
}


$(document).ready(function() {
    getPageData();
    $('#settings').submit(settings);
    $('#changePassword').submit(changePassword);
})
