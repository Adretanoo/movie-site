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


const translationsCache = {
    uk: {},
    ru: {}
};

function cacheCurrentTranslations(currentLang) {
    if (!currentLang) return;

    translationsCache[currentLang].title = document.querySelector(`[name="title_${currentLang}"]`)?.value || '';
    translationsCache[currentLang].description = document.querySelector(`[name="description_${currentLang}"]`)?.value || '';

    translationsCache[currentLang].seo_title = document.querySelector(`[name="seo_title_${currentLang}"]`)?.value || '';
    translationsCache[currentLang].seo_keywords = document.querySelector(`[name="seo_keywords_${currentLang}"]`)?.value || '';
    translationsCache[currentLang].seo_description = document.querySelector(`[name="seo_description_${currentLang}"]`)?.value || '';
}

function restoreCachedTranslations(lang) {
    const cached = translationsCache[lang] || {};

    const title = document.querySelector(`[name="title_${lang}"]`);
    if (title) title.value = cached.title;

    const description = document.querySelector(`[name="description_${lang}"]`);
    if (description) description.value = cached.description;

    const seoTitle = document.querySelector(`[name="seo_title_${lang}"]`);
    if (seoTitle) seoTitle.value = cached.seo_title;

    const seoKeywords = document.querySelector(`[name="seo_keywords_${lang}"]`);
    if (seoKeywords) seoKeywords.value = cached.seo_keywords;

    const seoDescription = document.querySelector(`[name="seo_description_${lang}"]`);
    if (seoDescription) seoDescription.value = cached.seo_description;
}




document.addEventListener("DOMContentLoaded", function () {
    const langButtons = document.querySelectorAll(".lang-buttons a");

    langButtons.forEach(button => {
        button.addEventListener("click", function (e) {
            e.preventDefault();
            const selectedLang = this.dataset.lang;

            // Перемикаємо активну кнопку
            langButtons.forEach(btn => btn.classList.remove("active"));
            this.classList.add("active");

            // Показуємо лише потрібну мову
            document.querySelectorAll(".lang-field").forEach(el => {
                if (el.classList.contains(`lang-${selectedLang}`)) {
                    el.style.display = "";
                } else {
                    el.style.display = "none";
                }
            });
        });
    });
});
