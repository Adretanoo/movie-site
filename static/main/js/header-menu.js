document.addEventListener('DOMContentLoaded', function () {
    const openMenuButton = document.getElementById('openMenuButton');
    const closeMenuButton = document.getElementById('closeMenuButton');
    const fullScreenMenu = document.getElementById('fullScreenMenu');
    const dropdownWrappers = fullScreenMenu.querySelectorAll('.dropdown-wrapper');

    // Відкрити меню
    if (openMenuButton) {
        openMenuButton.addEventListener('click', function () {
            fullScreenMenu.classList.add('open');
        });
    }

    // Закрити меню
    if (closeMenuButton) {
        closeMenuButton.addEventListener('click', function () {
            fullScreenMenu.classList.remove('open');
        });
    }

    // Тогл підменю
    dropdownWrappers.forEach(wrapper => {
        const dropdownToggle = wrapper.querySelector('a:first-child');
        if (dropdownToggle) {
            dropdownToggle.addEventListener('click', function (event) {
                event.preventDefault();
                wrapper.classList.toggle('active');
            });
        }
    });

    // Клік поза підменю — закрити підменю
    document.addEventListener('click', function (event) {
        dropdownWrappers.forEach(wrapper => {
            const dropdownToggle = wrapper.querySelector('a:first-child');
            if (dropdownToggle && !wrapper.contains(event.target) && wrapper.classList.contains('active')) {
                wrapper.classList.remove('active');
            }
        });
    });

    // Закривати меню при кліку на всі посилання, крім трикутників
    fullScreenMenu.querySelectorAll('a:not(.dropdown-toggle):not(.dropdown-toggle-split)').forEach(link => {
        link.addEventListener('click', function () {
            fullScreenMenu.classList.remove('open');
        });
    });
});


document.addEventListener('DOMContentLoaded', function () {
    const currentDateElement = document.getElementById('current-date');
    const today = new Date();

    // Отримуємо поточну мову з Django-шаблону
    const currentLanguageFromDjango = "{{ CURRENT_LANGUAGE }}";

    function updateDateForLanguage(lang) {
        let options = {day: 'numeric', month: 'long'};
        let formattedDate;

        if (lang === 'uk') {
            formattedDate = new Intl.DateTimeFormat('uk-UA', options).format(today);
        } else if (lang === 'ru') {
            formattedDate = new Intl.DateTimeFormat('ru-RU', options).format(today);
        } else {
            formattedDate = new Intl.DateTimeFormat('uk-UA', options).format(today);
        }
        currentDateElement.textContent = formattedDate;
    }

    updateDateForLanguage(currentLanguageFromDjango);
});