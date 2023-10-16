

let toast = document.querySelector('.toast');

function showToast() {
    toast.style.display = 'block';
}

function hideToast() {
    toast.style.display = 'none';
}

toast.querySelector('.toast-close').addEventListener('click', hideToast);
setTimeout(function() {
    toast.classList.add('hidden');
}, 30000);

showToast();


