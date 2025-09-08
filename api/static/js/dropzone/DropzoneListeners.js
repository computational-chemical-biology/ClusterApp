import { handlePcoaResponse, showModal, handleRepportResponse } from "../Graph.js";
import { submitDropzone, generateRepport } from "./DropzoneValidator.js";
export class DropzoneListeners {

  constructor(dropzone, redirectUrl, event) {
    this.dropzone = dropzone;
    this.redirectUrl = redirectUrl;
    this.event = event;
  }
  setupListeners() {
    this.dropzone.on("addedfile", (file) => {
      this._onAddedFile(file);
    });

    this.dropzone.on("success", (file, response) => {
      let data = null;

      if (typeof response === 'string') {
        const txt = response.trim();
        if (txt.startsWith('{') || txt.startsWith('[')) {
          try {
            data = JSON.parse(txt);
          } catch (err) {
            console.warn('Response is not valid JSON:', err);
            data = null;
          }
        }
      } else if (response && typeof response === 'object') {
        data = response;
      }

      if (data && data.pdf_path) {
        handleRepportResponse(data);
        document.getElementById('loadin-spn').hidden = true;
        this.dropzone.removeFile(file);
        return;
      }

      try {
        handlePcoaResponse(response);
      } catch (err) {
        console.error('handlePcoaResponse failed:', err);
        showModal('Resposta do servidor inválida. Veja console para detalhes.');
      } finally {
        this.dropzone.removeFile(file);
      }
    });

    this.dropzone.on("error", (file, errorMessage, xhr) => {
      if (errorMessage === 'You can not upload any more files.') {
        this._onError(errorMessage)
        return;
      }

      const splitted = errorMessage.details.split(" ")

      if (splitted[3] === 'index"') {
        let sharedGenerateReport = document.getElementById('shared-generate_repport_ch_dz');
        sharedGenerateReport.value = false;
        this._onErrorRemoveFile(file, "The Given Attribute Does Not exist in The Given File");
        return;
      }
      let sharedGenerateReport = document.getElementById('shared-generate_repport_ch_dz');
      sharedGenerateReport.value = false;
      this._onErrorRemoveFile(file);
    });

  }

  _onAddedFile(file) {
    const editCsvButton = document.getElementById("editCsvButton");
    const submit = document.getElementById("submit");
    const generateCsvButton = document.getElementById("generateCsvButton");
    generateCsvButton.hidden = false;
    editCsvButton.hidden = false;
    submit.hidden = false;
    submit.onclick = () => {
      submitDropzone(this.event, this.dropzone);
    }
    editCsvButton.onclick = () => {
      this._redirect(file);
    }
    generateCsvButton.onclick = () => {
      let sharedGenerateReport = document.getElementById('shared-generate_repport_ch_dz');
      sharedGenerateReport.value = true;
      generateRepport(this.dropzone,this.event);
    }
  }

  _redirect(file) {
    document.getElementById("submit").hidden = true;
    document.getElementById("editCsvButton").hidden = true;
    let formData = new FormData();

    formData.append('file', file);
    fetch(this.redirectUrl, {
      method: 'POST',
      body: formData
    })
      .then(response => {
        return response.url;
      })
      .then(redirectUrl => {
        window.location.href = redirectUrl;
      });
  }

  _onErrorRemoveFile(file, errorMessage = 'An error occurred while processing the request. Please try again.') {
    this.dropzone.removeFile(file);
    document.getElementById("submit").hidden = true;
    const editCsvButton = document.getElementById("editCsvButton");
    const submit = document.getElementById("submit");
    const generateCsvButton = document.getElementById("generateCsvButton");
    generateCsvButton.hidden = true;
    editCsvButton.hidden = true;
    submit.hidden = true;
    showModal(errorMessage);
  }

  _onError(message) {
    document.getElementById("submit").hidden = false;
    showModal(message);
  }


}

