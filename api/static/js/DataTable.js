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

function showPcoaModal(data) {
    document.getElementById('pcoa-div').innerHTML = '<h3>PCoA Analysis</h3><iframe id="pcoa-plot" type="text/html" style="width:100%;height:500px;"></iframe>';
    const pcoaModalPlot = document.getElementById("pcoa-plot");
    pcoaModalPlot.src = "static/"+data; 

    showModal("pcoa-modal");
}

function showErrorModal() {
    document.getElementById('pcoa-div').innerHTML = '<h3>Error</h3><p>There was an error processing the data. Please verify your data and try again.</p>';
    showModal("pcoa-modal");
}

function showModal(modalId) {
    const modalElement = document.getElementById(modalId);
    const modal = new bootstrap.Modal(modalElement);
    modal.show();
}

function hideModal(modalId) {
    const modalElement = document.getElementById(modalId);
    const modal = bootstrap.Modal.getInstance(modalElement);
    modal.hide();
}

function showLoading() {
    const loading = document.getElementById('loading-spn');
    loading.removeAttribute('hidden',false);
}

function hideLoading() {
    const loading = document.getElementById('loading-spn');
    loading.setAttribute('hidden', true);
}