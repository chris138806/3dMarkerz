document.addEventListener("DOMContentLoaded", function () {
    const resinaRadio = document.getElementById("resina");
    const filoRadio = document.getElementById("filo");
    const resinaOptions = document.getElementById("resina-options");
    const filoOptions = document.getElementById("filo-options");
    const fileInput = document.getElementById("file");
    const uploadText = document.getElementById("upload-text");
    const fileNameDisplay = document.getElementById("file-name");

    resinaRadio.addEventListener("change", function () {
        resinaOptions.classList.remove("hidden");
        filoOptions.classList.add("hidden");
    });

    filoRadio.addEventListener("change", function () {
        filoOptions.classList.remove("hidden");
        resinaOptions.classList.add("hidden");
    });

    fileInput.addEventListener("change", function () {
        if (fileInput.files.length > 0) {
            uploadText.classList.add("hidden");
            fileNameDisplay.textContent = `File caricato: ${fileInput.files[0].name}`;
            fileNameDisplay.classList.remove("hidden");
        }
    });

    document.getElementById("uploadForm").addEventListener("submit", function () {
        console.log("Form inviato, redirigere alla pagina summary...");
    });
});
