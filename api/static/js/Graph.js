document.addEventListener('DOMContentLoaded', function () {
    const modalElement = document.getElementById('alert-modal');
    removeModal(modalElement);
    startTooltip();
});

function removeModal(modalElement) {
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

export function showInputModal(text, callback) {
    const modalElement = document.getElementById('input-modal');
    const form = modalElement.querySelector('#inputModalForm');
    const input = modalElement.querySelector('#inputModalText');
    const cancelButton = document.getElementById('inputModalCancelButton');

    input.value = '';
    input.placeholder = text || '';
    input.focus();

    form.onsubmit = null;

    form.onsubmit = function (e) {
        e.preventDefault();
        const value = input.value.trim();
        if (typeof callback === 'function') {
            callback(value);
        }
        const modal = bootstrap.Modal.getInstance(modalElement) || new bootstrap.Modal(modalElement);
        modal.hide();
        return false;
    };

    cancelButton.onclick = function () {
        const modal = bootstrap.Modal.getInstance(modalElement) || new bootstrap.Modal(modalElement);
        let sharedGenerateReport = document.getElementById('shared-generate_repport_ch_dz');
        sharedGenerateReport.value = false;
        modal.hide();
    }
    

    const modal = new bootstrap.Modal(modalElement);
    modal.show();
}

export function handlePcoaResponse(response) {
    document.getElementById("submit").hidden = false;
    document.getElementById("editCsvButton").hidden = false;
    document.getElementById("generateCsvButton").hidden = false;
    document.getElementById("downloadPlot").hidden = false;

    const divPcoa = document.getElementById("pcoa-div");
    const pcoaPlot = document.getElementById("pcoa-plot");
    divPcoa.hidden = false;
    pcoaPlot.hidden = false;
    pcoaPlot.src = 'static/' + response.emperor_plot.emperorDir;
    showFilterFeedBack(response.emperor_plot.description);
}

export function handleRepportResponse(data) {
    let sharedGenerateReport = document.getElementById('shared-generate_repport_ch_dz');
    sharedGenerateReport.value = false;
    document.getElementById("submit").hidden = true;
    document.getElementById("editCsvButton").hidden = true;
    document.getElementById("generateCsvButton").hidden = true;
    document.getElementById("downloadPlot").hidden = true;
    const divPcoa = document.getElementById("pcoa-div");
    const pcoaPlot = document.getElementById("pcoa-plot");
    divPcoa.hidden = true;
    pcoaPlot.hidden = true;
    fetch('/static/downloads/' + data.uuid + '.pdf')
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.blob();
        })
        .then(blob => {
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = 'report.pdf';
            document.body.appendChild(a);
            a.click();
            a.remove();
        })
        .catch(error => {
            console.error('There was a problem with the fetch operation:', error);
        });
}

function showFilterFeedBack(description) {
    if (description !== '' && description) {
        showModal(description);
    }
}

function startTooltip() {
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        tooltipTriggerEl.setAttribute('title', `To be removed, a feature has to be less intense than the average of
blank samples in a portion of the non-blank samples. Be careful and
try different thresholds, inspecting the impact on your clustering.
You may remove true features.
`);

        const existingTooltip = bootstrap.Tooltip.getInstance(tooltipTriggerEl);
        if (existingTooltip) {
            existingTooltip.dispose();
        }
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
}


