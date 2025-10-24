document.addEventListener('DOMContentLoaded', function() {
    // -------------------------------
    // Tooltipy Bootstrap
    // -------------------------------
    document.querySelectorAll('[data-bs-toggle="tooltip"]').forEach(el => {
        new bootstrap.Tooltip(el);

        // Automatické skrytie tooltipu po kliknutí (napr. mobil)
        el.addEventListener('click', () => {
            const tooltip = bootstrap.Tooltip.getInstance(el);
            if (tooltip) setTimeout(() => tooltip.hide(), 3000); // 3 sekundy
        });
    });

    // Skrytie tooltipu pri scrollovaní
    window.addEventListener('scroll', () => {
        document.querySelectorAll('[data-bs-toggle="tooltip"]').forEach(el => {
            const tooltip = bootstrap.Tooltip.getInstance(el);
            if (tooltip) tooltip.hide();
        });
    });

    // -------------------------------
    // Scroll header
    // -------------------------------
    const header = document.querySelector('.site-header');
    window.addEventListener('scroll', function() {
        if (window.scrollY > 50) {
            header.classList.add('shrink');
        } else {
            header.classList.remove('shrink');
        }
    });

    // -------------------------------
    // Dynamický rok vo footeri
    // -------------------------------
    const yearEl = document.getElementById('year');
    if (yearEl) yearEl.textContent = new Date().getFullYear();
});
