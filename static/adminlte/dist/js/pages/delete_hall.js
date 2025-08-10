document.querySelectorAll('.delete-button').forEach(button => {
    button.addEventListener('click', function (e) {
        e.preventDefault();
        const hallId = button.dataset.id;
        const hallName = button.dataset.title;

        document.getElementById('deleteModalText').innerText = `Видалити зал"${hallName}"?`;
        document.getElementById('deleteForm').action = `/adminlte/hall/delete/${hallId}/`;
        document.getElementById('deleteModal').style.display = 'block';
    });
});

document.querySelector('.cancel-delete').addEventListener('click', function () {
    document.getElementById('deleteModal').style.display = 'none';
});
