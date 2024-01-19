
window.onload = function () {
    var myButton = document.getElementById("myButton");
    // Pridáme event listener, aby sme zachytili kliknutie na tlačidlo
    myButton.addEventListener("click", function () {
        // Zmeníme text v elemente s ID "myText" na uvítaciu správu
        document.getElementById("myText").innerHTML = "Vitajte na mojej stránke!";
    });
}
