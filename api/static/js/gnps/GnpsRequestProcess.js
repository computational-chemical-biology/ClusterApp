import { handlePcoaResponse } from '../Graph.js';
import { showModal } from '../Graph.js';
document.addEventListener('DOMContentLoaded', function() {
    requestListener();
});


function requestListener(){
    document.getElementById('clustering-form').addEventListener('submit', function(event) {
        requestExecutor(event,this);
    });
}


function requestExecutor(event,form){
    event.preventDefault();
    document.getElementById('loadin-spn').hidden = false;
    const formData = new FormData(form);
    fetch('/graph', {
        method: 'POST',
        body: formData
    })
    .then(async response => { 
        if(response.status == 500){
            showError('Problems to get data from GNPS please try again later');
            return;
        }
        const data = await response.json()
        handlePcoaResponse(data);
        document.getElementById('loadin-spn').hidden = true;
    }).catch(error => {
        showError("An error occurred while processing the request. Please try again.");
    });
    
}

function showError(text){
    showModal(text);
    document.getElementById('loadin-spn').hidden = true;
}