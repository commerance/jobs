// static/js/main.js

(function() {
    'use strict';
    
    const mobileMenuToggle = document.querySelector('.mobile-menu-toggle');
    const mainNav = document.querySelector('.main-nav');
    
    if (mobileMenuToggle && mainNav) {
        mobileMenuToggle.addEventListener('click', function() {
            const isExpanded = this.getAttribute('aria-expanded') === 'true';
            
            this.setAttribute('aria-expanded', !isExpanded);
            mainNav.classList.toggle('active');
            
            const hamburgers = this.querySelectorAll('.hamburger');
            if (!isExpanded) {
                hamburgers[0].style.transform = 'rotate(45deg) translateY(8px)';
                hamburgers[1].style.opacity = '0';
                hamburgers[2].style.transform = 'rotate(-45deg) translateY(-8px)';
            } else {
                hamburgers[0].style.transform = 'none';
                hamburgers[1].style.opacity = '1';
                hamburgers[2].style.transform = 'none';
            }
        });
        
        document.addEventListener('click', function(event) {
            if (!mobileMenuToggle.contains(event.target) && !mainNav.contains(event.target)) {
                if (mainNav.classList.contains('active')) {
                    mobileMenuToggle.click();
                }
            }
        });
    }
    
    const alertCloseButtons = document.querySelectorAll('.alert-close');
    alertCloseButtons.forEach(function(button) {
        button.addEventListener('click', function() {
            const alert = this.closest('.alert');
            if (alert) {
                alert.style.transition = 'opacity 150ms ease-in-out';
                alert.style.opacity = '0';
                setTimeout(function() {
                    alert.remove();
                }, 150);
            }
        });
    });
    
    const flashContainer = document.querySelector('.flash-container');
    if (flashContainer && flashContainer.children.length > 0) {
        setTimeout(function() {
            const alerts = flashContainer.querySelectorAll('.alert');
            alerts.forEach(function(alert, index) {
                setTimeout(function() {
                    alert.style.transition = 'opacity 300ms ease-in-out, transform 300ms ease-in-out';
                    alert.style.opacity = '0';
                    alert.style.transform = 'translateX(100%)';
                    setTimeout(function() {
                        alert.remove();
                    }, 300);
                }, index100);
});
}, 5000);
}
})();
