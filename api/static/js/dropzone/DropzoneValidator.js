import { showModal } from "../Graph.js";

export function submitDropzone(event,dropzoneInstance) {
    const inputs = populeInputs();
    
    populeDragAndDropForm();
    if(verifyForm(event,inputs) == false){
        showModal("Please ensure that Dissimilarity measure is filled or if Filter Blanks is checked if you filled the two percentage fields and if you forget choose an normalization and scaling.");
        return;
    }
    dropzoneInstance.processQueue();
    document.getElementById("submit").hidden = true;
}

function populeInputs(){
    const metric = document.getElementById('metric_dz');
    const sharedCheckBox = document.getElementById('filter_blanks_ch_dz');
    console.log(sharedCheckBox.value);
    if(!sharedCheckBox.value){
        return [metric];
    }
    const sharedPropBlanksFeats = document.getElementById('shared-prop_blank_feats');
    const sharedPropSamples = document.getElementById('shared-prop_samples');
    const result = [metric, sharedPropBlanksFeats,sharedPropSamples];
    return result;
}

function populeDragAndDropForm(){
    let sharedMetric = document.getElementById('shared-metric');
    let sharedNormalization = document.getElementById('shared-normalization');
    let sharedScaling = document.getElementById('shared-scaling');
    let sharedPropBlanksFeats = document.getElementById('shared-prop_blank_feats');
    let sharedPropSamples = document.getElementById('shared-prop_samples');
    let sharedCheckBox = document.getElementById('shared-filter_blanks_ch_dz');

    sharedMetric.value =  document.getElementById('metric_dz').value;
    sharedNormalization.value = document.getElementById('normalization_dz').value;
    sharedScaling.value = document.getElementById('scaling_dz').value;
    sharedPropBlanksFeats.value = document.getElementById('prop_blank_feats_dz').value;
    sharedPropSamples.value = document.getElementById('prop_samples_dz').value;
    sharedCheckBox.value = document.getElementById('filter_blanks_ch_dz').checked;
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