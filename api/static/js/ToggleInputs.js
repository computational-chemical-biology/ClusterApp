function toggleInputs(checkbox,propSample,feats) {
    const checkboxDom = document.getElementById(checkbox);
    const propSampleDom = document.getElementById(propSample);
    const featsDom = document.getElementById(feats);
    propSampleDom.value = '';

    propSampleDom.disabled = checkboxDom.checked;
    featsDom.disabled = checkboxDom.checked;
}