document.addEventListener("DOMContentLoaded", () => {
    const container = document.getElementById("banner-container");
    const addBtn = document.getElementById("add-banner");
    const defaultImgPath = container.dataset.default;

    function createGalleryItem() {
        const wrapper = document.createElement("div");
        wrapper.className = "gallery-item";

        const removeBtn = document.createElement("span");
        removeBtn.className = "remove";
        removeBtn.textContent = "×";

        const img = document.createElement("img");
        img.src = defaultImgPath;
        img.dataset.default = defaultImgPath;

        const fileInput = document.createElement("input");
        fileInput.type = "file";
        fileInput.name = "gallery_images";  // ВАЖЛИВО: однакова назва
        fileInput.accept = "image/*";
        fileInput.style.display = "none";

        const uploadBtnText = container.dataset.uploadBtn;
        const uploadBtn = document.createElement("button");
        uploadBtn.textContent = uploadBtnText;

        uploadBtn.addEventListener("click", (e) => {
            e.preventDefault();
            fileInput.click();
        });

        fileInput.addEventListener("change", () => {
            const file = fileInput.files[0];
            if (file) {
                const reader = new FileReader();
                reader.onload = e => {
                    img.src = e.target.result;
                };
                reader.readAsDataURL(file);
            }
        });

        removeBtn.addEventListener("click", () => {
            wrapper.remove();
        });

        wrapper.appendChild(removeBtn);
        wrapper.appendChild(img);
        wrapper.appendChild(fileInput);
        wrapper.appendChild(uploadBtn);
        return wrapper;
    }


    addBtn.addEventListener("click", () => {
        const item = createGalleryItem();
        container.insertBefore(item, addBtn);
    });

});


const uploadBtn = document.getElementById('uploadBtn');
const deleteBtn = document.getElementById('deleteBtn');
const fileInput = document.getElementById('mainUpload');
const preview = document.getElementById('mainPreview');

uploadBtn?.addEventListener('click', (e) => {
    e.preventDefault();
    fileInput.click();
});

fileInput?.addEventListener('change', () => {
    const file = fileInput.files[0];
    if (file) {
        const reader = new FileReader();
        reader.onload = function (e) {
            preview.src = e.target.result;
        };
        reader.readAsDataURL(file);
    }
});

deleteBtn?.addEventListener('click', (e) => {
    e.preventDefault();
    preview.src = preview.dataset.default;
    fileInput.value = '';
});
