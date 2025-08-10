document.addEventListener('DOMContentLoaded', function () {
    const filterElements = document.querySelectorAll('select, input[type="checkbox"]');

    filterElements.forEach(element => {
        element.addEventListener('change', function () {
            const url = new URL(window.location.href);

            url.searchParams.delete('is_3d');
            url.searchParams.delete('is_2d');
            url.searchParams.delete('is_imax');

            document.querySelectorAll('input[type="checkbox"]').forEach(checkbox => {
                if (checkbox.checked) {
                    url.searchParams.set(checkbox.name, 'true');
                }
            });

            document.querySelectorAll('select').forEach(select => {
                if (select.value) {
                    url.searchParams.set(select.name, select.value);
                } else {
                    url.searchParams.delete(select.name);
                }
            });
            window.location.href = url.href;
        });
    });
});