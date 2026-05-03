// Sidebar & Modal Toggles
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

function toggleModal() { 
    const modal = document.getElementById('modal') || document.getElementById('leadModal');
    if (modal) modal.classList.toggle('hidden'); 
}

function logout() { 
    localStorage.clear(); 
    location.href = '/'; 
}

// Global UI Initialization
document.addEventListener('DOMContentLoaded', () => {
    const bName = document.getElementById('bName');
    const dateDisplay = document.getElementById('dateDisplay');
    
    if (bName) bName.innerText = localStorage.getItem('branchName') || 'Academy';
    if (dateDisplay) dateDisplay.innerText = new Date().toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' });
});

// Add this helper function at the top of script.js
function applyStaggeredAnimations(selector) {
    const elements = document.querySelectorAll(selector);
    elements.forEach((el, index) => {
        // Add a 50ms delay between each row/card animating in
        el.style.animationDelay = `${index * 0.05}s`; 
        el.classList.add('animate-stagger');
    });
}