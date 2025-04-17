window.addEventListener("DOMContentLoaded", function () {
    const header = document.querySelector(".fixed-header");
    document.body.style.paddingTop = `${header.offsetHeight}px`;
});

window.addEventListener("resize", function () {
    const header = document.querySelector(".fixed-header");
    document.body.style.paddingTop = `${header.offsetHeight}px`;
});
document.addEventListener("DOMContentLoaded", function () {
    const header = document.querySelector("header");
    const main = document.querySelector("main");
    main.style.paddingTop = `${header.offsetHeight}px`;
});