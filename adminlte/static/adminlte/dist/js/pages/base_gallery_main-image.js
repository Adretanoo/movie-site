function buttonImagePreviewClick() {
    document.getElementById('formPreview')?.click();
}

function updateImagePreview(input) {
    const mainPreview = document.getElementById('mainPreview');
    if (input?.files && input.files[0]) {
        mainPreview.src = URL.createObjectURL(input.files[0]);
    }
}

function buttonResetPreviewClick() {
    const input = document.getElementById('formPreview');
    const preview = document.getElementById('mainPreview');
    input.value = '';
    preview.src = preview.dataset.default;
}

// === Галерея ===
document.addEventListener("DOMContentLoaded", () => {
    const galleryContainer = document.getElementById("gallery-formset-container");
    const addPhotoBtn = document.getElementById("add-movie-gallery-item");
    const emptyFormTemplate = document.getElementById("empty-gallery-form-template");
    const totalFormsInput = document.getElementById("id_basegallery_set-TOTAL_FORMS");

    if (!galleryContainer || !addPhotoBtn || !emptyFormTemplate || !totalFormsInput) return;

    function updateGalleryPreview(fileInput) {
        const itemDiv = fileInput.closest(".gallery-item");
        const img = itemDiv?.querySelector(".gallery-image-preview");
        if (fileInput.files?.[0]) {
            img.src = URL.createObjectURL(fileInput.files[0]);
        }
    }

    function toggleFormVisibility(checkbox) {
        const itemDiv = checkbox.closest(".gallery-item");
        if (checkbox.checked) {
            itemDiv.style.display = "none";
            const fileInput = itemDiv.querySelector('input[type="file"]');
            const img = itemDiv.querySelector(".gallery-image-preview");
            if (fileInput) fileInput.value = '';
            if (img) img.src = img.dataset.default || '';
        } else {
            itemDiv.style.display = "";
        }
    }

    function initializeGalleryItem(itemDiv) {
        const fileInput = itemDiv.querySelector(".gallery-file-input");
        const uploadBtn = itemDiv.querySelector(".upload-gallery-btn");
        const removeBtn = itemDiv.querySelector(".gallery-delete-btn");
        const deleteCheckbox = itemDiv.querySelector('input[type="checkbox"][name$="-DELETE"]');


        if (uploadBtn && fileInput) {
            uploadBtn.addEventListener("click", (e) => {
                e.preventDefault();
                fileInput.click();
            });
            fileInput.addEventListener("change", () => updateGalleryPreview(fileInput));
        }

        if (removeBtn) {
            removeBtn.addEventListener("click", () => {
                const img = itemDiv.querySelector(".gallery-image-preview");
                fileInput.value = '';
                if (img) img.src = img.dataset.default || '';
                itemDiv.style.display = "none";
            });
        }

        if (uploadBtn && fileInput) {
            uploadBtn.addEventListener("click", (e) => {
                e.preventDefault();
                fileInput.click();
            });
            fileInput.addEventListener("change", () => updateGalleryPreview(fileInput));
        }

        if (removeBtn && deleteCheckbox) {
            removeBtn.addEventListener("click", (e) => {
                e.preventDefault();
                deleteCheckbox.checked = true;
                toggleFormVisibility(deleteCheckbox);
            });
        }

        if (deleteCheckbox) {
            deleteCheckbox.addEventListener("change", () => {
                toggleFormVisibility(deleteCheckbox);
            });
        }
    }

    addPhotoBtn.addEventListener("click", () => {
        const index = parseInt(totalFormsInput.value);
        const newItem = emptyFormTemplate.cloneNode(true);
        newItem.removeAttribute("id");
        newItem.style.display = "block";

        newItem.innerHTML = newItem.innerHTML.replace(/__prefix__/g, index);
        newItem.querySelectorAll('[id]').forEach(el => el.id = el.id.replace(/__prefix__/g, index));
        newItem.querySelectorAll('[name]').forEach(el => el.name = el.name.replace(/__prefix__/g, index));
        newItem.querySelectorAll('[for]').forEach(el => el.setAttribute('for', el.getAttribute('for').replace(/__prefix__/g, index)));

        galleryContainer.insertBefore(newItem, addPhotoBtn);
        initializeGalleryItem(newItem);
        totalFormsInput.value = index + 1;
    });

    galleryContainer.querySelectorAll(".gallery-item").forEach(item => {
        if (item.id !== "empty-gallery-form-template") {
            initializeGalleryItem(item);
        }
    });
});









