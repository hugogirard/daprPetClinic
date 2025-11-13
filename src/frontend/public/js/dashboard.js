// Dashboard JavaScript

// Show toast based on query parameter
function initToasts() {
    const urlParams = new URLSearchParams(window.location.search);
    const toast = urlParams.get('toast');

    if (toast === 'success') {
        Toastify({
            text: "✅ Appointment created successfully!",
            duration: 3000,
            gravity: "top",
            position: "right",
            style: {
                background: "linear-gradient(to right, #00b09b, #96c93d)",
            }
        }).showToast();
        // Clean URL
        window.history.replaceState({}, document.title, window.location.pathname);
    } else if (toast === 'cancelled') {
        Toastify({
            text: "🗑️ Appointment cancelled",
            duration: 3000,
            gravity: "top",
            position: "right",
            style: {
                background: "linear-gradient(to right, #ff5f6d, #ffc371)",
            }
        }).showToast();
        window.history.replaceState({}, document.title, window.location.pathname);
    } else if (toast === 'error') {
        Toastify({
            text: "❌ An error occurred. Please try again.",
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
