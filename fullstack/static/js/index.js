$(document).ready(function(){
    window.addEventListener("load", function () {
        var loader = document.getElementById("preloader");
        loader.style.display = "none";
    });

    $('.searchModal').on('click', function() {
        const searchInput = document.getElementById('searchInput');
        searchInput.focus();
    })

    $("#searchInput").on('input', function () {
        var query = $(this).val();

        if (query.length >= 2) {
            $.ajax({
                url: '/api/search/',
                data: { q: query },
                dataType: 'json',
                success: function (data) {
                    $('#searchResult').empty();
                    if (data.result.length !== 0) {
                        data.result.forEach(function (result) {
                            $('#searchResult').append('<li class="group duration-150 flex items-center rounded-xl px-3 py-2 hover:bg-gray-900 hover:bg-opacity-5 hover:text-gray-900"><a href="/category/?q='+ encodeURIComponent(result.request) +'" class="truncate flex-auto">' + result.request + '</a></li>');
                        });
                    } else {
                        $('#searchResult').append('<li class="group duration-150 flex items-center rounded-xl px-3 py-2 hover:bg-gray-900 hover:bg-opacity-5 hover:text-gray-900"><a href="/category/?search='+ encodeURIComponent(query) +'" class="truncate flex-auto">' + query + '</a></li>');
                    }
                }
            });
        } else {
            $('#searchResult').empty();
        }
    });

    getCart();
})
