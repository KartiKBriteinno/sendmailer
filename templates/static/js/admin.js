document.addEventListener('DOMContentLoaded', () => {
    // Add confirmation for ban action
    const banButtons = document.querySelectorAll('button[value="ban"]');
    banButtons.forEach(button => {
        button.addEventListener('click', (e) => {
            if (!confirm('Are you sure you want to ban this user?')) {
                e.preventDefault();
            }
        });
    });
});