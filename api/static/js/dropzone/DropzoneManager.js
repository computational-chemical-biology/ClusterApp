class DropzoneManager {
    constructor() {
        this.dropzone = null;
    }

    setDropzone(dropzone) {
        this.dropzone = dropzone;
    }

    addFile(file) {
        if (!this.dropzone) {
            console.error("Dropzone não inicializado.");
            return;
        }
        this.dropzone.emit("addedfile", file);
        this.dropzone.files.push(file);
    }
}

export const dropzoneManager = new DropzoneManager();