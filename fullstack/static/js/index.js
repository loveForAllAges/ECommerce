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

    var btns = document.getElementsByClassName('addToCart');
    var addToWishlistBtns = document.getElementsByClassName('addToWishlist');
    
    for(var i = 0; i < btns.length; i++){
        btns[i].addEventListener('click', function(){
            var productId = this.dataset.product;
            var action = this.dataset.action;
            var sizeId = this.dataset.size;

            fetch(`/cart/update/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrftoken,
                },
                body: JSON.stringify({
                    'productId': productId,
                    'action': action,
                    'sizeId': sizeId,
                })
            })
    
            .then(() =>{
                location.reload()
            })
        })
    }

    // for(var i = 0; i < deleteAddressBtns.length; i++){
    //     deleteAddressBtns[i].addEventListener('click', function(){
    //         var addressId = this.dataset.address;
    //         var listItem = this.parentNode;
    //         console.log(addressId);
            
    //         fetch(`/address/delete/`, {
    //             method: 'POST',
    //             headers: {
    //                 'Content-Type': 'application/json',
    //                 'X-CSRFToken': csrftoken,
    //             },
    //             body: JSON.stringify({
    //                 'addressId': addressId,
    //             })
    //         })
    
    //         .then(() =>{
    //             listItem.remove();
    //         })            
    //     })
    // }

    for(var i = 0; i < addToWishlistBtns.length; i++){
        addToWishlistBtns[i].addEventListener('click', function(){
            var productId = this.dataset.product;
            var action = this.dataset.action;
            var choice_method = 'GET';

            if (action == 'add') {
                choice_method = 'POST';
            } else if (action == 'delete') {
                choice_method = 'DELETE';
            }

            fetch(`/wishlist/`, {
                method: choice_method,
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrftoken,
                },
                body: JSON.stringify({
                    'productId': productId,
                })
            })
    
            .then(() =>{
                location.reload()
            })
        })
    }
})
