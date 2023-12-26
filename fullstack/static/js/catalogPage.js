var nextPageURL;
var nextPageProcess = false;

function getPageData(is_update, queryDict={}) {
    var queryString = formatQueryDictToStr(queryDict);
    if (is_update) {
        $('#itemList').empty();
        for (var j = 0; j < 12; j++) $('#itemList').append(productCardPreloader);
    }

    $.ajax({
        url: '/api/products/catalog?' + queryString,
        headers: {
            'Authorization': authToken,
        },
        success: function(data) {
            nextPageURL = data.next;

            renderFilterMenu(data.categories, data.filters, data.queries);

            updateQueryData(data.queries);
            updateURL(queryDict);

            if (!is_update) {
                renderPageTitle();
                renderCart(data.cart);
                renderHeaderCategories(data.categories);    
            }

            if (data.content && data.content.length > 0) {
                $('#itemList').empty();
                data.content.forEach(function(product) {
                    renderProductCard(product, $('#itemList'))
                })
            } else {
                $('#itemList').html(emptyCatalogHTML);
            }

            // initModals();
            // initFlowbite();
        },
        error: function(error) {
            console.log('err', error)
        }
    })
}


function renderPageTitle() {
    $('#catalogTitle').html('Каталог товаров');
    $('#catalogDesc').html('Результат по запросу:');
    $('#catalogSortBtnPreloader')[0].classList.add('hidden');
    $('#catalogSortBtn')[0].classList.remove('hidden');
    $('#catalogFilterBtnPreloader')[0].classList.add('hidden');
    $('#catalogFilterBtn')[0].classList.remove('hidden');
}


function removeQuery(key, values) {
    var queryDict = getQueryDict();

    if (queryDict[key]) {
        var index = queryDict[key].indexOf(values.toString());
        if (index !== -1) {
            queryDict[key].splice(index, 1);
        }
    }

    getPageData(true, queryDict);
}


function updateQueryData(data) {
    $('#queryList').empty();
    $.each(data, function(key, value) {
        if (value[2].length > 0) {
            $('#queryList').append(
                `
                <span class="inline-flex items-center rounded-full bg-blue-100 py-0.5 pl-2 pr-0.5 text-xs font-medium text-blue-700">
                    ${value[2]}
                    <button onclick="removeQuery('${value[0]}', '${value[1]}')" type="button" class="ml-0.5 inline-flex h-4 w-4 flex-shrink-0 items-center justify-center rounded-full text-blue-400 hover:bg-blue-200 hover:text-blue-500 focus:bg-blue-500 focus:text-white focus:outline-none">
                      <svg class="h-2 w-2" stroke="currentColor" fill="none" viewBox="0 0 8 8">
                        <path stroke-linecap="round" stroke-width="1.5" d="M1 1l6 6m0-6L1 7" />
                      </svg>
                    </button>
                </span>
                `
            );
        }
    });
}



function renderFilterMenu(categories, data, queries) {
    function isValueInQueries(key, value) {
        for (let i = 0; i < queries.length; i++) {
            if (queries[i][0] === key && parseInt(queries[i][1]) === value) {
                return true;
            }
        }
        return false;
    }

    function manageCounter(cls, value) {
        if (value) {
            cls.text(value);
        } else {
            cls.text('');
        }
    }

    var count = 0;
    var subCount = 0;

    $('#mainCategoryList').empty();
    categories.forEach(e => {
        var isChecked = (isValueInQueries('category', e.id)) ? 'checked' : '';
        subCount = (isChecked) ? subCount + 1 : subCount;
        $('#mainCategoryList').append(
            `
            <div class="-my-1 flex items-center"> 
                <input ${ isChecked } id="category-${ e.id }" name="category" value="${ e.id }" type="checkbox" class="h-4 w-4 rounded border-gray-300 text-blue-600 focus:ring-offset-0 focus:ring-0">
                <label for="category-${ e.id }" class="pl-3 py-1 text-sm text-gray-500">${ e.name }</label>
            </div>
            `
        )
    })
    manageCounter($('#categoryParamLength'), subCount)
    count += subCount;
    subCount = 0;

    $('#categoryList').empty();
    data.categories.forEach(e => {
        var isChecked = (isValueInQueries('category', e.id)) ? 'checked' : '';
        subCount = (isChecked) ? subCount + 1 : subCount;
        $('#categoryList').append(
            `
            <div class="-my-1 flex items-center">
                <input ${ isChecked } id="category-${ e.id }" name="category" value="${ e.id }" type="checkbox" class="h-4 w-4 rounded border-gray-300 text-blue-600 focus:ring-offset-0 focus:ring-0">
                <label for="category-${ e.id }" class="pl-3 py-1 text-sm text-gray-500">${ e.name }</label>
            </div>
            `
        )
    })
    manageCounter($('#typeParamLength'), subCount)
    count += subCount;
    subCount = 0;
    $('#brandList').empty();
    data.brands.forEach(e => {
        var isChecked = (isValueInQueries('brand', e.id)) ? 'checked' : '';
        subCount = (isChecked) ? subCount + 1 : subCount;
        $('#brandList').append(
            `
            <div class="-my-1 flex items-center">
                <input ${ isChecked } id="brand-${ e.id }" name="brand" value="${ e.id }" type="checkbox" class="h-4 w-4 rounded border-gray-300 text-blue-600 focus:ring-offset-0 focus:ring-0">
                <label for="brand-${ e.id }" class="pl-3 py-1 text-sm text-gray-500">${ e.name }</label>
            </div>
            `
        )
    })
    manageCounter($('#brandParamLength'), subCount)
    count += subCount;
    subCount = 0;
    $('#sizeList').empty();
    data.sizes.forEach(e => {
        var isChecked = (isValueInQueries('size', e.id)) ? 'checked' : '';
        subCount = (isChecked) ? subCount + 1 : subCount;
        $('#sizeList').append(
            `
            <div class="-my-1 flex items-center">
                <input ${ isChecked } id="size-${ e.id }" name="size" value="${ e.id }" type="checkbox" class="h-4 w-4 rounded border-gray-300 text-blue-600 focus:ring-offset-0 focus:ring-0">
                <label for="size-${ e.id }" class="pl-3 py-1 text-sm text-gray-500">${ e.name }</label>
            </div>
            `
        )
    })
    manageCounter($('#sizeParamLength'), subCount)
    count += subCount;
    manageCounter($('.filterLength'), count)
}


