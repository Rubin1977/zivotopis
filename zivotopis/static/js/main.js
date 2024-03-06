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

// úvodný kód pre galériu
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