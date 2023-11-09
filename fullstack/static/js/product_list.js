var editProductBtns = document.querySelectorAll(".editProduct");
var productModal = document.querySelector("#productModal");
var productModalForm = document.querySelector("#productModalForm");

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

productModalForm.addEventListener('click', function(event) {
    event.preventDefault()
    console.log('modal sended')
})

