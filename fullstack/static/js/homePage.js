function getPageData() {
    $.ajax({
        url: '/api/products/home',
        headers: {
            'Authorization': authToken,
        },
        success: function(data) {
            renderCart(data.cart);
            renderHeaderCategories(data.categories);
            renderHomeCategories(data.categories);
            renderHomePage(data.content);
        },
        error: function(error) {
            console.log('Err');
        }
    })
}


function renderHomePage(data) {
    $('#homePage').empty();
    data.forEach(element => {
        if (element.products.length) {
            var products = []
            element.products.forEach(product => {
                products.push(generateProductCard(product));
            })

            $('#homePage').append(
                `
                <div class="">
                    <div class="flex items-center justify-between">
                        <h2 class="text-2xl font-bold tracking-tight text-gray-900">${ element.title }</h2>
                        <a href="/catalog${ element.url }" class="text-sm duration-150 text-gray-500 hover:text-gray-600">
                            Смотреть все
                        </a>
                    </div>
                    <div class="mt-10 grid grid-cols-2 gap-y-4 gap-x-4 md:gap-x-6 md:gap-y-8 md:grid-cols-4 lg:gap-x-8 lg:gap-y-10">
                    ${ products.join('') }
                    </div>
                </div>
                `
            )
        }
    })
}


function renderHomeCategories(categories) {
    $('#homeCategoryList').empty();
    categories.forEach(category => {
        $('#homeCategoryList').append(
            `
            <a href="/catalog?category=${ category.id }" class="duration-150 group relative h-64 sm:h-96 overflow-hidden sm:aspect-w-4 sm:aspect-h-5 rounded-xl hover:opacity-75 flex flex-col xl:w-auto">
                <span aria-hidden="true" class="absolute inset-0">
                    <img src="${ category.image }" alt="" class="h-full w-full object-cover object-center">
                </span>
                <span aria-hidden="true" class="absolute inset-x-0 bottom-0 h-2/3 bg-gradient-to-t from-gray-800 opacity-50"></span>
                <span class="relative mt-auto flex justify-center items-end p-6 text-xl font-bold text-white">${ category.name }</span>
            </a>
            `
        )
    })
}


$(document).ready(function() {
    getPageData();
})
