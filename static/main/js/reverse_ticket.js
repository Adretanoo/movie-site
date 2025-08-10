document.addEventListener('DOMContentLoaded', function() {
    const seats = document.querySelectorAll('.seat:not(.purchased):not(.blocked)');
    const ticketsSpan = document.querySelector('.count_tickets');
    const sumaSpan = document.querySelector('.suma_cost');
    const buyButton = document.querySelector('.reverse_ticket_buy_btn');
    const blockButton = document.querySelector('.reverse_ticket_blocked_btn');
    const csrfToken = document.querySelector('input[name="csrfmiddlewaretoken"]').value;
    const sessionId = document.querySelector('.block-seats-wrapper').dataset.sessionId;

    let selectedSeats = [];

    seats.forEach(seat => {
        seat.addEventListener('click', () => {
            seat.classList.toggle('selected-seat');

            const seatId = seat.dataset.id;
            if (seat.classList.contains('selected-seat')) {
                selectedSeats.push(seatId);
            } else {
                selectedSeats = selectedSeats.filter(id => id !== seatId);
            }

            updateOrderInfo();
        });
    });

    function handleSubmit(status) {
        if (selectedSeats.length === 0) {
            return;
        }

        const data = {
            'session_id': sessionId,
            'seat_ids': selectedSeats,
            'status': status
        };

        fetch('/buy-tickets/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken,
            },
            body: JSON.stringify(data),
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                window.location.reload();
            }
        })
    }

    buyButton.addEventListener('click', () => handleSubmit('purchased'));
    blockButton.addEventListener('click', () => handleSubmit('blocked'));

    function updateOrderInfo() {
        const totalTickets = selectedSeats.length;
        const totalSuma = totalTickets * ticketPrice;
        ticketsSpan.textContent = totalTickets;
        sumaSpan.textContent = totalSuma.toFixed(2);
    }
});
