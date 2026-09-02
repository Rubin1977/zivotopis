document.addEventListener("DOMContentLoaded", function () {
    const galleryModal = document.getElementById("gallery-modal");
    const galleryImage = document.getElementById("gallery-image");
    const galleryClose = document.getElementById("gallery-close");
    const galleryPrev = document.getElementById("gallery-prev");
    const galleryNext = document.getElementById("gallery-next");
    const modalTitle = document.getElementById("modal-title");
    const modalDescription = document.getElementById("modal-description");
    const galleryItems = document.querySelectorAll(".gallery-item");
    let currentSlideIndex = 0;
 
    function openGalleryModal(index) {
        if (galleryItems.length === 0) return;
        if (index < 0) index = galleryItems.length - 1;
        if (index >= galleryItems.length) index = 0;
 
        const item = galleryItems[index];
        const img = item.querySelector("img");
        const title = item.querySelector(".gallery-item-caption")?.textContent || "";
        const description = item.dataset.description || "";
 
        if (img) {
            galleryImage.src = img.src;
            modalTitle.textContent = title;
            modalDescription.textContent = description;
            galleryModal.removeAttribute("hidden");
            galleryModal.classList.add("open");
            currentSlideIndex = index;
            galleryModal.scrollTop = 0;
 
            galleryImage.onload = () => {
                const availableHeight = window.innerHeight * 0.8;
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
    }
 
    galleryItems.forEach((item, index) => {
        item.style.cursor = "pointer";
        item.addEventListener("click", () => openGalleryModal(index));
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
});