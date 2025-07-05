document.querySelectorAll('.delete-button').forEach(btn => {
    btn.addEventListener('click', e => {
        e.preventDefault();
        const id = btn.dataset.id;
        const title = btn.dataset.title;

        document.getElementById('modal-text').innerText = `Видалити публікацію "${title}"?`;
        const form = document.getElementById('delete-form');
        form.action = `/pages/news/delete/${id}/`;

        document.getElementById('deleteModal').style.display = 'flex';
    });
});

document.getElementById('cancel-button').addEventListener('click', () => {
    document.getElementById('deleteModal').style.display = 'none';
});