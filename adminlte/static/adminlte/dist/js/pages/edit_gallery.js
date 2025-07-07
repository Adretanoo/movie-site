document.addEventListener("DOMContentLoaded", () => {
    const galleryContainer = document.getElementById('banner-container');
    const galleryPreview = galleryContainer.querySelector('.gallery-preview');
    const addGalleryBtn = document.getElementById('add-banner');
    const defaultImg = galleryContainer.dataset.default;
    const galleryJson = JSON.parse(document.getElementById('gallery-images').textContent);

    const deletedImageIds = [];

    const imagesToDeleteInput = document.createElement('input');
    imagesToDeleteInput.type = 'hidden';
    imagesToDeleteInput.name = 'images_to_delete';
    document.getElementById('newsForm').appendChild(imagesToDeleteInput);

    const mainPreview = document.getElementById('mainPreview');
    const mainUploadBtn = document.getElementById('uploadBtn');
    const mainDeleteBtn = document.getElementById('deleteBtn');

    const mainFileInput = document.createElement('input');
    mainFileInput.type = 'file';
    mainFileInput.name = 'main_image';
    mainFileInput.accept = 'image/*';
    mainFileInput.style.display = 'none';
    document.getElementById('newsForm').appendChild(mainFileInput);

    mainUploadBtn?.addEventListener('click', (e) => {
        e.preventDefault();
        mainFileInput.click();
    });

    mainFileInput?.addEventListener('change', () => {
        const file = mainFileInput.files[0];
        if (file) {
            const reader = new FileReader();
            reader.onload = (e) => {
                mainPreview.src = e.target.result;
            };
            reader.readAsDataURL(file);
        }
    });

    mainDeleteBtn?.addEventListener('click', (e) => {
        e.preventDefault();
        mainPreview.src = mainPreview.dataset.default;
        mainFileInput.value = '';
    });

    function createExistingItem(imgSrc, imageId) {
        const wrapper = document.createElement('div');
        wrapper.className = 'gallery-preview-item';
        wrapper.dataset.imageId = imageId;

        const img = document.createElement('img');
        img.src = imgSrc || defaultImg;

        const removeBtn = document.createElement('button');
        removeBtn.type = 'button';
        removeBtn.className = 'remove-photo';
        removeBtn.textContent = galleryContainer.dataset.removeBtn || '×';

        removeBtn.addEventListener('click', () => {
            deletedImageIds.push(imageId);
            wrapper.remove();
        });

        wrapper.appendChild(img);
        wrapper.appendChild(removeBtn);
        return wrapper;
    }

    function createNewItem() {
        const wrapper = document.createElement("div");
        wrapper.className = "gallery-item";

        const removeBtn = document.createElement("span");
        removeBtn.className = "remove";
        removeBtn.textContent = "×";

        const img = document.createElement("img");
        img.src = defaultImg;
        img.dataset.default = defaultImg;

        const fileInput = document.createElement("input");
        fileInput.type = "file";
        fileInput.name = "gallery_images";
        fileInput.accept = "image/*";
        fileInput.style.display = "none";

        const uploadBtn = document.createElement("button");
        uploadBtn.textContent = galleryContainer.dataset.uploadBtn || 'Завантажити';
        uploadBtn.type = "button";

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

    galleryJson.forEach(({id, url}) => {
        const item = createExistingItem(url, id);
        galleryPreview.appendChild(item);
    });
    galleryPreview.appendChild(addGalleryBtn);


    addGalleryBtn.addEventListener('click', () => {
        const item = createNewItem();
        galleryPreview.insertBefore(item, addGalleryBtn);
    });


    document.getElementById('newsForm').addEventListener('submit', () => {
        imagesToDeleteInput.value = deletedImageIds.join(',');
    });
});

