// New appointment page JavaScript

// Show toast for errors
function initToasts() {
    const flashData = window.flashMessage;
    
    if (flashData && flashData.type === 'error') {
        Toastify({
            text: `❌ ${flashData.message}`,
            duration: 3000,
            gravity: "top",
            position: "right",
            style: {
                background: "linear-gradient(to right, #eb3349, #f45c43)",
            }
        }).showToast();
    }
}

// Initialize when DOM is ready
document.addEventListener('DOMContentLoaded', function () {
    initToasts();
});
