function buttonImagePreviewClick(inputId) {
    const input = document.getElementById(inputId);
    if (input) input.click();
}

function updateImagePreview(input, previewId) {
    const preview = document.getElementById(previewId);
    if (input.files && input.files[0]) {
        preview.src = URL.createObjectURL(input.files[0]);
    }
}

function buttonResetPreviewClick(inputId, previewId) {
    const input = document.getElementById(inputId);
    const preview = document.getElementById(previewId);
    if (input && preview) {
        input.value = '';
        preview.src = preview.dataset.default;
    }
}



function toggleFormVisibility(checkbox) {
    const formItem = checkbox.closest('.gallery-item');
    if (formItem) {
        const formFields = formItem.querySelectorAll('input:not([type="hidden"]):not([type="checkbox"]), select, textarea');

        if (checkbox.checked) {
            formItem.style.display = 'none';
            formFields.forEach(field => {
                // Зберігаємо оригінальний стан 'required' перед видаленням
                field.setAttribute('data-original-required', field.hasAttribute('required') ? 'true' : 'false');
                field.removeAttribute('required');
                field.setAttribute('disabled', 'true'); // Вимикаємо поля
            });
            const imageFileInput = formItem.querySelector('input[type="file"]');
            if (imageFileInput) {
                imageFileInput.value = '';
            }
        } else {
            formItem.style.display = '';
            formFields.forEach(field => {
                if (field.getAttribute('data-original-required') === 'true') {
                    field.setAttribute('required', 'true');
                }
                field.removeAttribute('disabled'); // Вмикаємо поля
            });
        }
    }
}

function initDynamicFormset(config) {
    const addButton = document.getElementById(config.addButtonId);
    const container = document.getElementById(config.containerId);
    const emptyFormTemplate = document.getElementById(config.templateId).innerHTML;
    const managementFormTotalForms = document.querySelector(config.totalFormsSelector);

    function updateElementIndex(element, prefix, index) {
        if (element.name && (element.name.includes('TOTAL_FORMS') || element.name.includes('INITIAL_FORMS') || element.name.includes('MAX_NUM_FORMS'))) {
            return;
        }

        const idRegex = new RegExp(`(${prefix}-(\\d+)-)|(${prefix}-__prefix__-)`);
        const nameRegex = new RegExp(`(${prefix}-(\\d+)-)|(${prefix}-__prefix__-)`);
        const forRegex = new RegExp(`(${prefix}-(\\d+)-)|(${prefix}-__prefix__-)`);

        if (element.id) {
            element.id = element.id.replace(idRegex, `${prefix}-${index}-`);
        }
        if (element.name) {
            element.name = element.name.replace(nameRegex, `${prefix}-${index}-`);
        }
        if (element.htmlFor) {
            element.htmlFor = element.htmlFor.replace(forRegex, `${prefix}-${index}-`);
        }

        if (element.getAttribute('onclick') && element.getAttribute('onclick').includes('__prefix__')) {
            const newOnClick = element.getAttribute('onclick').replace(/__prefix__/g, index);
            element.setAttribute('onclick', newOnClick);
        }
        if (element.getAttribute('onchange') && element.getAttribute('onchange').includes('__prefix__')) {
            const newOnChange = element.getAttribute('onchange').replace(/__prefix__/g, index);
            element.setAttribute('onchange', newOnChange);
        }

        if (element.classList.contains('image-preview')) {
            element.id = `${config.previewPrefix}${index}`;
        }
    }
    function reindexForms() {
        let currentFormIndex = 0;
        container.querySelectorAll('.gallery-item').forEach(function (formDiv) {
            formDiv.querySelectorAll('input, select, textarea, label, button, img').forEach(function (element) {
                updateElementIndex(element, config.prefix, currentFormIndex);
            });
            formDiv.id = `${config.galleryItemIdPrefix}-${currentFormIndex}`;
            const deleteLabel = formDiv.querySelector('.delete-label');
            if (deleteLabel) {
                deleteLabel.setAttribute('for', `id_${config.prefix}-${currentFormIndex}-DELETE`);
            }
            const deleteCheckbox = formDiv.querySelector('input[name$="-DELETE"][type="checkbox"]');
            if (deleteCheckbox) {
                deleteCheckbox.setAttribute('onchange', 'toggleFormVisibility(this);');
            }
            const imageFileInput = formDiv.querySelector(`input[name="${config.prefix}-${currentFormIndex}-${config.imageFieldName}"]`);
            if (imageFileInput) {
                imageFileInput.setAttribute('onchange', `updateImagePreview(this, "${config.previewPrefix}${currentFormIndex}")`);
            }
            const loadImageButton = formDiv.querySelector(`button[onclick*="buttonImagePreviewClick"]`);
            if (loadImageButton) {
                loadImageButton.setAttribute('onclick', `buttonImagePreviewClick('id_${config.prefix}-${currentFormIndex}-${config.imageFieldName}')`);
            }

            currentFormIndex++;
        });
        updateManagementFormTotals();
    }

    function updateManagementFormTotals() {
        const totalFormsInDOM = container.querySelectorAll('.gallery-item').length;
        managementFormTotalForms.value = totalFormsInDOM;
    }

    addButton.addEventListener('click', function () {
        const currentTotalForms = parseInt(managementFormTotalForms.value);
        const newFormHtml = emptyFormTemplate.replace(/__prefix__/g, currentTotalForms);
        const newFormDiv = document.createElement('div');
        newFormDiv.innerHTML = newFormHtml.trim();
        const newFormElement = newFormDiv.firstElementChild;
        newFormElement.id = `${config.galleryItemIdPrefix}-${currentTotalForms}`;

        container.appendChild(newFormElement);
        reindexForms();
    });

    container.addEventListener('change', function (event) {
        if (event.target.type === 'checkbox' && event.target.name.endsWith('-DELETE')) {
            toggleFormVisibility(event.target);
        }
    });

    reindexForms();
}

document.addEventListener('DOMContentLoaded', function () {
    initDynamicFormset({
        addButtonId: 'add-more-upper',
        containerId: 'upper-banner-container',
        templateId: 'upper-empty-form-template',
        totalFormsSelector: '#id_topbannerimage_set-TOTAL_FORMS',
        prefix: 'topbannerimage_set',
        imageFieldName: 'image_file',
        previewPrefix: 'mainPreview',
        galleryItemIdPrefix: 'gallery-item'
    });

    initDynamicFormset({
        addButtonId: 'add-more-shares',
        containerId: 'shares-banner-container',
        templateId: 'news-empty-form-template',
        totalFormsSelector: '#id_newsbannerimage_set-TOTAL_FORMS',
        prefix: 'newsbannerimage_set',
        imageFieldName: 'image_file_shares',
        previewPrefix: 'mainPreviewNews',
        galleryItemIdPrefix: 'gallery-item'
    });

    const formPreviewInput = document.getElementById('formPreview');
    const mainPreviewImg = document.getElementById('mainPreview');

    if (formPreviewInput && mainPreviewImg) {
        formPreviewInput.addEventListener('change', function() {
            updateImagePreview(this, 'mainPreview');
        });
    }
    window.buttonImagePreviewClick = buttonImagePreviewClick;
    window.updateImagePreview = updateImagePreview;
    window.buttonResetPreviewClick = buttonResetPreviewClick;
    window.toggleFormVisibility = toggleFormVisibility;
});