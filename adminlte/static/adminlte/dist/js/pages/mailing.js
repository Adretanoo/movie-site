const textareaSms = document.getElementById('sms-massage')
const spanCount = document.getElementById('char-count')

textareaSms.addEventListener("input", function () {
    let count = this.value.length
    spanCount.innerText = count
})


document.addEventListener('DOMContentLoaded', () => {
    const usersAllEmailRadio = document.getElementById('users-all-email');
    const usersEmailRadio = document.getElementById('users-email');
    const selectUsersButton = document.querySelector('.button-email-users');
    const uploadHtmlButton = document.getElementById('upload-html-button');
    const actualFileInput = document.getElementById('actual-file-input'); // New: reference to hidden file input
    const uploadedFileNameSpan = document.getElementById('uploaded-file-name');
    const currentTemplateNameSpan = document.getElementById('current-template-name');
    const templateList = document.getElementById('template-list');
    const startMallingButton = document.getElementById('start-malling-button');

    // Hint boxes
    const hintTopLeft = document.getElementById('hint-top-left');
    const hintBottomRight = document.getElementById('hint-bottom-right');

    // Initial state for user selection button
    if (usersEmailRadio.checked) {
        selectUsersButton.style.display = 'inline-block';
    }

    usersAllEmailRadio.addEventListener('change', () => {
        if (usersAllEmailRadio.checked) {
            selectUsersButton.style.display = 'none';
        }
    });

    usersEmailRadio.addEventListener('change', () => {
        if (usersEmailRadio.checked) {
            selectUsersButton.style.display = 'inline-block';
        }
    });

    let templates = [];

    // Function to render templates
    const renderTemplates = () => {
        templateList.innerHTML = ''; // Clear current list
        templates.forEach(template => {
            const listItem = document.createElement('li');
            listItem.classList.add('template-item');
            listItem.innerHTML = `
                        <input type="radio" id="template-${template.id}" name="selected_template" value="${template.name}" ${template.selected ? 'checked' : ''}>
                        <label for="template-${template.id}">${template.name}</label>
                        <button class="delete-link" data-id="${template.id}">Удалить</button>
                    `;
            templateList.appendChild(listItem);
        });

        // Set initial current template name if one is selected
        const initiallySelected = templates.find(t => t.selected);
        if (initiallySelected) {
            currentTemplateNameSpan.textContent = initiallySelected.name;
            uploadedFileNameSpan.textContent = initiallySelected.name; // Also update uploaded file name
        } else if (templates.length > 0) {
            // If no initial selected, default to the first one
            templates[0].selected = true;
            currentTemplateNameSpan.textContent = templates[0].name;
            uploadedFileNameSpan.textContent = templates[0].name;
        } else {
            currentTemplateNameSpan.textContent = ''; // No templates
            uploadedFileNameSpan.textContent = '';
        }
    };

    // Event listener for template selection
    templateList.addEventListener('change', (event) => {
        if (event.target.name === 'selected_template') {
            templates.forEach(t => t.selected = false); // Deselect all
            const selectedTemplate = templates.find(t => t.name === event.target.value);
            if (selectedTemplate) {
                selectedTemplate.selected = true; // Select the clicked one
                currentTemplateNameSpan.textContent = selectedTemplate.name;
                uploadedFileNameSpan.textContent = selectedTemplate.name; // Update uploaded file name as well
            }
        }
    });

    // Event listener for template deletion
    templateList.addEventListener('click', (event) => {
        if (event.target.classList.contains('delete-link')) {
            const templateIdToDelete = parseInt(event.target.dataset.id);
            const deletedTemplate = templates.find(t => t.id === templateIdToDelete);

            // Check if the deleted template was the current one
            if (deletedTemplate && deletedTemplate.selected) {
                currentTemplateNameSpan.textContent = ''; // Clear current template display
                uploadedFileNameSpan.textContent = ''; // Clear uploaded file display
            }

            templates = templates.filter(template => template.id !== templateIdToDelete);

            // If the current template was deleted, select the first remaining one (if any)
            if (!currentTemplateNameSpan.textContent && templates.length > 0) {
                templates[0].selected = true;
                currentTemplateNameSpan.textContent = templates[0].name;
                uploadedFileNameSpan.textContent = templates[0].name;
            } else if (templates.length === 0) {
                currentTemplateNameSpan.textContent = '';
                uploadedFileNameSpan.textContent = '';
            }

            renderTemplates(); // Re-render the list
        }
    });

    // Handle "Загрузить" button click to trigger hidden file input
    uploadHtmlButton.addEventListener('click', () => {
        actualFileInput.click(); // Programmatically click the hidden file input
    });

    // Handle file selection
    actualFileInput.addEventListener('change', (event) => {
        const file = event.target.files[0];
        if (file) {
            const fileName = file.name;
            uploadedFileNameSpan.textContent = fileName;

            // Add the newly uploaded file as a template
            const newId = templates.length > 0 ? Math.max(...templates.map(t => t.id)) + 1 : 1;
            const newTemplate = {id: newId, name: fileName, selected: false};

            // Add to the beginning and keep only the last 5
            templates.unshift(newTemplate);
            templates = templates.slice(0, 5); // Keep only the latest 5

            // Select the newly uploaded template
            templates.forEach(t => t.selected = false);
            newTemplate.selected = true;
            currentTemplateNameSpan.textContent = newTemplate.name;

            renderTemplates(); // Re-render the list
        }
    });

    // Show hint box on hover over the "Начать рассылку" button
    startMallingButton.addEventListener('mouseenter', () => {
        hintBottomRight.style.display = 'block';
    });

    startMallingButton.addEventListener('mouseleave', () => {
        hintBottomRight.style.display = 'none';
    });

    // Show hint box for user selection (always visible as per image)
    hintTopLeft.style.display = 'block';

    // Initial render of templates
    renderTemplates();
});