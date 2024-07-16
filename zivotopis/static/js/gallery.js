document.addEventListener('DOMContentLoaded', function () {
    let slideIndex = 0;
    showSlides(slideIndex);

    function showSlides(index) {
        let slides = document.querySelectorAll('.slides img');
        if (index >= slides.length) {
            slideIndex = 0;
        }
        if (index < 0) {
            slideIndex = slides.length - 1;
        }
        slides.forEach((slide, i) => {
            slide.style.display = 'none';
            slide.classList.remove('active');
        });
        slides[slideIndex].style.display = 'block';
        slides[slideIndex].classList.add('active');
        }

    document.querySelector('.prev').addEventListener('click', () => {
        showSlides(--slideIndex);
    });

    document.querySelector('.next').addEventListener('click', () => {
        showSlides(++slideIndex);
    });
});