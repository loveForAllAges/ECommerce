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
        const productModalForm = document.querySelector('#productModalForm');
        const formData = new FormData(productModalForm)

        $.ajax({
            url: '/api/products/',
            type: 'POST',
            data: formData,
            headers: {
                'X-CSRFToken': csrftoken,
            },
            dataType: 'json',
            processData: false,
            // contentType: false,
            success: function(data) {
                console.log('data success', data)
            },
            error: function(xhr, status, error) {
                console.log('Error', xhr, status, error)
            }
        })
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
                        <li class="group aspect-1 rounded-lg">
                            <img class="h-full w-full rounded-lg" src="${ event.target.result }" alt="">
                        </li>
                        `
                    );
                }
                reader.readAsDataURL(event.target.files[i]);
            }
        }
    })
})

