// Функция которая реагирует на нажатие кнопок сортировки.
function sortProductList(key, button) {
    var sortProductListBtns = document.querySelectorAll('.sortProductListBtn');
    sortProductListBtns.forEach(e => {
        e.classList.remove('text-gray-900', 'font-medium', 'bg-gray-100');
    })
    button.classList.add('text-gray-900', 'font-medium', 'bg-gray-100');
    
    var queryDict = getQueryDict();
    queryDict['sort'] = [key];
    updatePageData(queryDict);
}



// Получение списка товаров, категорий, размеров, брендов. Обновление Списка товаров, фильтров, запросов.
function updatePageData(queryDict={}) {
    var queryString = formatQueryDictToStr(queryDict);
    productListPreloader();
    $.ajax({
        url: '/api/products?' + queryString,
        method: 'GET',
        success: function(data) {
            if (data.items && data.items.length > 0) {
                $('#itemList').removeClass('hidden');
                $('#itemList').empty();
                data.items.forEach(function(product) {
                    addProductCard(product, $('#itemList'))
                })
            } else {
                $('#itemList').addClass('hidden');
                $('#itemListEmpty').removeClass('hidden');
            }

            updateFilterData(data.form, data.queries);
            updateQueryData(data.queries);
            updateURL(queryDict);

            wishlistBtns = document.querySelectorAll('.wishlistBtn');
            wishlistBtns.forEach(button => {
                button.addEventListener('click', updateWishlist)
            })
        },
        error: function(error) {
            console.log('err', error)
        }
    })
}



// Отображение искусственного списка товаров, пока данные реальных товаров не будут получены
function productListPreloader() {
    $('#itemList').empty();
    for (var i = 0; i < 8; i++) {
        $('#itemList').append(
            `
            <div class="relative group animate-pulse">
                <div>
                    <div class="aspect-w-1 aspect-h-1 overflow-hidden rounded-xl">
                        <div class="flex items-center justify-center w-full h-full bg-gray-300 rounded">
                            <svg class="w-10 h-10 text-gray-200 dark:text-gray-600" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="currentColor" viewBox="0 0 20 18">
                                <path d="M18 0H2a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2V2a2 2 0 0 0-2-2Zm-5.5 4a1.5 1.5 0 1 1 0 3 1.5 1.5 0 0 1 0-3Zm4.376 10.481A1 1 0 0 1 16 15H4a1 1 0 0 1-.895-1.447l3.5-7A1 1 0 0 1 7.468 6a.965.965 0 0 1 .9.5l2.775 4.757 1.546-1.887a1 1 0 0 1 1.618.1l2.541 4a1 1 0 0 1 .028 1.011Z"/>
                            </svg>
                        </div>
                    </div>
                    <div class="block mt-2 text-gray-900 group-hover:text-blue-600 text-sm duration-150">
                        <div class="h-2 md:h-3 bg-gray-200 rounded-full"></div>
                    </div>
                    <p class="mt-1"><div class="h-3 md:h-4 bg-gray-200 rounded-full w-24"></div></p>
                </div>
            </div>
            `
        );
    }
}



// Обновление данных фильтров. Необходимы: список брендов, размеров, категорий. А также список выбранных брендов, размеров, категорий.
// Функция обновления полей фильтров. Запускается при загрузке страницы
// и при удалении запросов.
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
            <div class="flex items-center">
                <input ${ isChecked } id="category-${ e.id }" name="category" value="${ e.id }" type="checkbox" class="h-4 w-4 rounded border-gray-300 text-blue-600 focus:ring-blue-500">
                <label for="category-${ e.id }" class="ml-3 text-sm text-gray-500">${ e.name }</label>
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
            <div class="flex items-center">
                <input ${ isChecked } id="category-${ e.id }" name="category" value="${ e.id }" type="checkbox" class="h-4 w-4 rounded border-gray-300 text-blue-600 focus:ring-blue-500">
                <label for="category-${ e.id }" class="ml-3 text-sm text-gray-500">${ e.name }</label>
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
            <div class="flex items-center">
                <input ${ isChecked } id="brand-${ e.id }" name="brand" value="${ e.id }" type="checkbox" class="h-4 w-4 rounded border-gray-300 text-blue-600 focus:ring-blue-500">
                <label for="brand-${ e.id }" class="ml-3 text-sm text-gray-500">${ e.name }</label>
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
            <div class="flex items-center">
                <input ${ isChecked } id="size-${ e.id }" name="size" value="${ e.id }" type="checkbox" class="h-4 w-4 rounded border-gray-300 text-blue-600 focus:ring-blue-500">
                <label for="size-${ e.id }" class="ml-3 text-sm text-gray-500">${ e.name }</label>
            </div>
            `
        )
    })
    manageCounter($('#sizeParamLength'), subCount)
    count += subCount;
    manageCounter($('.filterLength'), count)
}

// Получение выбранных фильтров
function getActiveFilters() {
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

    return queryDict;
}


// Получение списка GET URL запросов.
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

// Форматирование словаря запросов в строку.
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

// Обновление списка GET URL запросов.
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

// Функция которая отрабатывает когда пользователь нажимает на удаление GET параметра.
// Она получает словарь запросов, удаляет нужное, обновляет URL, форматирует словарь в строку и обновляет список товаров.
function removeQuery(key, values) {
    var queryDict = getQueryDict();

    if (queryDict[key]) {
        var index = queryDict[key].indexOf(values.toString());
        if (index !== -1) {
            queryDict[key].splice(index, 1);
        }
    }

    updatePageData(queryDict);
}



function updateURL(queryDict) {
    var queryString = formatQueryDictToStr(queryDict);
    var newUrl = window.location.href.split('?')[0] + '?' + queryString;
    history.pushState({}, '', newUrl);
}



$(document).ready(function() {
    var queryDict = getQueryDict();
    updatePageData(queryDict);

    $('#filtersBtn').click(function() {
        var queryDict = getActiveFilters();
        console.log('queryDict', queryDict);
        updatePageData(queryDict);
    })
})
