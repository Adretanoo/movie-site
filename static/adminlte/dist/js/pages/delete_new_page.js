document.addEventListener("DOMContentLoaded", () => {
    const modal = document.getElementById("deleteModal");
    const modalText = document.getElementById("modal-text");
    const deleteForm = document.getElementById("delete-form");
    const cancelBtn = document.getElementById("cancel-button");
    const urlTemplate = modal.dataset.urlTemplate;

    let currentPubId = null;
    let currentRow = null;

    document.querySelectorAll(".delete-button").forEach(button => {
        button.addEventListener("click", function (e) {
            e.preventDefault();

            currentPubId = this.dataset.id;
            currentRow = this.closest("tr");

            const title = this.dataset.title || 'Новая страница';
            modalText.textContent = `Видалити «${title}»?`;
            modal.style.display = "flex";
        });
    });

    cancelBtn.addEventListener("click", () => {
        modal.style.display = "none";
        currentPubId = null;
        currentRow = null;
    });

    deleteForm.addEventListener("submit", async function (e) {
        e.preventDefault();
        if (!currentPubId) return;

        const deleteUrl = urlTemplate.replace("0", currentPubId);

        try {
            const response = await fetch(deleteUrl, {
                method: "POST",
                headers: {
                    "X-CSRFToken": getCSRFToken(),
                    "Accept": "application/json",
                    "Content-Type": "application/json",
                },
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const data = await response.json();

            if (data.success) {
                if (currentRow) currentRow.remove();
                modal.style.display = "none";
            } else {
                alert("Помилка: " + (data.error || "Невідома помилка"));
            }
        } catch (error) {
            console.error("AJAX Error:", error);
            alert("Сталася помилка при видаленні.");
        }
    });

    function getCSRFToken() {
        const name = 'csrftoken';
        const cookieValue = document.cookie
            .split('; ')
            .find(row => row.startsWith(name + '='))
            ?.split('=')[1];
        return cookieValue || '';
    }
});
