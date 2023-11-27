function fillProductModal(nam='', description='', price='', images=null, category='', brands=[], sizes=[]) {
    $('#productName').val(nam);
    $('#productDescription').val(description);
    $('#productPrice').val(price);

    $("#productCategory option[value='" + category + "']").prop("selected", true);

    $('#productBrand li input[type="checkbox"]').each(function() {
        var val = parseInt($(this).val(), 10);
        if ($.inArray(val, brands) !== -1) {
            $(this).prop('checked', true);
        }
    })

    $('#productSize li input[type="checkbox"]').each(function() {
        var val = parseInt($(this).val(), 10);
        if ($.inArray(val, sizes) !== -1) {
            $(this).prop('checked', true);
        }
    })
    
    if (images) {
        loadFilesFromServer(images)
            .then(function() {
                showImages();
            })
            .catch(function(error) {
                console.error('Error');
            });
    }
}


var uploadedImages = [];
var productList = [];


// function getProductList() {
//     $.ajax({
//         url: '/api/products',
//         success: function(data) {
//             productList = data;
//             if (data.items && data.items.length > 0) {
//                 $('#productList').removeClass('hidden');
//                 $('#productList').empty();
//                 data.items.forEach(function(product) {
//                     updateProductList(product)
//                 })
//             } else {
//                 $('#productList').addClass('hidden');
//                 $('#productListEmpty').removeClass('hidden');
//             }
//         },
//         error: function(error) {
//             console.log('Error')
//         }
//     })
// }


function openProductModal(productId) {
    resetProductForm();
    $('#productModalForm').append(`<input type="hidden" value="${ productId }" name="pk" id="">`)
    $.ajax({
        url: `/api/products/${productId}`,
        success: function(data) {
            fillProductModal(data.name, data.description, data.price,
                data.images, data.category, data.brand, data.sizes      
            )
        },
        error: function(error) {
            console.log('Error')
        }
    })
}


function deleteImage(i) {
    uploadedImages.splice(i, 1);
    showImages();
}


function resetProductForm() {
    $('.error-container').each(function() {
        $(this).addClass('hidden');
    })
    $('#productModalForm')[0].reset();
    $('#productModalForm input[name="pk"]').remove();
    $('#fileList').empty();
    uploadedImages = [];
}


function showImages() {
    $('#fileList').empty();
    uploadedImages.forEach((value, key) => {
        $('#fileList').append(
            `
            <li class="group aspect-1 rounded-lg relative">
                <img class="h-full w-full rounded-lg" src="${ URL.createObjectURL(value) }" alt="">
                <div class="absolute top-0 right-0 flex overflow-hidden -m-2 pt-2 pr-2">
                    <button type="button" onclick="deleteImage(${ key })" class="p-2 text-gray-400 hover:text-gray-500">               
                        <svg class="w-5 h-5" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor">
                            <path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12" />
                        </svg>
                    </button>
                </div>
            </li>
            `
        );
    })
}


function loadFilesFromServer(serverFileUrls) {
    return new Promise(function(resolve, reject) {
        var counter = 0;

        function checkCompetition() {
            counter++;
            if (counter === serverFileUrls.length) {
                resolve();
            }
        }

        serverFileUrls.forEach(function(url) {
            fetch(url)
                .then(response => response.blob())
                .then(blob => {
                    const file = new File([blob], url.substring(url.lastIndexOf('/') + 1));
                    uploadedImages.push(file);
                    checkCompetition();
                })
                .catch(error => {
                    console.error('Error');
                    checkCompetition();
                });
        });
    })
}


function updateProductList(data, update=false) {
    var inStock = (data.in_stock) ? 
    `
    <svg class="mx-auto h-5 w-5 flex-shrink-0 text-green-400" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
        <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.857-9.809a.75.75 0 00-1.214-.882l-3.483 4.79-1.88-1.88a.75.75 0 10-1.06 1.061l2.5 2.5a.75.75 0 001.137-.089l4-5.5z" clip-rule="evenodd"></path>
    </svg>
    ` : ''

    content = `
        <tr id='product-${ data.id }'>
            <td class="whitespace-nowrap py-2 pl-4 pr-3 text-sm text-gray-500 sm:pl-6">
                <div class="h-8 w-8 flex-shrink-0">
                    <img class="h-8 w-8 rounded-lg" src="${ data.images[0] }" alt="">
                </div>
            </td>
            <td class="whitespace-nowrap px-2 py-2 text-sm text-gray-500">${ data.name }</td>
            <td class="whitespace-nowrap px-2 py-2 text-sm text-gray-500 hidden lg:table-cell">${ data.description.substring(0, 24) }...</td>
            <td class="whitespace-nowrap px-2 py-2 text-sm text-gray-500 hidden lg:table-cell">${ data.category }</td>
            <td class="whitespace-nowrap px-2 py-2 text-sm text-gray-500">${ data.price.toLocaleString('ru-RU') } ₽</td>
            <td class="whitespace-nowrap px-2 py-2 text-sm text-gray-500 hidden lg:table-cell">${ inStock }</td>
            <td class="relative whitespace-nowrap py-2 pl-3 pr-4 text-right text-sm font-medium sm:pr-6">
                <div class="flex items-center justify-end">
                    <button type="button" id="productDropwownBtn-${ data.id }" data-dropdown-placement="bottom-end" data-dropdown-toggle="productDropwown-${ data.id }" data-dropdown-delay={500} class="-m-2 flex items-center rounded-full p-2 text-gray-400 hover:text-gray-600">
                        <svg class="h-5 w-5" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
                            <path d="M10 3a1.5 1.5 0 110 3 1.5 1.5 0 010-3zM10 8.5a1.5 1.5 0 110 3 1.5 1.5 0 010-3zM11.5 15.5a1.5 1.5 0 10-3 0 1.5 1.5 0 003 0z"></path>
                        </svg>
                    </button>
                </div>
                <div id="productDropwown-${ data.id }" class="z-10 hidden bg-white divide-y divide-gray-100 rounded-md shadow-lg ring-1 ring-black ring-opacity-5">
                    <ul class="p-1 space-y-1 text-sm font-normal text-gray-700" aria-labelledby="productDropwownBtn-${ data.id }">
                        <li>
                            <a href="${ data.url }" class="hover:bg-gray-100 hover:text-gray-900 duration-150 text-gray-700 flex items-center py-2 px-4 rounded-md">
                                Подробнее
                            </a>
                        </li>
                        <li>
                            <button type="button" data-drawer-target="productModal" onclick="openProductModal(${ data.id })" data-drawer-show="productModal" data-drawer-placement="right" class="hover:bg-gray-100 hover:text-gray-900 duration-150 text-gray-700 flex items-center py-2 px-4 rounded-md">
                                Редактировать
                            </button>
                        </li>
                        <li>
                            <a href="#" class="hover:bg-gray-100 hover:text-gray-900 duration-150 text-gray-700 flex items-center py-2 px-4 rounded-md">
                                Удалить
                            </a>
                        </li>
                    </ul>
                </div>
            </td>
        </tr>
        `
    
    if (update) {
        $(`#product-${ update }`).replaceWith(content);
    } else {
        $('#productList').append(content);
    }
}


