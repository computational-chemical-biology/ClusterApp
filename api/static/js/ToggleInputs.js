function toggleInputs(checkbox,propSample) {
    const checkboxDom = document.getElementById(checkbox);
    const propSampleDom = document.getElementById(propSample);
    
    propSampleDom.value = '';

    propSampleDom.disabled = checkboxDom.checked;
}