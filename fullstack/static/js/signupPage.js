function signup(e) {
    e.preventDefault();
    showLoading();
    var formData = $(this).serialize();
    $.ajax({
        url: '/api/auth/signup',
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
                $("#signup").remove();
                $("#successSignup").removeClass('hidden');
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
    getSimplePageData();

    $('#signup').submit(signup);
})