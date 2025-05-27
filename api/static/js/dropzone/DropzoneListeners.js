import { handlePcoaResponse, showModal } from "../Graph.js";
import { submitDropzone } from "./DropzoneValidator.js";
export class DropzoneListeners {

    constructor(dropzone,redirectUrl,event){
        this.dropzone = dropzone;
        this.redirectUrl = redirectUrl;
        this.event = event;
    }
    setupListeners(){
        this.dropzone.on("addedfile", (file)=> {
          this._onAddedFile(file);
        });

        this.dropzone.on("success", (file, response)=> {
          handlePcoaResponse(response);
          this.dropzone.removeFile(file);
        });

        this.dropzone.on("error", (file, errorMessage, xhr) => {
          console.log(errorMessage)
          if(errorMessage === 'You can not upload any more files.'){
            this._onError(errorMessage)
            return;
          }
          this._onErrorRemoveFile(file);
        });

    }

    _onAddedFile(file){
      const editCsvButton = document.getElementById("editCsvButton");
      const submit = document.getElementById("submit");
      editCsvButton.hidden = false;
      submit.hidden = false;
      submit.onclick = ()=> {
        submitDropzone(this.event,this.dropzone);
      }
      editCsvButton.onclick = ()=> {
      this._redirect(file);
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

    _onErrorRemoveFile(file){
      this.dropzone.removeFile(file);
      document.getElementById("submit").hidden = false;
      showModal('An error occurred while processing the request. Please try again.');
    }

    _onError(message){
      document.getElementById("submit").hidden = false;
      showModal(message);
    }
    

}