function updateURL(queryDict) {
    var queryString = formatQueryDictToStr(queryDict);
    var newUrl = window.location.href.split('?')[0] + '?' + queryString;
    history.pushState({}, '', newUrl);
}


function updateFilters() {
    var filterLength = 0;
    var queryDict = {};
    $('input[type="checkbox"]:checked').each(function() {
        var key = $(this).attr('name');
        var value = $(this).val();
        if (!Array.isArray(queryDict[key])) {
            queryDict[key] = [value];
        } else {
            queryDict[key].push(value);
        }
        filterLength++;
    })

    var urlParams = new URLSearchParams(window.location.search);

    var searchQuery = urlParams.get('search')
    if (searchQuery) {
        queryDict['search'] = [searchQuery];
    }

    var sortQuery = urlParams.get('sort')
    if (sortQuery) {
        queryDict['sort'] = [sortQuery];
    }

    getPageData(true, queryDict);
}


function formatQueryDictToStr(queryDict) {
    var queryString = '';
    $.each(queryDict, function(name, values) {
        if (values.length > 0) {
            if (queryString !== '') {
                queryString += '&';
            }
            queryString += name + '=' + values.join(',');
        }
    });
    return queryString;
}


function getQueryDict() {
    var currentUrl = window.location.href;
    var urlParts = currentUrl.split('?');
    var query = urlParts[1];

    var queryDict = {};
    if (query) {
        var queryParams = query.split('&');
        for (var i = 0; i < queryParams.length; i++) {
            var param = queryParams[i].split('=');
            var paramName = decodeURIComponent(param[0]);
            var paramValue = decodeURIComponent(param[1]);
            if (queryDict[paramName]) {
                queryDict[paramName].push(paramValue.split(','));
            } else {
                queryDict[paramName] = paramValue.split(',');
            }
        }
    }
    return queryDict;
}


function sortProductList(key, button) {
    var sortProductListBtns = document.querySelectorAll('.sortProductListBtn');
    sortProductListBtns.forEach(e => {
        e.classList.remove('text-gray-900', 'font-medium', 'bg-gray-100');
    })
    button.classList.add('text-gray-900', 'font-medium', 'bg-gray-100');
    
    var queryDict = getQueryDict();
    queryDict['sort'] = [key];
    getPageData(true, queryDict);
}


function loadMore() {
    nextPageProcess = true;
    for (var j = 0; j < 12; j++) $('#itemList').append(productCardPreloader);

    $.ajax({
        url: nextPageURL,
        success: function(data) {
            nextPageURL = data.next;
            $('#itemList > div:gt(-13)').remove();
            data.content.forEach(function(product) {
                renderProductCard(product, $('#itemList'))
            })
            nextPageProcess = false;
        },
        error: function(err) {
            console.log('Err', err)
        }
    })
}


$(document).ready(function() {
    getPageData(false, getQueryDict());

    $(window).scroll(function () {
        if ($(window).scrollTop() + $(window).height() >= $(document).height() - 100 && !nextPageProcess && nextPageURL) {
            loadMore();
        }
    })
})