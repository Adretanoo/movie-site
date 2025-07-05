document.addEventListener("DOMContentLoaded", function () {
    const mainUpload = document.getElementById("mainUpload");
    const mainPreview = document.getElementById("mainPreview");
    const uploadBtn = document.getElementById("uploadBtn");
    const deleteBtn = document.getElementById("deleteBtn");

    if (uploadBtn && mainUpload && mainPreview) {
        uploadBtn.addEventListener("click", function (e) {
            e.preventDefault();
            mainUpload.click();
        });

        mainUpload.addEventListener("change", function () {
            const file = this.files[0];
            if (file) {
                const reader = new FileReader();
                reader.onload = function (e) {
                    mainPreview.src = e.target.result;
                };
                reader.readAsDataURL(file);
            }
        });

        deleteBtn.addEventListener("click", function (e) {
            e.preventDefault();
            const fallback = mainPreview.getAttribute("data-default");
            mainPreview.src = fallback || "";
            mainUpload.value = "";
        });
    }

    const galleryUpload = document.getElementById("galleryUpload");
    const galleryPreview = document.getElementById("gallery-preview");
    const addBanner = document.getElementById("add-banner");

    if (addBanner && galleryUpload && galleryPreview) {
        addBanner.addEventListener("click", function () {
            galleryUpload.click();
        });

        galleryUpload.addEventListener("change", function () {
            galleryPreview.innerHTML = "";
            Array.from(this.files).forEach(file => {
                const reader = new FileReader();
                reader.onload = function (e) {
                    const img = document.createElement("img");
                    img.src = e.target.result;
                    img.style.height = "100px";
                    img.style.margin = "5px";
                    img.style.border = "1px solid #ccc";
                    galleryPreview.appendChild(img);
                };
                reader.readAsDataURL(file);
            });
        });
    }
});
