function getPageData() {
    $.ajax({
        url: '/api/auth/account/',
        success: function(data) {
            console.log(data);
            renderCart(data.cart);
            renderHeaderCategories(data.categories);
            // renderPage(data.cart);
            loadPage();
        },
        error: function(error) {
        }
    })
}


$(document).ready(function() {
    getPageData();
})
