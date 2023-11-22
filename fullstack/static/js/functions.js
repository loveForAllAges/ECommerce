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


// Отображение искусственного списка товаров, пока данные реальных товаров не будут получены
function productListPreloader(cont=$('#itemList'), count=8) {
    cont.empty();
    for (var i = 0; i < count; i++) {
        cont.append(
            `
            <div class="relative group animate-pulse">
                <div>
                    <div class="aspect-w-1 aspect-h-1 overflow-hidden rounded-xl">
                        <div class="flex items-center justify-center w-full h-full bg-gray-300 rounded">
                            <svg class="w-10 h-10 text-gray-200 dark:text-gray-600" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="currentColor" viewBox="0 0 20 18">
                                <path d="M18 0H2a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2V2a2 2 0 0 0-2-2Zm-5.5 4a1.5 1.5 0 1 1 0 3 1.5 1.5 0 0 1 0-3Zm4.376 10.481A1 1 0 0 1 16 15H4a1 1 0 0 1-.895-1.447l3.5-7A1 1 0 0 1 7.468 6a.965.965 0 0 1 .9.5l2.775 4.757 1.546-1.887a1 1 0 0 1 1.618.1l2.541 4a1 1 0 0 1 .028 1.011Z"/>
                            </svg>
                        </div>
                    </div>
                    <div class="block mt-2 text-gray-900 group-hover:text-blue-600 text-sm duration-150">
                        <div class="h-2 md:h-3 bg-gray-200 rounded-full"></div>
                    </div>
                    <p class="mt-2"><div class="h-3 md:h-4 bg-gray-200 rounded-full w-24"></div></p>
                </div>
            </div>
            `
        );
    }
}


function generateProductCardPreloader() {
    return `
        <div class="relative group animate-pulse">
            <div class="space-y-3 space">
                <div class="aspect-w-1 aspect-h-1 overflow-hidden rounded-xl">
                    <div class="flex items-center justify-center w-full h-full bg-gray-300 rounded">
                        <svg class="w-10 h-10 text-gray-200 dark:text-gray-600" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="currentColor" viewBox="0 0 20 18">
                            <path d="M18 0H2a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2V2a2 2 0 0 0-2-2Zm-5.5 4a1.5 1.5 0 1 1 0 3 1.5 1.5 0 0 1 0-3Zm4.376 10.481A1 1 0 0 1 16 15H4a1 1 0 0 1-.895-1.447l3.5-7A1 1 0 0 1 7.468 6a.965.965 0 0 1 .9.5l2.775 4.757 1.546-1.887a1 1 0 0 1 1.618.1l2.541 4a1 1 0 0 1 .028 1.011Z"/>
                        </svg>
                    </div>
                </div>
                <div class="block text-gray-900 group-hover:text-blue-600 text-sm duration-150">
                    <div class="my-1 h-3 bg-gray-200 rounded-full"></div>
                </div>
                <div>
                    <div class="my-1 h-4 bg-gray-200 rounded-full w-24"></div>
                </div>
            </div>
        </div>
    `
}


function updateHeaderCategories(categories) {
    categories.forEach(category => {
        $('#mainCategoryHeader').append(
            `
                <a href="/category/?category=${ category.id }" class="flex items-center text-sm duration-150 text-black hover:text-blue-700">${ category.name }</a>
            `
        )
    })
}