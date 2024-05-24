function submitDropzone(event) {
    const inputs = populeInputs();
    
    populeDragAndDropForm();
    if(verifyForm(event,inputs) == false){
        return;
    }

    document.getElementById("submit").hidden = true;
}

function populeInputs(){
    const metric = document.getElementById('metric');
    return [metric];
}

function populeDragAndDropForm(){
    let sharedMetric = document.getElementById('shared-metric');
    let sharedNormalization = document.getElementById('shared-normalization');
    let sharedScaling = document.getElementById('shared-scaling');
       
    sharedMetric.value =  document.getElementById('metric').value;
    sharedNormalization.value = document.getElementById('normalization').value;
    sharedScaling.value = document.getElementById('scaling').value;

}


function verifyForm(event, inputs) {

    for (let input of inputs) {
        if (input.value === "") {
            invalidInput(event,input);
            return false;
        }
    }

    return true;
}

function invalidInput(event, input) {
    event.preventDefault(); 
    input.style.border = "1px solid red";

    const optionElement = input.querySelector("option[value='']");
    if (optionElement) {
        optionElement.textContent = 'Please select a value';
    }
}