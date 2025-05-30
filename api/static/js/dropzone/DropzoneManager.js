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
        this.dropzone.addFile(file);
    }

    countQueuedFiles() {
    return this.dropzone.files.filter(file => {
        return file.status === Dropzone.ADDED || file.status === Dropzone.QUEUED;
    }).length;
}
}

export const dropzoneManager = new DropzoneManager();