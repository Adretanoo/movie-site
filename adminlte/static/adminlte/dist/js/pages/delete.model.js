document.addEventListener("DOMContentLoaded", () => {
    const modal = document.getElementById("deleteModal");
    const modalText = document.getElementById("modal-text");
    const deleteForm = document.getElementById("delete-form");
    const cancelBtn = document.getElementById("cancel-button");

    const urlTemplate = modal.dataset.urlTemplate;

    document.querySelectorAll(".delete-button").forEach(button => {
        button.addEventListener("click", function (e) {
            e.preventDefault();
            const pubId = this.dataset.id;
            const title = this.dataset.title;

            modalText.textContent = `Видалити «${title}»?`;
            deleteForm.action = urlTemplate.replace("9999", pubId);

            modal.style.display = "flex";  // або block, залежить від стилів
        });
    });

    cancelBtn.addEventListener("click", () => {
        modal.style.display = "none";
        deleteForm.action = "";
    });
});