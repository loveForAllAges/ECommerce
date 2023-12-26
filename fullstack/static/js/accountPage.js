function uploadOrdersIntoAccountPage(orders) {
    if (orders.length == 0) {
        $("#accountOrderList").html(`
            <div id="wishListEmpty" class="col-span-3 md:col-span-4 lg:col-span-5 mt-10 text-center">
                <svg class="mx-auto h-12 w-12 text-gray-400" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M15.75 10.5V6a3.75 3.75 0 10-7.5 0v4.5m11.356-1.993l1.263 12c.07.665-.45 1.243-1.119 1.243H4.25a1.125 1.125 0 01-1.12-1.243l1.264-12A1.125 1.125 0 015.513 7.5h12.974c.576 0 1.059.435 1.119 1.007zM8.625 10.5a.375.375 0 11-.75 0 .375.375 0 01.75 0zm7.5 0a.375.375 0 11-.75 0 .375.375 0 01.75 0z"></path>
                </svg>
                <p class="mt-2 text-sm text-gray-900">История заказов пустая</p>
            </div>
        `);
        return;
    }
    $('#accountOrderList').empty();
    orders.slice(0, 4).forEach(order => {
        var items = '';
        order.goods.forEach((item, key) => {
            console.log(item);
            var geo = ''
            if (key == 1) {
                geo = 'left-auto'
            } else if (key == 2) {
                geo = 'top-auto'
            } else if (key == 3) {
                geo = 'top-auto left-auto'
            }
            items += `
            <div class="absolute ${ geo } w-1/2 h-1/2 rounded-xl border-gray-100 p-2">
                <div class="flex items-center justify-center w-full h-full bg-gray-300 rounded-xl">
                    <img src="${ item.product.images[0] }" class="h-full w-full object-cover object-center rounded-xl">
                </div>
            </div>
            `
        })

        var statusColor = 'blue';
        if (order.status.id == 1) statusColor = 'green'
        else if (order.status.id == 2) statusColor = 'red'
        else if (order.status.id == 3) statusColor = 'yellow'

        $('#accountOrderList').append(`
        <li class="group relative">
            <div class="relative aspect-w-1 aspect-h-1 rounded-xl bg-gray-50">
                ${ items }
                <div class="absolute left-2 top-1">
                    <span class="inline-flex items-center rounded-lg bg-${ statusColor }-100 px-2 py-0.5 text-xs font-medium text-${ statusColor }-800">
                        <svg class="mr-1.5 h-2 w-2 text-${ statusColor }-400" fill="currentColor" viewBox="0 0 8 8">
                        <circle cx="4" cy="4" r="3" />
                        </svg>
                        ${ order.status.name }
                    </span>
                </div>
            </div>
            <a href="${ order.url }" class="block mt-2 text-gray-900 group-hover:text-blue-600 text-sm duration-150">
                <span aria-hidden="true" class="absolute inset-0"></span>
                Заказ #${ order.number }
            </a>
            <p class="mt-1 text-gray-900 font-medium">${ order.total_price.toLocaleString('ru-RU') } ₽</p>
        </li>
        `)
    });
}


function getPageData() {
    $.ajax({
        url: '/api/auth/account',
        success: function(data) {
            console.log(data);
            renderCart(data.cart);
            renderHeaderCategories(data.categories);
            $('#accountName').html(data.content.full_name);
            $('#accountEmail').html(data.content.email);
            $('#accountWelcomeText').html('Добро пожаловать,');
            $('#accountOrderTitle').html(`Заказы<span class="text-sm text-gray-500 font-normal ml-2">${ data.content.orders.length }</span>`);
            $('#accountOrderDesc').html('История ваших заказов');
            $('#accountMenu').removeClass('hidden');
            uploadOrdersIntoAccountPage(data.content.orders);
            if (data.content.is_staff) {
                addAdmBtn();
            }
        },
        error: function(error) {
        }
    })
}


function logout() {
    authToken = '';
    $.ajax({
        url: '/api/auth/logout',
        type: 'POST',
        headers: {
            'X-CSRFToken': csrftoken,
        },
        success: function(data) {
            location.replace(data.redirect_url);
        },
        error: function(error) {
            console.log(error);
        }
    })
}

$(document).ready(function() {
    getPageData();
})
