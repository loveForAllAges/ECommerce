function showToast(message) {
    const toastMessage = document.getElementById('toastMessage');
    if (toastMessage.childElementCount) {
        toastMessage.removeChild();
    }
    let toast = document.createElement('div');
    toast.innerHTML = `
    <div class="pointer-events-none fixed inset-0 flex items-center justify-center z-50">
        <div class="max-w-sm pointer-events-auto cursor-default bg-black text-white text-sm py-1 px-2 rounded-lg shadow bg-opacity-75">
            <p>${message}</p>
        </div>
    </div>
    `
    toastMessage.appendChild(toast);

    setTimeout(() => {
        toast.remove();
    }, 3000)
}