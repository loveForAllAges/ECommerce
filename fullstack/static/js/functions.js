function getProductFilters() {
    return new Promise(function(resolve, reject) {
        $.ajax({
            url: '/api/product-filters',
            method: 'GET',
            success: function(data) {
                resolve(data);
            },
            error: function(error) {
                reject(false);
            }
        })
    })
}



var user = '{{ request.user }}';

function getToken() {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            if (cookie.substring(0, 'csrftoken'.length + 1) === ('csrftoken' + '=')) {
                cookieValue = decodeURIComponent(cookie.substring('csrftoken'.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

const csrftoken = getToken();



function showMessage(message) {
    const toastMessage = document.getElementById('toastMessage');
    if (toastMessage.childElementCount) {
        toastMessage.innerHTML = '';
    }
    let toast = document.createElement('div');
    toast.innerHTML = `
    <div class="pointer-events-none fixed inset-0 flex items-center justify-center z-50">
        <div class="max-w-sm pointer-events-auto cursor-default bg-black text-white text-sm py-1 px-2 rounded-lg shadow bg-opacity-75">
            <p>${message}</p>
        </div>
    </div>
    `
    toastMessage.appendChild(toast);

    setTimeout(() => {
        toast.remove();
    }, 3000)
}