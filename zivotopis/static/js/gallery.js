document.addEventListener('DOMContentLoaded', function () {
    let slideIndex = 0;
    showSlides(slideIndex);

    function showSlides(index) {
        let slides = document.querySelectorAll('.slides img');

        // Ak index presiahne počet obrázkov, resetuj
        if (index >= slides.length) {
            slideIndex = 0;
        }
        if (index < 0) {
            slideIndex = slides.length - 1;
        }

        // Skry všetky obrázky
        slides.forEach((slide) => {
            slide.style.display = 'none';
            slide.classList.remove('active');
        });

        // Zobraz aktívny obrázok
        let activeSlide = slides[slideIndex];
        activeSlide.style.display = 'block';
        activeSlide.classList.add('active');

        // Dynamicky uprav veľkosť obrázka podľa pomeru strán
        let maxHeight = 500;  // Nastav maximálnu výšku v px
        let aspectRatio = activeSlide.naturalWidth / activeSlide.naturalHeight;

        if (aspectRatio < 1) {
            // Obrázok je na výšku – obmedz výšku a prispôsob šírku
            activeSlide.style.height = `${maxHeight}px`;
            activeSlide.style.width = 'auto';
        } else {
            // Obrázok je na šírku – obmedz šírku a prispôsob výšku
            activeSlide.style.width = '80%';
            activeSlide.style.height = 'auto';
        }
    }

    document.querySelector('.prev').addEventListener('click', () => {
        showSlides(--slideIndex);
    });

    document.querySelector('.next').addEventListener('click', () => {
        showSlides(++slideIndex);
    });
});