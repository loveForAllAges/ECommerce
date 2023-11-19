var mainCategories = [];

function getMainCategories() {
    $.ajax({
        url: '/api/main-categories',
        success: function(data) {
            mainCategories = data;
        },
        error: function(error) {}
    })
}


getMainCategories();


$(document).ready(function(){
    // window.addEventListener("load", function () {
    //     var loader = document.getElementById("preloader");
    //     loader.style.display = "none";
    // });



    getCart();
})
