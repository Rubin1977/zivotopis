document.addEventListener("DOMContentLoaded", function () {
    // Tlačidlo a text
    const myButton = document.getElementById("myButton");
    const myText = document.getElementById("myText");

    if (myButton && myText) {
        myButton.addEventListener("click", function () {
            myText.innerHTML = "Pozadie tlačidla sa zmenilo :-)";
            myButton.style.backgroundColor = getRandomColor();
        });

        function getRandomColor() {
            const letters = "0123456789ABCDEF";
            let color = "#";
            for (let i = 0; i < 6; i++) {
                color += letters[Math.floor(Math.random() * 16)];
            }
            return color;
        }
    }

    // Modálne okno
    const modal = document.getElementById("zoomed-in-modal");
    const zoomedImage = document.getElementById("zoomed-in-image");
    const closeBtn = document.getElementById("close");

    if (modal && zoomedImage) {
        document.querySelectorAll('.post-image').forEach(function (image) {
            image.addEventListener('click', function () {
                zoomedImage.src = this.src;
                modal.style.display = "block";
            });
        });

        if (closeBtn) {
            closeBtn.addEventListener('click', function () {
                modal.style.display = "none";
                zoomedImage.src = "";
            });
        }

        window.addEventListener('click', function (event) {
            if (event.target === modal) {
                modal.style.display = "none";
                zoomedImage.src = "";
            }
        });

        window.addEventListener('keydown', function (event) {
            if (event.key === "Escape") {
                modal.style.display = "none";
                zoomedImage.src = "";
            }
        });
    }

    // Galéria
    let slideIndex = 0;
    const showSlides = () => {
        const slides = document.querySelectorAll('.slides img');
        if (slides.length === 0) return;
        if (slideIndex >= slides.length) slideIndex = 0;
        if (slideIndex < 0) slideIndex = slides.length - 1;
        slides.forEach(slide => slide.style.display = 'none');
        slides[slideIndex].style.display = 'block';
    };

    const plusSlides = (n) => {
        slideIndex += n;
        showSlides();
    };

    const prevBtn = document.querySelector('.prev');
    const nextBtn = document.querySelector('.next');

    if (prevBtn) prevBtn.addEventListener('click', () => plusSlides(-1));
    if (nextBtn) nextBtn.addEventListener('click', () => plusSlides(1));

    showSlides();
});