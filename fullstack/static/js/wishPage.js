const emptyWishListHTML = `
<div id="wishListEmpty" class="col-span-2 md:col-span-3 lg:col-span-4 mt-10 text-center">
    <svg class="mx-auto h-12 w-12 text-rose-400" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor">
        <path stroke-linecap="round" stroke-linejoin="round" d="M21 8.25c0-2.485-2.099-4.5-4.688-4.5-1.935 0-3.597 1.126-4.312 2.733-.715-1.607-2.377-2.733-4.313-2.733C5.1 3.75 3 5.765 3 8.25c0 7.22 9 12 9 12s9-4.78 9-12z" />
    </svg>
    <p class="mt-2 text-sm text-gray-900">Список избранного пуст</p>
</div>
`

function renderPage(data) {
    $('#wishTitle').html('Избранное');
    if (data && data.length > 0) {
        $('#wishList').empty();
        data.forEach(function(product) {
            renderProductCard(product, $('#wishList'))
        })
    } else {
        $('#wishList').html(emptyWishListHTML);
    }
}


function getPageData() {
    $.ajax({
        url: '/api/products/wish',
        headers: {
            'Authorization': token,
        },
        success: function(data) {
            renderCart(data.cart);
            renderHeaderCategories(data.categories);
            renderPage(data.content);
        },
        error: function(error) {
            console.log('Err');
        }
    })
}


$(document).ready(function() {
    getPageData()
})