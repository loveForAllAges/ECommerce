function homePagePreview() {
    $('#homePage').empty();
    for (var i = 0; i < 2; i++) {
        var products = [];
        for (var j = 0; j < 4; j++) products.push(generateProductCardPreloader());
        $('#homePage').append(
            `
            <div class="">
                <div class="flex items-center justify-between">
                    <div class="my-1.5 h-5 bg-gray-200 rounded-full w-32"></div>
                    <div class="my-1 h-3 bg-gray-200 rounded-full w-24"></div>
                </div>
                <div class="mt-10 grid grid-cols-2 gap-y-4 gap-x-4 md:gap-x-6 md:gap-y-8 md:grid-cols-4 lg:gap-x-8 lg:gap-y-10">
                ${ products.join('') }
                </div>
            </div>
            `
        );
    }
}


function homeCategoriesPreview() {
    for (var i = 0; i < 2; i++) {
        $('#homeCategoryList').append(
            `
            <div class="animate-pulse group relative h-64 sm:h-96 overflow-hidden sm:aspect-w-4 sm:aspect-h-5 rounded-xl flex flex-col xl:w-auto">
                <span aria-hidden="true" class="absolute inset-0">
                    <div class="flex items-center justify-center w-full h-full bg-gray-300 rounded">
                        <svg class="w-10 h-10 text-gray-200 dark:text-gray-600" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="currentColor" viewBox="0 0 20 18">
                            <path d="M18 0H2a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2V2a2 2 0 0 0-2-2Zm-5.5 4a1.5 1.5 0 1 1 0 3 1.5 1.5 0 0 1 0-3Zm4.376 10.481A1 1 0 0 1 16 15H4a1 1 0 0 1-.895-1.447l3.5-7A1 1 0 0 1 7.468 6a.965.965 0 0 1 .9.5l2.775 4.757 1.546-1.887a1 1 0 0 1 1.618.1l2.541 4a1 1 0 0 1 .028 1.011Z"/>
                        </svg>
                    </div>
                </span>
            </div>
            `
        );
    }
}


function getPageData() {
    homePagePreview();
    $.ajax({
        url: '/api/home',
        success: function(data) {
            $('#homePage').empty();
            data.forEach(element => {
                if (element.content.length) {
                    var products = []
                    element.content.forEach(product => {
                        products.push(generateProductCard(product));
                    })
    
                    $('#homePage').append(
                        `
                        <div class="">
                            <div class="flex items-center justify-between">
                                <h2 class="text-2xl font-bold tracking-tight text-gray-900">${ element.title }</h2>
                                <a href="/catalog/${ element.url }" class="text-sm duration-150 text-gray-500 hover:text-gray-600">
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

            findWishlistBtns();
        },
        error: function(error) {

        }
    })
}

function updateHomeCategories(categories) {
    $('#homeCategoryList').empty();
    categories.forEach(category => {
        $('#homeCategoryList').append(
            `
            <a href="/catalog?category=${ category.id }" class="duration-150 group relative h-64 sm:h-96 overflow-hidden sm:aspect-w-4 sm:aspect-h-5 rounded-xl hover:opacity-75 flex flex-col xl:w-auto">
                <span aria-hidden="true" class="absolute inset-0">
                    <img src="${ category.url }" alt="" class="h-full w-full object-cover object-center">
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