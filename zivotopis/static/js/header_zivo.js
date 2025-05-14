window.addEventListener("DOMContentLoaded", function () {
    const header = document.querySelector(".fixed-header");
    const main = document.querySelector("main");

    if (header) {
        document.body.style.paddingTop = `${header.offsetHeight}px`;
    }

    if (header && main) {
        main.style.paddingTop = `${header.offsetHeight}px`;
    }
});

window.addEventListener("resize", function () {
    const header = document.querySelector(".fixed-header");

    if (header) {
        document.body.style.paddingTop = `${header.offsetHeight}px`;
    }
});

window.addEventListener("scroll", function () {
    let header = document.querySelector(".fixed-header");
    if (window.scrollY > 50) {
        header.classList.add("scroll"); // Pridá triedu pri posunutí
    } else {
        header.classList.remove("scroll"); // Odstráni triedu, keď si hore
    }
});