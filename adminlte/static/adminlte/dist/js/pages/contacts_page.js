function triggerInput(index) {
    // Знайти input файлу і викликати click
    const input = document.querySelectorAll('input[type="file"]')[index - 1];
    input.click();
}

function updateImagePreview(input) {
    const index = Array.from(document.querySelectorAll('input[type="file"]')).indexOf(input) + 1;
    const preview = document.getElementById(`logoPreview${index}`);
    const file = input.files[0];

    if (file) {
        const reader = new FileReader();
        reader.onload = function (e) {
            preview.src = e.target.result;
        }
        reader.readAsDataURL(file);
    }
}

function resetImage(index) {
    const input = document.querySelectorAll('input[type="file"]')[index - 1];
    const preview = document.getElementById(`logoPreview${index}`);
    const defaultSrc = preview.dataset.default;

    input.value = ''; // Очистити інпут
    preview.src = defaultSrc; // Повернути дефолт
}