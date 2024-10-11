document.addEventListener('DOMContentLoaded', function() {
    const modalElement = document.getElementById('alert-modal');
    removeModal(modalElement);
});

function removeModal(modalElement){
    modalElement.addEventListener('hidden.bs.modal', function (event) {
        document.body.classList.remove('modal-open');
        const backdrop = document.querySelector('.modal-backdrop');
        if (backdrop) {
          backdrop.parentNode.removeChild(backdrop);
        }
    });
}

export function showModal(text) {
    const modalElement = document.getElementById('alert-modal');
    const modalBodyElement = modalElement.querySelector('.modal-body');
    modalBodyElement.textContent = text;
    const modal = new bootstrap.Modal(modalElement);
    modal.show();
}

export function handlePcoaResponse(response){
    document.getElementById("submit").hidden = false;
    document.getElementById("editCsvButton").hidden = false;
    document.getElementById("downloadPlot").hidden = false;
    
    const divPcoa = document.getElementById("pcoa-div");
    const pcoaPlot = document.getElementById("pcoa-plot");
    divPcoa.hidden = false;
    pcoaPlot.hidden = false;
    pcoaPlot.src = 'static/'+response.emperor_plot.emperorDir; 
    showFilterFeedBack(response.emperor_plot.description);
}

function showFilterFeedBack(description){
    if(description !== ''){
        showModal(description);
    }
}