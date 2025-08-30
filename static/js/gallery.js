document.addEventListener("DOMContentLoaded", function () {
    const slides = document.querySelectorAll(".slide-item");
    let currentIndex = 0;

    function showSlide(index) {
        slides.forEach((slide, i) => {
            slide.classList.remove("active");
            slide.style.display = "none";
            if (i === index) {
                slide.classList.add("active");
                slide.style.display = "block";
            }
        });
    }

    document.querySelector(".next").addEventListener("click", () => {
        currentIndex = (currentIndex + 1) % slides.length;
        showSlide(currentIndex);
    });

    document.querySelector(".prev").addEventListener("click", () => {
        currentIndex = (currentIndex - 1 + slides.length) % slides.length;
        showSlide(currentIndex);
    });

    showSlide(currentIndex);
});