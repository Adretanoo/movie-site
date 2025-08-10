$(document).ready(function () {
    AjaxDatatableViewUtils.initialize_table(
        $('#users_table'),
        "{% url 'ajax_datatable_users' %}",
        {
            info: false,
            processing: false,
            autoWidth: false,
            full_row_select: true,
            scrollX: false,
            lengthChange: false,
            order: [[0, 'asc']],
            language: {search: ""},
            pageLength: 10
        },
        {},
    );
    setTimeout(function () {
        $('#users_table_filter input').attr('placeholder', 'Поиск');
    }, 200);
});
