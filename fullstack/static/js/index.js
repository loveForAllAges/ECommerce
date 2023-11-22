var mainCategories = [];

function getMainCategories() {
    $.ajax({
        url: '/api/main-categories',
        success: function(data) {
            mainCategories = data;

            updateHeaderCategories(data);

            if ($('#homePage')[0]) {
                updateHomeCategories(data);
            }
        },
        error: function(error) {
            console.log('Error')
        }
    })
}


getMainCategories();


$(document).ready(function(){
    getCart();
    if ($('#homePage')[0]) {
        homeCategoriesPreview();
    }
})
