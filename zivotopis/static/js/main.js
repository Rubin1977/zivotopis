document.addEventListener("DOMContentLoaded", function () {
    var myButton = document.getElementById("myButton");
    var myText = document.getElementById("myText");

    myButton.addEventListener("click", function () {
        // Zmeníme text v elemente s ID "myText" na uvítaciu správu
        myText.innerHTML = "Vitajte na mojej stránke!";
    });
});