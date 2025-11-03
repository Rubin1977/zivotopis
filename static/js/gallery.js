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
        slide.classList.toggle("active", i === index);
    });

    currentSlideIndex = index;
    }

    function openGalleryModal(index) {
        if (slideItems.length === 0) return;
        if (index < 0) index = slideItems.length - 1;
        if (index >= slideItems.length) index = 0;

        const slide = slideItems[index];
        const img = slide.querySelector("img");
        const title = slide.querySelector("h3")?.textContent || "";
        const description = slide.querySelector("p")?.textContent || "";

        if (img) {
            galleryImage.src = img.src;
            modalTitle.textContent = title;
            modalDescription.textContent = description;
            galleryModal.removeAttribute("hidden");
            galleryModal.classList.add("open");
            currentSlideIndex = index;

            // Reset scroll pozície modálu
            galleryModal.scrollTop = 0;

            // Dynamické centrovanie obrázka pri načítaní
            galleryImage.onload = () => {
                const availableHeight = window.innerHeight * 0.8; // max-height obrázka
                const imageHeight = galleryImage.offsetHeight;
                const topMargin = Math.max((availableHeight - imageHeight) / 2, 10);
                galleryImage.style.marginTop = `${topMargin}px`;
                galleryImage.style.marginBottom = `${topMargin}px`;
            };
        }
    }

    function closeGalleryModal() {
        galleryModal.setAttribute("hidden", "");
        galleryModal.classList.remove("open");
        galleryImage.src = "";
        modalTitle.textContent = "";
        modalDescription.textContent = "";

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
                openGalleryModal(currentSlideIndex - 1);
            } else if (event.key === "ArrowRight") {
                openGalleryModal(currentSlideIndex + 1);
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
