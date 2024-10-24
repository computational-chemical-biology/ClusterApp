function toggleInputs(checkbox,blankInputs) {
    const checkboxDom = document.getElementById(checkbox);    
    const blankInputsDom = document.getElementById(blankInputs);
    blankInputsDom.style.display = checkboxDom.checked == false ? 'none' : 'flex';
}

function toggleInputsForm(checkbox, blankInputs) {
    const checkboxDom = document.getElementById(checkbox);    
    const blankInputsDom = document.getElementById(blankInputs);
    const inputs = blankInputsDom.querySelectorAll('input[type="number"]');

    if (checkboxDom.checked) {
        blankInputsDom.style.display = 'block';
        inputs.forEach(input => {
            input.setAttribute('required', 'required');
        });
        return;
    }
    
    blankInputsDom.style.display = 'none';
    inputs.forEach(input => {
        input.removeAttribute('required');
    });
}