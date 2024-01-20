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