// Dashboard JavaScript

// Show toast based on flash message from server
function initToasts() {
    const flashData = window.flashMessage;
    
    if (flashData && flashData.type && flashData.message) {
        let background;
        let icon;
        
        switch(flashData.type) {
            case 'success':
                background = "linear-gradient(to right, #00b09b, #96c93d)";
                icon = "✅";
                break;
            case 'cancelled':
                background = "linear-gradient(to right, #ff5f6d, #ffc371)";
                icon = "🗑️";
                break;
            case 'error':
                background = "linear-gradient(to right, #eb3349, #f45c43)";
                icon = "❌";
                break;
            default:
                background = "linear-gradient(to right, #4facfe, #00f2fe)";
                icon = "ℹ️";
        }
        
        Toastify({
            text: `${icon} ${flashData.message}`,
            duration: 3000,
            gravity: "top",
            position: "right",
            style: { background }
        }).showToast();
    }
}

// Initialize when DOM is ready
document.addEventListener('DOMContentLoaded', function () {
    initToasts();
});
