const checkBoxes = document.querySelectorAll(".checkbox");
console.log(checkBoxes)

for (let i = 0; i < checkBoxes.length; i++) {
    if (checkBoxes[i].checked) {
        console.log("Hello")
        document.querySelector(".status_form").submit();
        break;
    }
}

