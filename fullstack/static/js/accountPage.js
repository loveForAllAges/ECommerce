// function accountPagePreloader() {
//     $('#accountName').html('<div class="my-2.5 h-6 bg-gray-200 rounded-full w-36"></div>');
//     $('#accountEmail').html('<div class="my-1 h-3 bg-gray-200 rounded-full w-32"></div>')
//     $('#accountWelcomeText').html('<div class="my-1 h-3 bg-gray-200 rounded-full w-24"></div>')
//     $('#accountOrderTitle').html('<div class="my-1 h-4 bg-gray-200 rounded-full w-24"></div>');
//     $('#accountOrderDesc').html('<div class="my-1 h-3 bg-gray-200 rounded-full w-48"></div>');
//     $('#accountOrderList').empty();
//     for (var i = 0; i < 7; i++) {
//         var items = '';
//         for (var j = 0; j < 4; j++) {
//             var geo = ''
//             if (j == 1) {
//                 geo = 'left-auto'
//             } else if (j == 2) {
//                 geo = 'top-auto'
//             } else if (j == 3) {
//                 geo = 'top-auto left-auto'
//             }
//             items += `
//             <div class="absolute ${ geo } w-1/2 h-1/2 rounded-xl border-gray-100 p-2">
//                 <div class="flex items-center justify-center w-full h-full bg-gray-300 rounded-xl">
//                     <svg class="w-10 h-10 text-gray-200 dark:text-gray-600" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="currentColor" viewBox="0 0 20 18">
//                         <path d="M18 0H2a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2V2a2 2 0 0 0-2-2Zm-5.5 4a1.5 1.5 0 1 1 0 3 1.5 1.5 0 0 1 0-3Zm4.376 10.481A1 1 0 0 1 16 15H4a1 1 0 0 1-.895-1.447l3.5-7A1 1 0 0 1 7.468 6a.965.965 0 0 1 .9.5l2.775 4.757 1.546-1.887a1 1 0 0 1 1.618.1l2.541 4a1 1 0 0 1 .028 1.011Z"/>
//                     </svg>
//                 </div>
//             </div>
//             `
//         }
//         $('#accountOrderList').append(`
//         <li class="group relative space-y-3 animate-pulse">
//             <div class="relative aspect-w-1 aspect-h-1 rounded-xl bg-gray-50">
//             ${ items }
//             </div>
//             <div class="block text-gray-900 group-hover:text-blue-600 text-sm duration-150">
//                 <div class="my-1 h-3 bg-gray-200 rounded-full"></div>
//             </div>
//             <div>
//                 <div class="my-1 h-4 bg-gray-200 rounded-full w-24"></div>
//             </div>
//         </li>
//         `)
//     }
// }


function uploadOrdersIntoAccountPage(orders) {
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


function getAccountPageData() {
    $.ajax({
        url: '/api/account',
        success: function(data) {
            $('#accountName').html(data.full_name);
            $('#accountEmail').html(data.email);
            $('#accountWelcomeText').html('Добро пожаловать,');
            $('#accountOrderTitle').html(`Заказы<span class="text-sm text-gray-500 font-normal ml-2">${ data.orders.length }</span>`);
            $('#accountOrderDesc').html('История ваших заказов');
            $('#accountMenu').removeClass('hidden');
            uploadOrdersIntoAccountPage(data.orders);
            if (data.is_staff) {
                addAdmBtn();
            }
        },
        error: function(error) {
            
        }
    })
}


$(document).ready(function() {
    getAccountPageData();
})