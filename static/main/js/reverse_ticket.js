document.addEventListener('DOMContentLoaded', function () {
    const seats = document.querySelectorAll('.seat');
    const ticketsSpan = document.querySelector('.count_tickets');
    const sumaSpan = document.querySelector('.suma_cost');
    const buyButton = document.querySelector('.reverse_ticket_buy_btn');
    const blockButton = document.querySelector('.reverse_ticket_blocked_btn');
    const sessionId = document.querySelector('.block-seats-wrapper').dataset.sessionId;

    let selectedSeats = [];

    function disableSeat(seatElement, status) {
        seatElement.classList.remove('selected-seat');
        seatElement.classList.remove('purchased', 'blocked');
        seatElement.classList.add(status);
        seatElement.style.cursor = 'not-allowed';
    }

    seats.forEach(seat => {
        seat.addEventListener('click', () => {
            if (seat.classList.contains('purchased') || seat.classList.contains('blocked')) {
                alert('Це місце вже зайняте або заброньоване!');
                return;
            }

            seat.classList.toggle('selected-seat');

            const seatId = seat.dataset.id;
            if (seat.classList.contains('selected-seat')) {
                if (!selectedSeats.includes(seatId)) {
                    selectedSeats.push(seatId);
                }
            } else {
                selectedSeats = selectedSeats.filter(id => id !== seatId);
            }

            updateOrderInfo();
        });
    });

    function handleSubmit(status) {
        const data = {
            session_id: sessionId,
            seat_ids: selectedSeats,
            status: status
        };

        fetch('/buy-tickets/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data),
        })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    // Оновлюємо візуальний стан місць на сторінці
                    selectedSeats.forEach(seatId => {
                        const seatElement = document.querySelector(`.seat[data-id="${seatId}"]`);
                        if (seatElement) {
                            disableSeat(seatElement, status);
                        }
                    });

                    // Після успішної операції, очищаємо масив обраних місць
                    // і оновлюємо інформацію про замовлення
                    selectedSeats = [];
                    updateOrderInfo();
                } else if (data.error) {
                    alert('Помилка: ' + data.error);
                }
            })
            .catch(() => {
                alert('Сталася помилка при з\'єднанні з сервером.');
            });
    }

    buyButton.addEventListener('click', () => handleSubmit('purchased'));
    blockButton.addEventListener('click', () => handleSubmit('blocked'));

    function updateOrderInfo() {
        const currentlySelectedSeats = document.querySelectorAll('.seat.selected-seat:not(.purchased):not(.blocked)');
        selectedSeats = Array.from(currentlySelectedSeats).map(seat => seat.dataset.id);

        const totalTickets = selectedSeats.length;
        const totalSuma = totalTickets * ticketPrice;
        ticketsSpan.textContent = totalTickets;
        sumaSpan.textContent = totalSuma.toFixed(2);
    }

    const socket = new WebSocket(`ws://${window.location.host}/ws/session/${sessionId}/`);

    socket.onmessage = function (event) {
        const data = JSON.parse(event.data);
        if (!data.tickets) return;

        data.tickets.forEach(ticket => {
            const seatElement = document.querySelector(`.seat[data-id="${ticket.id}"]`);
            if (!seatElement) return;
            disableSeat(seatElement, ticket.status);
        });


        selectedSeats = selectedSeats.filter(id => {
            const el = document.querySelector(`.seat[data-id="${id}"]`);
            return el && !el.classList.contains('purchased') && !el.classList.contains('blocked');
        });

        updateOrderInfo();
    };
});
