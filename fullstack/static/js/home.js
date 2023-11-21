function getPageData() {
    $.ajax({
        url: '/api/home',
        success: function(data) {
            data.forEach(element => {
                var products = []
                element.content.forEach(product => {
                    products.push(generateProductCard(product));
                })

                $('#page').append(
                    `
                    <div class="mx-auto max-w-7xl px-4 py-24 lg:py-32 sm:px-6 lb:px-8">
                        <div class="flex items-center justify-between">
                            <h2 class="text-2xl font-bold tracking-tight text-gray-900">${ element.title }</h2>
                            <a href="${ element.url }" class="text-sm duration-150 text-gray-500 hover:text-gray-600">
                                Смотреть все
                            </a>
                        </div>
                        <div class="mt-10 grid grid-cols-2 gap-y-4 gap-x-4 md:gap-x-6 md:gap-y-8 md:grid-cols-4 lg:gap-x-8 lg:gap-y-10">
                        ${ products.join('') }
                        </div>
                    </div>
                    `
                )
            })
        },
        error: function(error) {

        }
    })
}


$(document).ready(function() {
    getPageData();
})