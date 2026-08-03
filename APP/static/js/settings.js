function openTab(evt, tabName) {
    var i, tabcontent, tablinks;
    
    // Hide all tab content
    tabcontent = document.getElementsByClassName("tab-content");
    for (i = 0; i < tabcontent.length; i++) {
        tabcontent[i].classList.remove("active");
    }
    
    // Remove active class from all tab links
    tablinks = document.getElementsByClassName("tab-link");
    for (i = 0; i < tablinks.length; i++) {
        tablinks[i].classList.remove("active");
    }
    
    // Show current tab and add active class to button
    document.getElementById(tabName).classList.add("active");
    evt.currentTarget.classList.add("active");
}

document.addEventListener("DOMContentLoaded", function() {
    // Utility for form submission
    function handleFormSubmit(formId, endpoint) {
        const form = document.getElementById(formId);
        if (!form) return;
        
        form.addEventListener('submit', async function(e) {
            e.preventDefault();
            const formData = new FormData(form);
            const btn = form.querySelector('button[type="submit"]');
            const originalText = btn.innerText;
            
            btn.innerText = 'Processing...';
            btn.disabled = true;
            
            try {
                const response = await fetch(endpoint, {
                    method: 'POST',
                    body: formData
                });
                const result = await response.json();
                
                if (result.status === 'success') {
                    alert(result.message);
                    if (formId === 'passwordForm' || formId === 'issueForm' || formId === 'feedbackForm') {
                        form.reset();
                    }
                } else {
                    alert(result.message || 'An error occurred.');
                }
            } catch (error) {
                alert('A network error occurred. Please try again.');
                console.error(error);
            } finally {
                btn.innerText = originalText;
                btn.disabled = false;
            }
        });
    }

    handleFormSubmit('profileForm', '/settings/update_profile');
    handleFormSubmit('passwordForm', '/settings/change_password');
    handleFormSubmit('issueForm', '/settings/report_issue');
    handleFormSubmit('feedbackForm', '/settings/give_feedback');

    // Double Confirmation logic
    const modal = document.getElementById('confirmationModal');
    const modalTitle = document.getElementById('modalTitle');
    const modalMessage = document.getElementById('modalMessage');
    const confirmBtn = document.getElementById('confirmModalBtn');
    const cancelBtn = document.getElementById('cancelModalBtn');
    
    let currentAction = null;

    function openModal(title, message, action) {
        modalTitle.innerText = title;
        modalMessage.innerText = message;
        currentAction = action;
        modal.classList.add('show');
    }

    function closeModal() {
        modal.classList.remove('show');
        currentAction = null;
    }

    cancelBtn.addEventListener('click', closeModal);

    confirmBtn.addEventListener('click', async function() {
        if (!currentAction) return;
        
        const originalText = confirmBtn.innerText;
        confirmBtn.innerText = 'Processing...';
        confirmBtn.disabled = true;
        cancelBtn.disabled = true;
        
        try {
            const response = await fetch(currentAction.endpoint, { method: 'POST' });
            const result = await response.json();
            
            if (result.status === 'success') {
                alert(result.message);
                if (result.redirect) {
                    window.location.href = result.redirect;
                }
            } else {
                alert(result.message || 'An error occurred.');
            }
        } catch (error) {
            alert('A network error occurred.');
        } finally {
            confirmBtn.innerText = originalText;
            confirmBtn.disabled = false;
            cancelBtn.disabled = false;
            closeModal();
        }
    });

    const deleteDataBtn = document.getElementById('deleteDataBtn');
    if (deleteDataBtn) {
        deleteDataBtn.addEventListener('click', function() {
            openModal(
                'Delete Data', 
                'Are you absolutely sure you want to delete your data? This will keep your account but remove predictions, roadmaps, etc. This action requires confirmation.', 
                { endpoint: '/settings/delete_data' }
            );
        });
    }

    const deleteAccountBtn = document.getElementById('deleteAccountBtn');
    if (deleteAccountBtn) {
        deleteAccountBtn.addEventListener('click', function() {
            openModal(
                'Delete Account', 
                'WARNING: You are about to permanently delete your account and all associated data. This action CANNOT be undone.', 
                { endpoint: '/settings/delete_account' }
            );
        });
    }
});
