// Sidebar Toggles
function toggleSidebar() {
    const sidebar = document.getElementById('sidebar');
    const mainContent = document.getElementById('mainContent');
    const overlay = document.getElementById('sidebarOverlay');
    
    if (window.innerWidth >= 768) {
        sidebar.classList.toggle('desktop-closed');
        mainContent.classList.toggle('desktop-closed');
    } else {
        sidebar.classList.toggle('mobile-open');
        if (overlay.classList.contains('hidden')) {
            overlay.classList.remove('hidden');
            setTimeout(() => overlay.classList.remove('opacity-0'), 10);
        } else {
            overlay.classList.add('opacity-0');
            setTimeout(() => overlay.classList.add('hidden'), 300);
        }
    }
}

// THE FIX: Explicitly target the exact modal by its ID
function toggleModal(modalId) { 
    const modal = document.getElementById(modalId);
    if (modal) modal.classList.toggle('hidden'); 
}

function logout() { 
    localStorage.clear(); 
    location.href = '/'; 
}

// Staggered Animations
function applyStaggeredAnimations(selector) {
    const elements = document.querySelectorAll(selector);
    elements.forEach((el, index) => {
        el.style.animationDelay = `${index * 0.05}s`; 
        el.classList.add('animate-stagger');
    });
}

// Client-Side Table Filtering
function filterTable(tableId, searchInputId) {
    const input = document.getElementById(searchInputId).value.toLowerCase();
    const rows = document.querySelectorAll(`#${tableId} tr`);
    
    rows.forEach(row => {
        const text = row.innerText.toLowerCase();
        row.style.display = text.includes(input) ? '' : 'none';
    });
}

// Toast Notifications
function showToast(message) {
    const toast = document.createElement('div');
    toast.className = 'fixed bottom-5 right-5 bg-gray-900 text-white px-6 py-3 rounded-xl shadow-2xl z-50 text-sm font-medium animate-stagger flex items-center gap-2';
    toast.innerHTML = `<i class="ph-fill ph-check-circle text-green-400 text-lg"></i> ${message}`;
    document.body.appendChild(toast);
    setTimeout(() => { 
        toast.style.opacity = '0';
        toast.style.transform = 'translateY(10px)';
        toast.style.transition = 'all 0.3s ease';
        setTimeout(() => toast.remove(), 300);
    }, 3000);
}

document.addEventListener('DOMContentLoaded', () => {
    const bName = document.getElementById('bName');
    const dateDisplay = document.getElementById('dateDisplay');
    
    if (bName) bName.innerText = localStorage.getItem('branchName') || 'Academy';
    if (dateDisplay) dateDisplay.innerText = new Date().toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' });
});

document.addEventListener('DOMContentLoaded', () => {
    const bName = document.getElementById('bName');
    const dateDisplay = document.getElementById('dateDisplay');
    
    if (bName) bName.innerText = localStorage.getItem('branchName') || 'Academy';
    if (dateDisplay) dateDisplay.innerText = new Date().toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' });

    // --- NEW: DYNAMICALLY HIDE ADMIN MENU ---
    const role = localStorage.getItem('role');
    const adminMenu = document.getElementById('adminMenu');
    
    // If they are not an Admin Master, hide the Administration sidebar section completely
    if (role !== 'Admin Master' && adminMenu) {
        adminMenu.style.display = 'none';
    }
});
