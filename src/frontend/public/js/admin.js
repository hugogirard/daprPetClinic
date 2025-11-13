// Admin panel JavaScript

// Show toast based on query parameter
function initToasts() {
    const urlParams = new URLSearchParams(window.location.search);
    const toast = urlParams.get('toast');
    const message = urlParams.get('message');

    if (toast === 'success') {
        Toastify({
            text: "✅ " + (message || "Operation successful!"),
            duration: 3000,
            gravity: "top",
            position: "right",
            style: {
                background: "linear-gradient(to right, #00b09b, #96c93d)",
            }
        }).showToast();
        window.history.replaceState({}, document.title, window.location.pathname);
    } else if (toast === 'error') {
        Toastify({
            text: "❌ " + (message || "An error occurred"),
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

async function searchAppointments() {
    const email = document.getElementById('searchEmail').value.trim();
    const resultsDiv = document.getElementById('searchResults');
    const appointmentsList = document.getElementById('appointmentsList');
    const loadingSpinner = document.getElementById('loadingSpinner');

    if (!email) {
        Toastify({
            text: "⚠️ Please enter an email address",
            duration: 2000,
            gravity: "top",
            position: "right",
            style: {
                background: "linear-gradient(to right, #ff5f6d, #ffc371)",
            }
        }).showToast();
        return;
    }

    // Show loading
    resultsDiv.style.display = 'none';
    loadingSpinner.style.display = 'block';

    try {
        const response = await fetch(`/admin/search?email=${encodeURIComponent(email)}`);
        const data = await response.json();

        loadingSpinner.style.display = 'none';

        if (data.success && data.appointments.length > 0) {
            appointmentsList.innerHTML = data.appointments.map(apt => `
                <div class="appointment-result-card">
                    <div class="appointment-result-header">
                        <div>
                            <div class="result-id">ID: ${apt.id}</div>
                            <div class="result-date">${new Date(apt.appointmentDate).toLocaleString('en-US', {
                weekday: 'long',
                year: 'numeric',
                month: 'long',
                day: 'numeric',
                hour: '2-digit',
                minute: '2-digit'
            })}</div>
                        </div>
                        <button class="btn-copy" onclick="copyToClipboard('${apt.id}')">
                            📋 Copy ID
                        </button>
                    </div>
                    <div class="appointment-result-details">
                        <div class="detail-row">
                            <span class="detail-label">Pet:</span>
                            <span>${apt.animal.name} (${apt.animal.type})</span>
                        </div>
                        <div class="detail-row">
                            <span class="detail-label">Owner:</span>
                            <span>${apt.owner.name}</span>
                        </div>
                        <div class="detail-row">
                            <span class="detail-label">Reason:</span>
                            <span>${apt.reason}</span>
                        </div>
                        ${apt.notes ? `
                        <div class="detail-row">
                            <span class="detail-label">Notes:</span>
                            <span>${apt.notes}</span>
                        </div>
                        ` : ''}
                    </div>
                </div>
            `).join('');
            resultsDiv.style.display = 'block';
        } else if (data.success && data.appointments.length === 0) {
            appointmentsList.innerHTML = `
                <div class="empty-result">
                    <p>No appointments found for ${email}</p>
                </div>
            `;
            resultsDiv.style.display = 'block';
        } else {
            Toastify({
                text: "❌ " + (data.error || "Failed to search appointments"),
                duration: 3000,
                gravity: "top",
                position: "right",
                style: {
                    background: "linear-gradient(to right, #eb3349, #f45c43)",
                }
            }).showToast();
        }
    } catch (error) {
        loadingSpinner.style.display = 'none';
        Toastify({
            text: "❌ Failed to search appointments",
            duration: 3000,
            gravity: "top",
            position: "right",
            style: {
                background: "linear-gradient(to right, #eb3349, #f45c43)",
            }
        }).showToast();
    }
}

function copyToClipboard(appointmentId) {
    navigator.clipboard.writeText(appointmentId).then(() => {
        // Also paste into the charge input
        document.getElementById('appointmentId').value = appointmentId;

        Toastify({
            text: "✅ Appointment ID copied to clipboard!",
            duration: 2000,
            gravity: "top",
            position: "right",
            style: {
                background: "linear-gradient(to right, #00b09b, #96c93d)",
            }
        }).showToast();

        // Scroll to charge section
        document.querySelector('.section:nth-of-type(3)').scrollIntoView({ behavior: 'smooth' });
    }).catch(() => {
        Toastify({
            text: "❌ Failed to copy to clipboard",
            duration: 2000,
            gravity: "top",
            position: "right",
            style: {
                background: "linear-gradient(to right, #eb3349, #f45c43)",
            }
        }).showToast();
    });
}

// Initialize when DOM is ready
document.addEventListener('DOMContentLoaded', function () {
    initToasts();

    // Allow search on Enter key
    const searchInput = document.getElementById('searchEmail');
    if (searchInput) {
        searchInput.addEventListener('keypress', function (e) {
            if (e.key === 'Enter') {
                searchAppointments();
            }
        });
    }
});
