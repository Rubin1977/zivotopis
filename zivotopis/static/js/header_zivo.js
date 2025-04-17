window.addEventListener("DOMContentLoaded", function () {
    const header = document.querySelector(".fixed-header");
    document.body.style.paddingTop = `${header.offsetHeight}px`;
});

window.addEventListener("resize", function () {
    const header = document.querySelector(".fixed-header");
    document.body.style.paddingTop = `${header.offsetHeight}px`;
});