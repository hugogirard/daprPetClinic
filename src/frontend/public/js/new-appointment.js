// New appointment page JavaScript

// Show toast for errors
function initToasts() {
    const urlParams = new URLSearchParams(window.location.search);
    const toast = urlParams.get('toast');

    if (toast === 'error') {
        Toastify({
            text: "❌ Failed to create appointment. Please try again.",
            duration: 3000,
            gravity: "top",
            position: "right",
            style: {
                background: "linear-gradient(to right, #eb3349, #f45c43)",
            }
        }).showToast();
        window.history.replaceState({}, document.title, window.location.pathname);
    }
}

// Initialize when DOM is ready
document.addEventListener('DOMContentLoaded', function () {
    initToasts();
});
