// src/JS/modules/navigation.js
/**
 * Navigation and shared utilities
 */

/**
 * Highlight current page in sidebar
 */
document.addEventListener('DOMContentLoaded', () => {
    const currentPage = window.location.pathname.split('/').pop() || 'dashboard.html';
    document.querySelectorAll('a[href]').forEach(link => {
        if (link.href.endsWith(currentPage)) {
            link.classList.remove('hover:bg-[#1e2d42]', 'text-slate-400', 'hover:text-[#f1ede6]');
            link.classList.add('bg-teal-400/10', 'border', 'border-teal-400/20', 'text-teal-400');
        }
    });
});