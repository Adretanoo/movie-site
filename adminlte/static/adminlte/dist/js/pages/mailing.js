const radioButtons = document.querySelectorAll('input[name="selected_template"]');
const startButton = document.getElementById('start-button');
const deleteButton = document.getElementById('delete-button');
const all_users = document.getElementById('users-all-email');
const users_tok = document.getElementById('users-email');
const table_blocks = document.getElementsByClassName('block-table');

function hasSelectedUsers() {
    return document.querySelectorAll('input[name="selected_users"]:checked').length > 0;
}

function toggleButtons() {
    const selectedTemplate = document.querySelector('input[name="selected_template"]:checked');
    const isTemplateSelected = !!selectedTemplate;

    const isAllUsers = all_users.checked;
    const isSelective = users_tok.checked;
    const isUsersSelected = isAllUsers || (isSelective && hasSelectedUsers());

    startButton.disabled = !(isTemplateSelected && isUsersSelected);
    deleteButton.disabled = !isTemplateSelected;
}

function toggleTableBlock() {
    const shouldShow = users_tok.checked;
    for (const block of table_blocks) {
        block.style.display = shouldShow ? 'block' : 'none';
    }
    toggleButtons();
}

radioButtons.forEach(radio => {
    radio.addEventListener('change', toggleButtons);
});
all_users.addEventListener('change', toggleTableBlock);
users_tok.addEventListener('change', toggleTableBlock);

document.addEventListener('change', function (e) {
    if (e.target && e.target.name === 'selected_users') {
        toggleButtons();
    }
});

window.addEventListener('DOMContentLoaded', () => {
    toggleTableBlock();
    toggleButtons();
});
