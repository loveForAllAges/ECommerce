$(document).ready(function(){
    const sortItemsBtn = document.querySelectorAll('.sortItemsBtn');

    function sortItems() {
        console.log('clickll')
    }

    sortItemsBtn.forEach(element => {
        element.addEventListener('click', sortItems)
    })
})