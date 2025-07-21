document.querySelectorAll('.delete-button').forEach(button => {
    button.addEventListener('click', function (e) {
        e.preventDefault();
        const cinemaId = button.dataset.id;
        const cinemaName = button.dataset.title;

        document.getElementById('deleteModalText').innerText = `Видалити "${cinemaName}"?`;

        const form = document.getElementById('deleteForm');
        form.action = `/adminlte/cinemas/delete/`;

        // додай або онови приховане поле з cinema_id
        let hiddenInput = form.querySelector('input[name="cinema_id"]');
        if (!hiddenInput) {
            hiddenInput = document.createElement('input');
            hiddenInput.type = 'hidden';
            hiddenInput.name = 'cinema_id';
            form.appendChild(hiddenInput);
        }
        hiddenInput.value = cinemaId;

        document.getElementById('deleteModal').style.display = 'block';
    });
});

document.querySelector('.cancel-delete').addEventListener('click', function () {
    document.getElementById('deleteModal').style.display = 'none';
});
