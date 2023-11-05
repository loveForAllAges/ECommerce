$(document).ready(function(){
    window.addEventListener("load", function () {
        var loader = document.getElementById("preloader");
        loader.style.display = "none";
    });

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
                    }
                }
            });
        } else {
            $('#searchResult').empty();
        }
    });


    // $('#sortForm').on('change', 'input[type=radio]', function() {
    //     $('.products').hide();
    //     $('.waiting-products').show();

    //     var sortType = $('input[name=sort]:checked').val();

    //     $.ajax({
    //         url: '/api/products/',
    //         type: 'GET',
    //         data: { sortType: sortType },
    //         dataType: 'json',
    //         success: function(data) {
    //             console.log(data)
    //             var itemsDiv = $('.products');
    //             itemsDiv.empty();

    //             $.each(data, function(index, item) {
    //                 console.log(item);
    //                 var cardDiv = $('<div class="p"></div>').text(item.fields.name);
    //                 itemsDiv.append(cardDiv);
    //             });

    //             $('.waiting-products').hide();
    //             itemsDiv.show();
    //         },
    //         error: function() {
    //             console.log('Ошибка при запросе на сервер');
    //         }
    //     });
    // });
})
