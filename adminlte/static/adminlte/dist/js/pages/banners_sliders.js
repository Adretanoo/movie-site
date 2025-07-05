document.addEventListener("DOMContentLoaded", () => {
    // === Головний банер (На главной верх) ===
    const topContainer = document.getElementById("banner-container");
    const topAddBtn = document.getElementById("add-banner");
    const template = document.getElementById("banner-template");

    function createBannerFromTemplate(container, insertBeforeBtn) {
        const clone = template.content.cloneNode(true);
        const card = clone.querySelector(".banner-card");
        const fileInput = card.querySelector(".file-input");
        const previewImg = card.querySelector(".preview-img");
        const uploadBtn = card.querySelector(".upload-label");
        const removeBtn = card.querySelector(".remove-btn");

        uploadBtn.addEventListener("click", () => fileInput.click());

        fileInput.addEventListener("change", (e) => {
            const file = e.target.files[0];
            if (file) {
                const reader = new FileReader();
                reader.onload = () => previewImg.src = reader.result;
                reader.readAsDataURL(file);
            }
        });

        removeBtn.addEventListener("click", () => card.remove());

        container.insertBefore(clone, insertBeforeBtn);
    }


    topAddBtn.addEventListener("click", () => {
        createBannerFromTemplate(topContainer, topAddBtn);
    });

    // === Сквозной банер (фон) ===
    const bgFileInput = document.getElementById("bg-file-input");
    const bgPreviewImg = document.getElementById("bg-preview-img");
    const bgUploadBtn = document.getElementById("bg-upload-btn");
    const bgRemoveBtn = document.getElementById("bg-remove-btn");
    const bgPlaceholder = "https://via.placeholder.com/150x90";

    bgUploadBtn.addEventListener("click", () => bgFileInput.click());

    bgFileInput.addEventListener("change", (e) => {
        const file = e.target.files[0];
        if (file) {
            const reader = new FileReader();
            reader.onload = () => bgPreviewImg.src = reader.result;
            reader.readAsDataURL(file);
        }
    });

    bgRemoveBtn.addEventListener("click", () => {
        bgPreviewImg.src = bgPlaceholder;
        bgFileInput.value = "";
    });

    // === Новини/Акції (На главной Новости Акции) ===
    const promoContainer = document.getElementById("promo-banner-container");
    const promoAddBtn = document.getElementById("add-promo-banner");

    promoAddBtn.addEventListener("click", () => {
        createBannerFromTemplate(promoContainer, promoAddBtn);
    });

});
