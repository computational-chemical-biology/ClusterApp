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

export function showModal() {
    const modalElement = document.getElementById('alert-modal');
    const modal = new bootstrap.Modal(modalElement);
    modal.show();
}