document.addEventListener("DOMContentLoaded", () => {
    const saveBtn = document.querySelector(".save-block button");
    const errorsBox = document.getElementById("form-errors");

    saveBtn.addEventListener("click", (e) => {
        e.preventDefault();
        errorsBox.innerHTML = "";

        const mainTitle = document.getElementById("main-title")?.value.trim();
        const publishDate = document.getElementById("date")?.value.trim();
        const desc = document.getElementById("desc")?.value.trim();
        const video = document.getElementById("video-link")?.value.trim();

        const seoUrl = document.getElementById("url")?.value.trim();
        const seoTitle = document.getElementById("seo-title")?.value.trim();
        const seoKeywords = document.getElementById("keywords")?.value.trim();
        const seoDesc = document.getElementById("description")?.value.trim();

        const errors = [];

        if (!mainTitle) errors.push("Введіть назву новини");
        if (!publishDate) errors.push("Оберіть дату публікації");
        if (!desc) errors.push("Опишіть новину");
        if (!seoUrl) errors.push("URL не може бути порожнім");
        if (!seoTitle) errors.push("SEO Title обовʼязковий");
        if (!seoKeywords) errors.push("Вкажіть ключові слова");
        if (!seoDesc) errors.push("Введіть SEO опис");

        const mainImage = document.getElementById("mainPreview");
        if (mainImage && mainImage.src === mainImage.dataset.default) {
            errors.push("Головне зображення не вибране");
        }

        const galleryItems = document.querySelectorAll(".gallery-item input[type='file']");
        const hasGalleryImage = Array.from(galleryItems).some(input => input.files.length > 0);
        if (!hasGalleryImage) {
            errors.push("Додайте хоча б одне зображення до галереї");
        }

        if (errors.length > 0) {
            errorsBox.innerHTML = errors.map(err => `<div>${err}</div>`).join("");
            return;
        }

        alert("Успішно збережено!");
        setTimeout(() => {
            document.getElementById("newsForm").submit();
        }, 200);
    });
});



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
        fileInput.name = "gallery_images";
        fileInput.accept = "image/*";
        fileInput.style.display = "none";

        const uploadBtn = document.createElement("button");
        uploadBtn.textContent = "Добавить";

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

    for (let i = 0; i < 2; i++) {
        const item = createGalleryItem();
        container.insertBefore(item, addBtn);
    }
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