function updateErrorFields(error) {
    var errors = error.responseJSON;

    $('.error-container').each(function() {
        $(this).addClass('hidden');
    })

    if (errors.name) {
        $('#productNameError').removeClass('hidden');
        $('#productNameError').text(errors.name);
    }

    if (errors.description) {
        $('#productDescriptionError').removeClass('hidden');
        $('#productDescriptionError').text(errors.description);
    }

    if (errors.price) {
        $('#productPriceError').removeClass('hidden');
        $('#productPriceError').text(errors.price);
    }

    if (errors.images) {
        $('#productImagesError').removeClass('hidden');
        $('#productImagesError').text(errors.images);
    }

    if (errors.category) {
        $('#productCategoryError').removeClass('hidden');
        $('#productCategoryError').text(errors.category);
    }

    if (errors.brand) {
        $('#productBrandError').removeClass('hidden');
        $('#productBrandError').text(errors.brand);
    }

    if (errors.size) {
        $('#productSizeError').removeClass('hidden');
        $('#productSizeError').text(errors.size);
    }
}


// function sendProductForm(event) {

// }


$(document).ready(function() {
    // getProductList();

    getProductFilters()
        .then(function(data) {
            const productFilters = data;
            data.categories.forEach(i => {
                $('#productCategory').append(
                    `<option value="${ i.id }">${ i.name }</option>`
                )
            })
            data.sizes.forEach(i => {
                $('#productSize').append(
                    `
                    <li>
                        <div class="flex items-center rounded hover:bg-gray-100">
                            <input id="size-${ i.id }" name="size" type="checkbox" value="${ i.id }" class="ml-2 w-4 h-4 text-blue-600 bg-gray-100 border-gray-300 rounded focus:ring-blue-500 focus:ring-2">
                            <label for="size-${ i.id }" class="w-full p-2 text-sm font-medium text-gray-900 rounded">${ i.name }</label>
                        </div>
                    </li>
                    `
                )
            })
            data.brands.forEach(i => {
                $('#productBrand').append(
                    `
                    <li>
                        <div class="flex items-center rounded hover:bg-gray-100">
                            <input id="brand-${ i.id }" name="brand" type="checkbox" value="${ i.id }" class="ml-2 w-4 h-4 text-blue-600 bg-gray-100 border-gray-300 rounded focus:ring-blue-500 focus:ring-2">
                            <label for="brand-${ i.id }" class="w-full p-2 text-sm font-medium text-gray-900 rounded">${ i.name }</label>
                        </div>
                    </li>
                    `
                )
            })
        })
        .catch(function(error) {
            console.log('Error')
        })

    $('#productModalForm').submit(function(e) {
        e.preventDefault();

        const formData = new FormData($('#productModalForm')[0]);
        var pk = $(this).find('input[name="pk"]');
        var method = 'POST';
        var url = '/api/products';
        var message = 'Товар создан';
        var update_id = null;
        if (pk.length > 0) {
            update_id = pk.val();
            formData.append('pk', update_id);
            method = 'PATCH';
            url = `/api/products/${update_id}`
            message = 'Изменения сохранены'
        }
        formData.append(`images`, uploadedImages);
        $.ajax({
            url: url,
            type: method,
            data: formData,
            headers: {
                'X-CSRFToken': csrftoken,
            },
            // dataType: 'json',
            processData: false,
            contentType: false,
            success: function(data) {
                updateProductList(data, update_id);
                showMessage(message);

                $('#productModalClose').click();

                initDropdowns();
            },
            error: function(error) {
                console.log(error)
                // console.log('OKOKOK', $('#productModal').isVisible())
                updateErrorFields(error);
                // button.removeAttribute('data-drawer-hide');
            }
        })
    })

    $('#fileUpload').change(event => {
        let file = $('#fileUpload')[0].files;
        console.log('files', file);
        for (let i = 0; i <  file.length; i++) {
            if (uploadedImages.every(e => e.name !== file[i].name)) uploadedImages.push(file[i]);
        }

        showImages();
    })
})

