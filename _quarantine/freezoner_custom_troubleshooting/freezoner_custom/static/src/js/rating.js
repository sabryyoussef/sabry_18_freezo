/** @odoo-module **/

// Rating System JavaScript Enhancement
document.addEventListener('DOMContentLoaded', function() {
    // Add interactive star rating functionality
    const ratingStars = document.querySelectorAll('.rating-star');
    
    ratingStars.forEach((star, index) => {
        star.addEventListener('click', function() {
            // Remove active class from all stars
            ratingStars.forEach(s => s.classList.remove('active'));
            
            // Add active class to clicked star and all previous stars
            for (let i = 0; i <= index; i++) {
                ratingStars[i].classList.add('active');
            }
            
            // Update the hidden input value
            const form = this.closest('form');
            if (form) {
                const rateInput = form.querySelector('input[name="rate"]:checked');
                if (rateInput) {
                    rateInput.value = index + 1;
                }
            }
        });
        
        star.addEventListener('mouseenter', function() {
            const currentIndex = Array.from(ratingStars).indexOf(this);
            ratingStars.forEach((s, i) => {
                if (i <= currentIndex) {
                    s.style.transform = 'scale(1.1)';
                    s.style.backgroundColor = '#ffc107';
                    s.style.color = '#000';
                }
            });
        });
        
        star.addEventListener('mouseleave', function() {
            ratingStars.forEach(s => {
                s.style.transform = 'scale(1)';
                s.style.backgroundColor = '';
                s.style.color = '';
            });
        });
    });
    
    // Add form validation
    const ratingForms = document.querySelectorAll('form[action*="/rate/"]');
    ratingForms.forEach(form => {
        form.addEventListener('submit', function(e) {
            const rateInput = form.querySelector('input[name="rate"]:checked');
            if (!rateInput) {
                e.preventDefault();
                alert('Please select a rating before submitting.');
                return false;
            }
        });
    });
    
    // Add smooth animations
    const ratingCards = document.querySelectorAll('.rating-card');
    ratingCards.forEach(card => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(30px)';
        
        setTimeout(() => {
            card.style.transition = 'all 0.6s ease-out';
            card.style.opacity = '1';
            card.style.transform = 'translateY(0)';
        }, 100);
    });
});
