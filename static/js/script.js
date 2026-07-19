document.addEventListener('DOMContentLoaded', () => {
    // 1. Mobile Sidebar Toggle
    const menuToggle = document.getElementById('menu-toggle');
    const sidebar = document.querySelector('.sidebar');
    const mainWrapper = document.querySelector('.main-wrapper');

    if (menuToggle && sidebar) {
        menuToggle.addEventListener('click', (e) => {
            e.stopPropagation();
            sidebar.classList.toggle('active');
        });

        // Close sidebar when clicking outside on mobile
        document.addEventListener('click', (e) => {
            if (sidebar.classList.contains('active') && !sidebar.contains(e.target) && e.target !== menuToggle) {
                sidebar.classList.remove('active');
            }
        });
    }

    // 2. Alert Dismissal Animation
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        const closeBtn = alert.querySelector('.alert-close');
        if (closeBtn) {
            closeBtn.addEventListener('click', () => {
                dismissAlert(alert);
            });
        }

        // Auto-dismiss after 6 seconds
        setTimeout(() => {
            dismissAlert(alert);
        }, 6000);
    });

    function dismissAlert(alert) {
        alert.style.transition = 'opacity 0.3s ease, transform 0.3s ease';
        alert.style.opacity = '0';
        alert.style.transform = 'translateY(-10px)';
        setTimeout(() => {
            alert.remove();
        }, 300);
    }

    // 3. Custom Delete Confirmation Modal
    const deleteModal = document.getElementById('delete-confirm-modal');
    const confirmDeleteBtn = document.getElementById('confirm-delete-btn');
    const cancelDeleteBtn = document.getElementById('cancel-delete-btn');
    const studentNamePlaceholder = document.getElementById('delete-student-name-placeholder');
    let activeDeleteFormId = null;

    const deleteTriggers = document.querySelectorAll('.delete-student-trigger');
    deleteTriggers.forEach(trigger => {
        trigger.addEventListener('click', (e) => {
            e.preventDefault();
            const studentId = trigger.getAttribute('data-id');
            const studentName = trigger.getAttribute('data-name');
            activeDeleteFormId = `delete-form-${studentId}`;
            
            if (studentNamePlaceholder) {
                studentNamePlaceholder.textContent = studentName;
            }
            
            if (deleteModal) {
                deleteModal.classList.add('active');
            }
        });
    });

    if (cancelDeleteBtn && deleteModal) {
        cancelDeleteBtn.addEventListener('click', () => {
            deleteModal.classList.remove('active');
            activeDeleteFormId = null;
        });
        
        // Also close modal on overlay click
        deleteModal.addEventListener('click', (e) => {
            if (e.target === deleteModal) {
                deleteModal.classList.remove('active');
                activeDeleteFormId = null;
            }
        });
    }

    if (confirmDeleteBtn) {
        confirmDeleteBtn.addEventListener('click', () => {
            if (activeDeleteFormId) {
                const form = document.getElementById(activeDeleteFormId);
                if (form) {
                    form.submit();
                }
            }
            if (deleteModal) {
                deleteModal.classList.remove('active');
            }
        });
    }
});
