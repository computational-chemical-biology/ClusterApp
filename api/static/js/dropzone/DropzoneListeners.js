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

        this.dropzone.on("success", function(file, response) {
            console.log("File uploaded successfully:", file.name);
            console.log("Server response:", response);
            
          });
        this.dropzone.on("error", function(file, errorMessage, xhr) {
            console.error("Error uploading file:", file.name);
            console.error("Error message:", errorMessage);
            console.error("XHR object:", xhr);
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
      console.log(file);
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

}

