$(document).ready(function(){
    var editProductBtns = document.querySelectorAll(".editProductBtn");

    function openProductModal() {
        var productId = this.dataset.id;
        
        fetch(`/api/products/${productId}/`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken,
            },
        })
        .then(response => response.json())
        .then(data => {
            $('#productName').val(data.name);
            $('#productAbout').val(data.description);
            $('#productPrice').val(data.price);
            // productModal.style.transform = 'translateX(0)';
        })
        .catch(errors => {
            console.log('err')
        })
    }

    editProductBtns.forEach(element => {
        element.addEventListener('click', openProductModal)
    })

    $('#productModalForm').submit(function(e) {
        e.preventDefault()
        const formData = new FormData(productModalForm)
        console.log('modal sended', formData.get('images'))

        // $.ajax({
        //     url: '/api/',
        //     type: 'POST',
        //     data: formData,
        //     success: function(data) {
        //         console.log('data success')
        //     },
        //     error: function(xhr, status, error) {
        //         console.log('Error', xhr, status, error)
        //     }
        // })
    })

    $('#fileUpload').change(event => {
        if (event.target.files) {
            let filesAmount = event.target.files.length;

            $('#fileList').html('');

            for (let i = 0; i < filesAmount; i++) {
                let reader = new FileReader();
                reader.onload = function(event) {
                    console.log(event.target.files)
                    $('#fileList').append(
                        `
                        <li class="p-2 border rounded-lg">
                            <div class="flex items-center space-x-4">
                                <div class="">
                                    <p class="text-sm text-gray-500 pl-2">${ i+1 }</p>
                                </div>
                                <div class="flex-shrink-0">
                                    <img class="h-12 w-12 rounded-lg" src="${ event.target.result }" alt="">
                                </div>
                                <div class="min-w-0 flex-1">
                                    <p class="truncate text-sm font-medium text-gray-900">${ event.target.name }</p>
                                    <p class="truncate text-sm text-gray-500">${ event.target.size }</p>
                                </div>
                                <div>
                                    <button type="button" class="removeProductImage inline-flex items-center rounded-full border border-gray-300 bg-white p-0.5 text-sm font-medium leading-5 text-gray-700 shadow-sm hover:bg-gray-50">
                                        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-4 h-4">
                                            <path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12" />
                                        </svg>                                          
                                    </button>
                                </div>
                            </div>
                        </li>
                        `
                    );
                }
                reader.readAsDataURL(event.target.files[i]);
            }
        }
    })

    // var removeProductImage = document.querySelectorAll('.removeProductImage');

    // removeProductImage.forEach(button => {
    //     button.addEventListener('click', function(event) {

    //     });
    // })

    // fileUpload.addEventListener('change', (e) => {
    //     let filename = e.target.files[0].name;
    //     let fileSize = (e.target.files[0].size / 1024).toFixed(1);
    //     let fileType = e.target.files[0].type.split('/')[1];

    //     $('#fileList').append(
    //         `
            // <li class="p-2 border rounded-lg">
            //     <div class="flex items-center space-x-4">
            //         <div class="">
            //             <p class="text-sm text-gray-500 pl-2">1</p>
            //         </div>
            //         <div class="flex-shrink-0">
            //             <img class="h-12 w-12 rounded-lg" src="https://images.unsplash.com/photo-1519345182560-3f2917c472ef?ixlib=rb-1.2.1&amp;ixid=eyJhcHBfaWQiOjEyMDd9&amp;auto=format&amp;fit=facearea&amp;facepad=2&amp;w=256&amp;h=256&amp;q=80" alt="">
            //         </div>
            //         <div class="min-w-0 flex-1">
            //             <p class="truncate text-sm font-medium text-gray-900">filename</p>
            //             <p class="truncate text-sm text-gray-500">filetype and filesize</p>
            //         </div>
            //         <div>
            //             <a href="#" class="inline-flex items-center rounded-full border border-gray-300 bg-white p-0.5 text-sm font-medium leading-5 text-gray-700 shadow-sm hover:bg-gray-50">
            //                 <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-4 h-4">
            //                     <path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12" />
            //                 </svg>                                          
            //             </a>
            //         </div>
            //     </div>
            // </li>
    //         `
    //     );
    // })
})

