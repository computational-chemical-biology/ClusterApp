import { handlePcoaResponse } from '../Graph.js';
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
    .then(response => response.json())
    .then(data => {
        handlePcoaResponse(data);
        document.getElementById('loadin-spn').hidden = true;
    }).catch(error => {
        document.getElementById('loadin-spn').hidden = true;
    });
}