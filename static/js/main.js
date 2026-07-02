document.addEventListener('DOMContentLoaded', function() {
    
    // --- Responsive Sidebar Toggle ---
    const sidebar = document.getElementById('sidebar');
    const sidebarToggle = document.getElementById('sidebarToggle');
    if (sidebarToggle && sidebar) {
        sidebarToggle.addEventListener('click', function() {
            sidebar.classList.toggle('active');
        });
    }

    // --- Auto Dismiss Django Messages ---
    const alerts = document.querySelectorAll('.alert-dismissible');
    alerts.forEach(function(alert) {
        setTimeout(function() {
            // Use Bootstrap native alert close or simple fade
            const bsAlert = bootstrap.Alert.getOrCreateInstance(alert);
            if (bsAlert) {
                bsAlert.close();
            } else {
                alert.style.transition = 'opacity 0.5s ease';
                alert.style.opacity = '0';
                setTimeout(() => alert.remove(), 500);
            }
        }, 4000);
    });

    // --- Delete Employee Modal Handling ---
    const deleteModal = document.getElementById('deleteConfirmModal');
    if (deleteModal) {
        deleteModal.addEventListener('show.bs.modal', function(event) {
            const button = event.relatedTarget;
            const employeeId = button.getAttribute('data-id');
            const employeeName = button.getAttribute('data-name');
            const deleteUrl = button.getAttribute('data-url');
            
            const modalNameSpan = deleteModal.querySelector('#modal-employee-name');
            const modalIdSpan = deleteModal.querySelector('#modal-employee-id');
            const deleteForm = deleteModal.querySelector('#delete-confirm-form');
            
            if (modalNameSpan) modalNameSpan.textContent = employeeName;
            if (modalIdSpan) modalIdSpan.textContent = employeeId;
            if (deleteForm) deleteForm.setAttribute('action', deleteUrl);
        });
    }

    // --- Image Upload Preview ---
    const photoInput = document.getElementById('id_profile_photo');
    const photoPreview = document.getElementById('profile-photo-preview');
    if (photoInput && photoPreview) {
        photoInput.addEventListener('change', function() {
            const file = this.files[0];
            if (file) {
                const reader = new FileReader();
                reader.onload = function(e) {
                    photoPreview.setAttribute('src', e.target.result);
                    photoPreview.classList.remove('d-none');
                    // Hide initials placeholder if visible
                    const placeholder = document.getElementById('profile-photo-placeholder');
                    if (placeholder) placeholder.classList.add('d-none');
                }
                reader.readAsDataURL(file);
            }
        });
    }

    // --- Instant AJAX Search ---
    const searchInput = document.getElementById('employeeSearchInput');
    const tableBody = document.getElementById('employeeTableBody');
    const paginationContainer = document.getElementById('paginationContainer');
    
    if (searchInput && tableBody) {
        let debounceTimer;
        
        searchInput.addEventListener('input', function() {
            clearTimeout(debounceTimer);
            const query = this.value.trim();
            const sortBy = document.getElementById('currentSortField') ? document.getElementById('currentSortField').value : '';
            
            // Show a small spinner indicator inside table if needed, or simple visual cue
            tableBody.style.opacity = '0.5';

            debounceTimer = setTimeout(function() {
                // Fetch dynamic filtered rows
                fetch(`/employees/search/?q=${encodeURIComponent(query)}&sort_by=${encodeURIComponent(sortBy)}`)
                    .then(response => {
                        if (!response.ok) throw new Error('Network response was not ok');
                        return response.text();
                    })
                    .then(html => {
                        // Replace table body
                        tableBody.innerHTML = html;
                        tableBody.style.opacity = '1';
                        
                        // Re-initialize tooltip bindings or modal triggers if necessary
                        // Re-fetch pagination snippet if search view supports pagination refresh
                        refreshPagination(query, sortBy);
                    })
                    .catch(err => {
                        console.error('Search error:', err);
                        tableBody.style.opacity = '1';
                    });
            }, 300); // 300ms debounce
        });
    }

    function refreshPagination(query, sortBy) {
        if (!paginationContainer) return;
        // Fetch standard page layout to update pagination links
        fetch(`/employees/?q=${encodeURIComponent(query)}&sort_by=${encodeURIComponent(sortBy)}`)
            .then(response => response.text())
            .then(html => {
                const parser = new DOMParser();
                const doc = parser.parseFromString(html, 'text/html');
                const newPagination = doc.getElementById('paginationContainer');
                if (newPagination && paginationContainer) {
                    paginationContainer.innerHTML = newPagination.innerHTML;
                }
            })
            .catch(err => console.error('Pagination refresh error:', err));
    }
});
