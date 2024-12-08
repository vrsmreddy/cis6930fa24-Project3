// src/static/script.js

document.addEventListener('DOMContentLoaded', () => {
    const pdfOption = document.getElementById('pdf-option');
    const urlOption = document.getElementById('url-option');
    const pdfFileInput = document.getElementById('pdf_file_input');
    const pdfUrlInput = document.getElementById('pdf_url_input');

    function toggleInputFields() {
        if (pdfOption && urlOption && pdfFileInput && pdfUrlInput) {
            if (pdfOption.checked) {
                pdfFileInput.style.display = 'block';
                pdfUrlInput.style.display = 'none';
            } else {
                pdfFileInput.style.display = 'none';
                pdfUrlInput.style.display = 'block';
            }
        }
    }

    // Initial state
    toggleInputFields();

    if (pdfOption && urlOption) {
        pdfOption.addEventListener('change', toggleInputFields);
        urlOption.addEventListener('change', toggleInputFields);
    }
});
