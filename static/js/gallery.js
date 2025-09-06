document.addEventListener("DOMContentLoaded", function () {
    const galleryModal = document.getElementById("gallery-modal");
    const galleryImage = document.getElementById("gallery-image");
    const galleryClose = document.getElementById("gallery-close");
    const galleryPrev = document.getElementById("gallery-prev");
    const galleryNext = document.getElementById("gallery-next");
    const modalTitle = document.getElementById("modal-title");
    const modalDescription = document.getElementById("modal-description");
    const slideItems = document.querySelectorAll(".slide-item");

    let currentSlideIndex = 0;

    function showGallerySlide(index) {
        if (slideItems.length === 0) return;
        if (index < 0) index = slideItems.length - 1;
        if (index >= slideItems.length) index = 0;

        slideItems.forEach((slide, i) => {
            if (i === index) {
                slide.classList.add("active");
                slide.style.display = "block";
            } else {
                slide.classList.remove("active");
                slide.style.display = "none";
            }
        });

        currentSlideIndex = index;
    }

    function openGalleryModal(index) {
        const slide = slideItems[index];
        const img = slide.querySelector("img");
        const title = slide.querySelector("h3")?.textContent || "";
        const description = slide.querySelector("p")?.textContent || "";

        if (img) {
            galleryImage.src = img.src;
            modalTitle.textContent = title;
            modalDescription.textContent = description;
            galleryModal.style.display = "block";
            galleryModal.classList.add("open");
            currentSlideIndex = index;
        }
    }

    function closeGalleryModal() {
        galleryModal.style.display = "none";
        galleryModal.classList.remove("open");
        galleryImage.src = "";
        modalTitle.textContent = "";
        modalDescription.textContent = "";

        // Aktualizuj galériu
        showGallerySlide(currentSlideIndex);
    }

    slideItems.forEach((slide, index) => {
        const img = slide.querySelector("img");
        if (img) {
            img.style.cursor = "pointer";
            img.addEventListener("click", () => openGalleryModal(index));
        }
    });

    if (galleryClose) {
        galleryClose.addEventListener("click", closeGalleryModal);
    }

    if (galleryPrev) {
        galleryPrev.addEventListener("click", () => openGalleryModal(currentSlideIndex - 1));
    }

    if (galleryNext) {
        galleryNext.addEventListener("click", () => openGalleryModal(currentSlideIndex + 1));
    }

    window.addEventListener("keydown", function (event) {
        if (galleryModal.classList.contains("open")) {
            if (event.key === "Escape") {
                closeGalleryModal();
            } else if (event.key === "ArrowLeft") {
                showGallerySlide(currentSlideIndex - 1);
            } else if (event.key === "ArrowRight") {
                showGallerySlide(currentSlideIndex + 1);
            }
        }
    });

    window.addEventListener("click", function (event) {
        if (event.target === galleryModal) {
            closeGalleryModal();
        }
    });

    // Inicializuj zobrazenie prvého obrázka v galérii
    showGallerySlide(currentSlideIndex);
});