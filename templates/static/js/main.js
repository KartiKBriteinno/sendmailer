document.addEventListener('DOMContentLoaded', () => {
    const statusDiv = document.getElementById('status-updates');
    if (statusDiv) {
        setInterval(() => {
            statusDiv.innerHTML = `Emails sent: ${Math.floor(Math.random() * 100)}`;
        }, 2000);
    }
});