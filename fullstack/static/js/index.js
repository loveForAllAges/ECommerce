$('#searchForm').submit(function(e) {
    e.preventDefault();
    var uri = new URL(window.location.protocol + '//' + window.location.host);
    uri.pathname += 'catalog';
    uri.searchParams.set('search', $('#searchInput').val());
    window.location.href = uri.toString();
})

$("#searchInput").on('input', function () {
    var query = $(this).val();

    if (query.length >= 2) {
        $.ajax({
            url: '/api/products/search?search=' + query,
            success: function (data) {
                $('#searchResult').empty();
                var uri = new URL(window.location.protocol + '//' + window.location.host);
                uri.pathname += 'catalog';
                if (data.length) {
                    data.forEach(function (result) {
                        uri.searchParams.set('search', result.content);
                        $('#searchResult').append('<li class="group duration-150 flex items-center rounded-xl px-3 py-2 hover:bg-gray-900 hover:bg-opacity-5 hover:text-gray-900"><a href="'+ uri.toString() +'" class="truncate flex-auto">' + result.content + '</a></li>');
                    });
                } else {
                    uri.searchParams.set('search', query);
                    $('#searchResult').append(`<li class="group duration-150 flex items-center rounded-xl px-3 py-2 hover:bg-gray-900 hover:bg-opacity-5 hover:text-gray-900"><a href="${ uri.toString() }" class="truncate flex-auto">${ query }</a></li>`);
                }
            }
        });
    } else {
        $('#searchResult').empty();
    }
});


modalBgStyles = "bg-gray-900 bg-opacity-50 fixed inset-0 z-30 z-40"

console.log('token', authToken);