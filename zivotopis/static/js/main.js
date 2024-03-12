document.addEventListener("DOMContentLoaded", function () {
    var myButton = document.getElementById("myButton");
    var myText = document.getElementById("myText");

    myButton.addEventListener("click", function () {
        // Zmeníme text v elemente s ID "myText" na uvítaciu správu
        myText.innerHTML = "Pozadie tlačidla sa zmenilo :-)";
        var randomColor = getRandomColor();
        // Nastavíme novú farbu pozadia tlačidla
        myButton.style.backgroundColor = randomColor;

        // Funkcia na generovanie náhodnej farby v hex formáte
        function getRandomColor() {
            var letters = "0123456789ABCDEF";
            var color = "#";
            for (var i = 0; i < 6; i++) {
                color += letters[Math.floor(Math.random() * 16)];
            }
            return color;
        }
    });
});

// Kódový blok 2: Zväčšenie obrázkov po kliknutí

// Získať všetky obrázky s triedou 'post-image'
document.addEventListener("DOMContentLoaded", function () {
    var images = document.querySelectorAll('.post-image');
    // Pridáme onClick udalosť každému obrázku
    images.forEach(function (image) {
        image.addEventListener('click', function () {
            // Ak obrázok má triedu 'zoomed-in', odstráňme ju, inak ju pridajte
            this.classList.toggle('zoomed-in');
        });
    });
});

document.addEventListener("DOMContentLoaded", function () {
    var images = document.querySelectorAll('.post-image');
    // Pridať onClick udalosť každému obrázku
    images.forEach(function (image) {
        image.addEventListener('click', function () {
            // Ak obrázok je kliknutý, získať jeho src atribút a zobraziť modálne okno s týmto obrázkom
            showModal(this.src);
        });
    });
});

//Funkcia na zobrazenie modálneho okna s obrázkom
function showModal(imageSrc) {
    //Odkaz na modálne okno
    var modal = document.getElementById("zoomed-in-modal");
    //Odkaz na obrázok v modálnom okne
    var zoomedImage = document.getElementById("zoomed-in-image");
    // Nastaviť obrázok v modálnom okne
    zoomedImage.src = imageSrc;
    // Zobraziť modálne okno
    modal.style.display = "block"
}
// Udalosť na kliknutie mimo obrázka (skryje modálne okno)
window.onclick = function (event) {
    var modal = document.getElementById("zoomed-in-modal");
        if (event.target == modal) {
            modal.style.display = "none";
    }
}

// úvodný kód pre galériu
document.addEventListener("DOMContentLoaded", function () {
let slideIndex = 0;

const showSlides = () => {
    const slides = document.querySelectorAll('.slides img');
    if (slideIndex >= slides.length) slideIndex = 0;
    if (slideIndex < 0) slideIndex = slides.length - 1;
    slides.forEach(slide => slide.style.display = 'none');
    slides[slideIndex].style.display = 'block';
}

const plusSlides = (n) => {
    slideIndex += n;
    showSlides();
}

document.querySelector('.prev').addEventListener('click', () => plusSlides(-1));
document.querySelector('.next').addEventListener('click', () => plusSlides(1));

showSlides();
});