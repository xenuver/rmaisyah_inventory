// ── Sidebar Mobile Toggle ────────────────────────────────────────────
document.addEventListener('DOMContentLoaded', () => {
    const sidebar = document.querySelector('.sidebar');
    const toggle = document.querySelector('.sidebar-toggle');
    const overlay = document.querySelector('.sidebar-overlay');

    if (toggle && sidebar && overlay) {
        toggle.addEventListener('click', () => {
            sidebar.classList.toggle('open');
            overlay.classList.toggle('open');
        });

        overlay.addEventListener('click', () => {
            sidebar.classList.remove('open');
            overlay.classList.remove('open');
        });
    }

    // ── Auto-dismiss messages ────────────────────────────────────────
    const messages = document.querySelectorAll('.message');
    messages.forEach((msg) => {
        setTimeout(() => {
            msg.style.animation = 'slideIn 0.3s ease reverse';
            setTimeout(() => msg.remove(), 300);
        }, 4000);
    });
});
