document.addEventListener('DOMContentLoaded', function () {
    document.body.addEventListener('click', function (e) {
        const btn = e.target.closest('.delete-button');
        if (!btn) return;

        e.preventDefault();
        const userId = btn.dataset.id;
        const userName = btn.dataset.title;
        const deleteUrl = btn.dataset.url; // тепер отримуємо URL

        const modal = document.getElementById('deleteModal');
        const text = document.getElementById('deleteModalText');
        const form = document.getElementById('deleteForm');

        text.innerText = `Ви точно хочете видалити "${userName}"?`;
        form.action = deleteUrl;

        let hiddenInput = form.querySelector('input[name="user_id"]');
        if (!hiddenInput) {
            hiddenInput = document.createElement('input');
            hiddenInput.type = 'hidden';
            hiddenInput.name = 'user_id';
            form.appendChild(hiddenInput);
        }
        hiddenInput.value = userId;

        modal.style.display = 'block';
    });

    document.querySelector('.cancel-delete').addEventListener('click', function () {
        document.getElementById('deleteModal').style.display = 'none';
    });
});
