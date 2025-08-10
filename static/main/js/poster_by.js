document.addEventListener('DOMContentLoaded', function () {
    const dateCards = document.querySelectorAll('.block-movie-card');
    const sessionBlocks = document.querySelectorAll('.block-session-item');
    const buyTicketBtn = document.getElementById('buy-ticket-btn');
    const filterForm = document.getElementById('filter-form');
    const cinemaSelect = filterForm.querySelector('select[name="cinema"]');

    let selectedSessionId = null;

    cinemaSelect.addEventListener('change', function () {
        filterForm.submit();
    });

    filterForm.querySelectorAll('input[type="checkbox"]').forEach(checkbox => {
        checkbox.addEventListener('change', function() {
            // Оновлюємо візуальний стиль
            const label = this.closest('.checkbox_filters_item').querySelector('label');
            if (this.checked) {
                label.classList.add('active');
            } else {
                label.classList.remove('active');
            }

            // Запускаємо клієнтську фільтрацію
            const activeDateCard = document.querySelector('.block-movie-card.active');
            if (activeDateCard) {
                const selectedDate = activeDateCard.getAttribute('data-date');
                filterSessionsByDateAndFormat(selectedDate);
            }
        });
    });

    function filterSessionsByDateAndFormat(selectedDate) {
        // Отримуємо активні фільтри форматів
        const is3D = document.getElementById('3d')?.checked;
        const is2D = document.getElementById('2d')?.checked;
        const isIMAX = document.getElementById('IMAX')?.checked;

        sessionBlocks.forEach(block => {
            const blockDate = block.getAttribute('data-date');
            const blockFormat = block.getAttribute('data-format');

            // Перевіряємо, чи сеанс відповідає обраній даті
            const dateMatch = blockDate === selectedDate;

            // Перевіряємо, чи сеанс відповідає формату (якщо чекбокси активні)
            let formatMatch = false;
            if (is3D || is2D || isIMAX) {
                if (is3D && blockFormat === '3d') formatMatch = true;
                if (is2D && blockFormat === '2d') formatMatch = true;
                if (isIMAX && blockFormat === 'imax') formatMatch = true;
            } else {
                formatMatch = true;
            }

            if (dateMatch && formatMatch) {
                block.style.display = 'grid';
            } else {
                block.style.display = 'none';
                block.classList.remove('active');
            }
        });
    }

    dateCards.forEach(card => {
        card.addEventListener('click', function () {
            dateCards.forEach(c => c.classList.remove('active'));
            this.classList.add('active');

            const selectedDate = this.getAttribute('data-date');
            filterSessionsByDateAndFormat(selectedDate);

            selectedSessionId = null;
            buyTicketBtn.classList.add('disabled');
            buyTicketBtn.href = 'javascript:void(0);';
        });
    });
    sessionBlocks.forEach(block => {
        block.addEventListener('click', function () {
            sessionBlocks.forEach(s => s.classList.remove('active'));
            this.classList.add('active');
            selectedSessionId = this.getAttribute('data-session-id');
            buyTicketBtn.classList.remove('disabled');
            buyTicketBtn.href = `/uk/session/${selectedSessionId}/reverse-ticket/`;
        });
    });

    function initializePage() {
        filterForm.querySelectorAll('input[type="checkbox"]').forEach(checkbox => {
            const label = checkbox.closest('.checkbox_filters_item').querySelector('label');
            if (checkbox.checked) {
                label.classList.add('active');
            } else {
                label.classList.remove('active');
            }
        });

        // Імітуємо клік на першу дату, щоб відобразити сеанси
        if (dateCards.length > 0) {
            dateCards[0].click();
        }
    }
    initializePage();
});