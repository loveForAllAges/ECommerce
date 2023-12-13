var nextPageURL;
var nextPageProcess = false;

function getCatalogPageData(is_update, queryDict={}) {
    var queryString = formatQueryDictToStr(queryDict);
    if (is_update) {
        $('#itemList').empty();
        for (var j = 0; j < 12; j++) $('#itemList').append(productCardPreloader);
    }

    $.ajax({
        url: '/api/products?' + queryString,
        success: function(data) {
            nextPageURL = data.next;
            getProductFilters()
                .then(function(productFilters) {
                    updateFilterData(productFilters, data.queries);

                    updateQueryData(data.queries);
                    updateURL(queryDict);
            
                    if (!is_update) {
                        $('#pageContent').append(filtersModal);
                        $('#catalogTitle').html('Каталог товаров');
                        $('#catalogDesc').html('Результат по запросу:');
                        $('#catalogOrderBtn').html(`
                        <button id="sortDropdownBtn" data-dropdown-toggle="sortDropdown" data-dropdown-delay="150" type="button" class="group inline-flex justify-center items-center text-sm duration-150 font-medium text-gray-900 hover:text-blue-700">
                            Сортировать
                            <svg class="ml-2 h-4 w-4 duration-150 text-gray-400" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
                                <path fill-rule="evenodd" d="M5.23 7.21a.75.75 0 011.06.02L10 11.168l3.71-3.938a.75.75 0 111.08 1.04l-4.25 4.5a.75.75 0 01-1.08 0l-4.25-4.5a.75.75 0 01.02-1.06z" clip-rule="evenodd" />
                            </svg>
                        </button>
                        `);
                        $('#catalogFilterBtn').html(`
                        <button type="button" data-drawer-target="filtersModal" data-drawer-show="filtersModal" data-drawer-placement="right" aria-controls="filtersModal" class="space-x-2 inline-block font-medium text-sm text-gray-900 hover:text-blue-700">
                            <span>Фильтры</span>
                            <span class="filterLength font-normal text-xs text-gray-500"></span>
                        </button>
                        `)
                    }
    
                    if (data.items && data.items.length > 0) {
                        $('#itemList').empty();
                        data.items.forEach(function(product) {
                            addProductCard(product, $('#itemList'))
                        })
                    } else {
                        $('#itemList').html(`
                        <div id="itemListEmpty" class="col-span-2 md:col-span-3 lg:col-span-4 mt-10 text-center">
                            <svg class="mx-auto h-12 w-12 text-gray-400" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor">
                                <path stroke-linecap="round" stroke-linejoin="round" d="M15.75 10.5V6a3.75 3.75 0 10-7.5 0v4.5m11.356-1.993l1.263 12c.07.665-.45 1.243-1.119 1.243H4.25a1.125 1.125 0 01-1.12-1.243l1.264-12A1.125 1.125 0 015.513 7.5h12.974c.576 0 1.059.435 1.119 1.007zM8.625 10.5a.375.375 0 11-.75 0 .375.375 0 01.75 0zm7.5 0a.375.375 0 11-.75 0 .375.375 0 01.75 0z"></path>
                            </svg>
                            <p class="mt-2 text-sm text-gray-900">Ничего не найдено</p>
                            <a href="{% url 'catalog' %}" class="duration-150 text-gray-500 hover:text-gray-600 text-sm">Очистить фильтры</a>
                        </div>
                        `);
                    }
    
                    wishlistBtns = document.querySelectorAll('.wishlistBtn');
                    wishlistBtns.forEach(button => {
                        button.addEventListener('click', updateWishlist)
                    })

                    // initModals();
                    initFlowbite();
                })
                .catch(function(error) {
                    console.log('Error', error)
                })
        },
        error: function(error) {
            console.log('err', error)
        }
    })
}


function removeQuery(key, values) {
    var queryDict = getQueryDict();

    if (queryDict[key]) {
        var index = queryDict[key].indexOf(values.toString());
        if (index !== -1) {
            queryDict[key].splice(index, 1);
        }
    }

    getCatalogPageData(true, queryDict);
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



function updateFilterData(data, queries) {
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
    mainCategories.forEach(e => {
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

    getCatalogPageData(true, queryDict);
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
    getCatalogPageData(true, queryDict);
}


function loadMore() {
    nextPageProcess = true;
    for (var j = 0; j < 12; j++) $('#itemList').append(productCardPreloader);

    $.ajax({
        url: nextPageURL,
        success: function(data) {
            nextPageURL = data.next;
            $('#itemList > div:gt(-13)').remove();
            data.items.forEach(function(product) {
                addProductCard(product, $('#itemList'))
            })
            nextPageProcess = false;
        },
        error: function(err) {
            console.log('Err', err)
        }
    })
}


$(document).ready(function() {
    getCatalogPageData(false, getQueryDict());

    $(window).scroll(function () {
        if ($(window).scrollTop() + $(window).height() >= $(document).height() - 100 && !nextPageProcess && nextPageURL) {
            loadMore();
        }
    })
})