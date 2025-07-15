    document.addEventListener('DOMContentLoaded', () => {
    const deleteButtons = document.querySelectorAll('.delete-button');
    const modal = document.getElementById('deleteModal');
    const modalText = document.getElementById('deleteModalText');
    const movieIdInput = document.getElementById('deleteMovieId');
    const cancelBtn = document.querySelector('.cancel-delete');

    deleteButtons.forEach(button => {
        button.addEventListener('click', e => {
            e.preventDefault();
            const movieId = button.getAttribute('data-id');
            const movieTitle = button.getAttribute('data-title');
            modalText.textContent = `Ви точно хочете видалити фільм: "${movieTitle}"?`;
            movieIdInput.value = movieId;
            modal.style.display = 'block';
        });
    });

    cancelBtn.addEventListener('click', () => {
        modal.style.display = 'none';
    });

    // Закриття по кліку поза модальним вікном
    window.addEventListener('click', (e) => {
        if (e.target === modal) {
            modal.style.display = 'none';
        }
    });
});