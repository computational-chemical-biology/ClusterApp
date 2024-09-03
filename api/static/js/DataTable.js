function invalidInput(input) {
    input.style.border = "1px solid red";

    const optionElement = input.querySelector("option[value='']");
    if (optionElement) {
        optionElement.textContent = 'Please select a value';
    }
}

function removeInvalidBorder(input) {
    input.style.border = "";
}