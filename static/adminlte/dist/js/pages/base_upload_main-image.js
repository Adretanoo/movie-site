console.log('✅ main_image.js loaded');

function buttonImagePreviewClick() {
    const input = document.getElementById('id_main-main_image');
    if (input) {
        input.click();
    } else {
        console.warn('❌ Не знайдено інпут id_main-main_image');
    }
}

function updateImagePreview(input) {
    const mainPreview = document.getElementById('mainPreview');
    if (!mainPreview) {
        console.warn('❌ Не знайдено #mainPreview');
        return;
    }

    if (input.files && input.files[0]) {
        mainPreview.src = URL.createObjectURL(input.files[0]);
    } else {
        mainPreview.src = mainPreview.dataset.default;
    }
}

function buttonResetPreviewClick() {
    const input = document.getElementById('id_main-main_image');
    const preview = document.getElementById('mainPreview');

    if (!input || !preview) {
        console.warn('❌ input або preview не знайдені');
        return;
    }

    input.value = '';
    preview.src = preview.dataset.default;
}

document.addEventListener("DOMContentLoaded", () => {
    const input = document.getElementById('id_main-main_image');
    if (input) {
        input.addEventListener('change', () => updateImagePreview(input));
        console.log('✅ Привʼязано change до #id_main-main_image');
    } else {
        console.warn('❌ input #id_main-main_image не знайдено в DOM');
    }
});
