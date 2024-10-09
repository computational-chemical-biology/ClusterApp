function toggleInputs(checkbox,blankInputs) {
    const checkboxDom = document.getElementById(checkbox);    
    const blankInputsDom = document.getElementById(blankInputs);
    blankInputsDom.style.display = checkboxDom.checked == false ? 'none' : 'flex';
}