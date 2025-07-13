function buttonImagePreviewClick() {
    document.getElementById('formPreview').click();
}

function updateImagePreview(input) {
    const mainPreview = document.getElementById('mainPreview');
    if (input.files && input.files[0]) {
        const file = input.files[0];
        mainPreview.src = URL.createObjectURL(file);
    }
}

function buttonResetPreviewClick() {
    const input = document.getElementById('formPreview');
    const preview = document.getElementById('mainPreview');
    input.value = '';
    preview.src = preview.dataset.default;
}

function buttonImagePreviewClickUpper(inputId) {
    document.getElementById(inputId).click();
}

function updateImagePreviewUpper(input, previewId) {
    const preview = document.getElementById(previewId);
    if (input.files && input.files[0]) {
        preview.src = URL.createObjectURL(input.files[0]);
    }
}

function buttonResetPreviewClickUpper(inputId, previewId) {
    const input = document.getElementById(inputId);
    const preview = document.getElementById(previewId);
    input.value = '';
    preview.src = preview.dataset.default;
}

function toggleFormVisibilityUpper(checkbox) {
    const formItem = checkbox.closest('.gallery-item');
    if (formItem) {
        const urlInput = formItem.querySelector('input[name$="-url"]');
        const imageFileInput = formItem.querySelector('input[name$="-image_file"]');

        if (checkbox.checked) {
            formItem.style.display = 'none';
            if (urlInput) {
                urlInput.removeAttribute('required');
                urlInput.value = '';
            }
            if (imageFileInput) {
                imageFileInput.removeAttribute('required');
                imageFileInput.value = '';
            }
        } else {
            formItem.style.display = '';
        }
    }
}

document.addEventListener('DOMContentLoaded', function () {
    const addButtonUpper = document.getElementById('add-more-upper');
    const containerUpper = document.getElementById('upper-banner-container');
    const emptyFormTemplateUpper = document.getElementById('upper-empty-form-template').innerHTML;
    const managementFormTotalFormsUpper = document.querySelector('#id_topbannerimage_set-TOTAL_FORMS');

    function updateElementIndexUpper(element, prefix, index) {
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
        if (element.getAttribute('onclick')) {
            const newOnClick = element.getAttribute('onclick').replace(/__prefix__/g, index);
            element.setAttribute('onclick', newOnClick);
        }
        if (element.getAttribute('onchange')) {
            if (element.getAttribute('onchange').includes('__prefix__')) {
                const newOnChange = element.getAttribute('onchange').replace(/__prefix__/g, index);
                element.setAttribute('onchange', newOnChange);
            }
        }
        if (element.id && element.id.startsWith('mainPreview')) {
            element.id = `mainPreview${index}`;
        }
    }

    function reindexFormsUpper() {
        let currentFormIndex = 0;
        containerUpper.querySelectorAll('.gallery-item').forEach(function (formDiv) {
            formDiv.querySelectorAll('input, select, textarea, label, button, img').forEach(function (element) {
                updateElementIndexUpper(element, 'topbannerimage_set', currentFormIndex);
            });
            formDiv.id = `gallery-item-${currentFormIndex}`;

            const deleteLabel = formDiv.querySelector('.delete-label');
            if (deleteLabel) {
                deleteLabel.setAttribute('for', `id_topbannerimage_set-${currentFormIndex}-DELETE`);
            }

            const deleteCheckbox = formDiv.querySelector('input[name$="-DELETE"][type="checkbox"]');
            if (deleteCheckbox) {
                deleteCheckbox.setAttribute('onchange', 'toggleFormVisibilityUpper(this);');
            }

            currentFormIndex++;
        });
        updateManagementFormTotalsUpper();
    }

    function updateManagementFormTotalsUpper() {
        const totalFormsInDOM = containerUpper.querySelectorAll('.gallery-item').length;
        managementFormTotalFormsUpper.value = totalFormsInDOM;
    }

    addButtonUpper.addEventListener('click', function () {
        const currentTotalForms = parseInt(managementFormTotalFormsUpper.value);
        const newFormHtml = emptyFormTemplateUpper.replace(/__prefix__/g, currentTotalForms);
        const newFormDiv = document.createElement('div');
        newFormDiv.innerHTML = newFormHtml.trim();
        const newFormElement = newFormDiv.firstElementChild;
        newFormElement.id = `gallery-item-${currentTotalForms}`;

        const newImageInput = newFormElement.querySelector(`input[name="topbannerimage_set-${currentTotalForms}-image_file"]`);
        if (newImageInput) {
            newImageInput.setAttribute('onchange', `updateImagePreviewUpper(this, "mainPreview${currentTotalForms}")`);
        }

        const newDeleteInput = newFormElement.querySelector('input[name$="-DELETE"][type="checkbox"]');
        if (newDeleteInput) {
            newDeleteInput.setAttribute('onchange', 'toggleFormVisibilityUpper(this);');
        }

        const newImagePreview = newFormElement.querySelector('img.image-preview');
        if (newImagePreview) {
            newImagePreview.id = `mainPreview${currentTotalForms}`;
        }

        containerUpper.appendChild(newFormElement);
        reindexFormsUpper();
    });

    containerUpper.addEventListener('change', function (event) {
        if (event.target.type === 'checkbox' && event.target.name.endsWith('-DELETE')) {
            toggleFormVisibilityUpper(event.target);
        }
    });

    reindexFormsUpper();
});


function buttonImagePreviewClickNews(inputId) {
    document.getElementById(inputId).click();
}

function updateImagePreviewNews(input, previewId) {
    const preview = document.getElementById(previewId);
    if (input.files && input.files[0]) {
        preview.src = URL.createObjectURL(input.files[0]);
    }
}

function buttonResetPreviewClickNews(inputId, previewId) {
    const input = document.getElementById(inputId);
    const preview = document.getElementById(previewId);
    input.value = '';
    preview.src = preview.dataset.default;
}

function toggleFormVisibilityNews(checkbox) {
    const formItem = checkbox.closest('.gallery-item');
    if (formItem) {
        const urlInput = formItem.querySelector('input[name$="-url"]');
        const textInput = formItem.querySelector('input[name$="-text"]');
        const imageFileInput = formItem.querySelector('input[name$="-image_file_shares"]');

        if (checkbox.checked) {
            formItem.style.display = 'none';
            if (urlInput) {
                urlInput.removeAttribute('required');
                urlInput.value = '';
            }
            if (textInput) {
                textInput.removeAttribute('required');
                textInput.value = '';
            }
            if (imageFileInput) {
                imageFileInput.removeAttribute('required');
                imageFileInput.value = '';
            }
        } else {
            formItem.style.display = '';

        }
    }
}

document.addEventListener('DOMContentLoaded', function () {
    const addButtonNews = document.getElementById('add-more-shares');
    const containerNews = document.getElementById('shares-banner-container');
    const emptyFormTemplateNews = document.getElementById('news-empty-form-template').innerHTML;
    const managementFormTotalFormsNews = document.querySelector('#id_newsbannerimage_set-TOTAL_FORMS');

    // Функція reindexFormsNews має бути оновлена, щоб враховувати 'mainPreviewNews'
    function updateElementIndexNews(element, prefix, index) {
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
        if (element.getAttribute('onclick')) {
            const newOnClick = element.getAttribute('onclick').replace(/__prefix__/g, index);
            element.setAttribute('onclick', newOnClick);
        }
        if (element.getAttribute('onchange')) {
            if (element.getAttribute('onchange').includes('__prefix__')) {
                const newOnChange = element.getAttribute('onchange').replace(/__prefix__/g, index);
                element.setAttribute('onchange', newOnChange);
            }
        }
        // Оновлено: Використовуємо 'mainPreviewNews' для унікальності ID в News Banner
        if (element.id && element.id.startsWith('mainPreview')) { // Перевіряємо, чи ID починається з "mainPreview"
            element.id = `mainPreviewNews${index}`; // Змінюємо на "mainPreviewNews"
        }
    }

    function reindexFormsNews() {
        let currentFormIndex = 0;
        containerNews.querySelectorAll('.gallery-item').forEach(function (formDiv) {
            formDiv.querySelectorAll('input, select, textarea, label, button, img').forEach(function (element) {
                updateElementIndexNews(element, 'newsbannerimage_set', currentFormIndex);
            });
            formDiv.id = `gallery-item-${currentFormIndex}`;

            const deleteLabel = formDiv.querySelector('.delete-label');
            if (deleteLabel) {
                deleteLabel.setAttribute('for', `id_newsbannerimage_set-${currentFormIndex}-DELETE`);
            }

            const deleteCheckbox = formDiv.querySelector('input[name$="-DELETE"][type="checkbox"]');
            if (deleteCheckbox) {
                deleteCheckbox.setAttribute('onchange', 'toggleFormVisibilityNews(this);');
            }

            currentFormIndex++;
        });
        updateManagementFormTotalsNews();
    }

    function updateManagementFormTotalsNews() {
        const totalFormsInDOM = containerNews.querySelectorAll('.gallery-item:not([style*="display: none"])').length; // Рахуємо тільки видимі форми
        managementFormTotalFormsNews.value = totalFormsInDOM;
    }

    addButtonNews.addEventListener('click', function () {
        const currentTotalForms = parseInt(managementFormTotalFormsNews.value);
        const newFormHtml = emptyFormTemplateNews.replace(/__prefix__/g, currentTotalForms);
        const newFormDiv = document.createElement('div');
        newFormDiv.innerHTML = newFormHtml.trim();
        const newFormElement = newFormDiv.firstElementChild;
        newFormElement.id = `gallery-item-${currentTotalForms}`;

        const newImageInput = newFormElement.querySelector(`input[name="newsbannerimage_set-${currentTotalForms}-image_file_shares"]`);
        if (newImageInput) {
            newImageInput.id = `id_newsbannerimage_set-${currentTotalForms}-image_file_shares`;
            newImageInput.setAttribute('onchange', `updateImagePreviewNews(this, "mainPreviewNews${currentTotalForms}")`);
        }

        const newLoadButton = newFormElement.querySelector('button[onclick*="__prefix__"]');
        if (newLoadButton) {
            newLoadButton.setAttribute('onclick', `buttonImagePreviewClickNews('id_newsbannerimage_set-${currentTotalForms}-image_file_shares')`);
        }

        const newImagePreview = newFormElement.querySelector('img.image-preview');
        if (newImagePreview) {
            newImagePreview.id = `mainPreviewNews${currentTotalForms}`; // Оновлено: Встановлюємо ID на 'mainPreviewNewsX'
        }

        const newDeleteInput = newFormElement.querySelector('input[name$="-DELETE"][type="checkbox"]');
        if (newDeleteInput) {
            newDeleteInput.setAttribute('onchange', 'toggleFormVisibilityNews(this);');
        }

        containerNews.appendChild(newFormElement);
        reindexFormsNews();
    });

    containerNews.addEventListener('change', function (event) {
        if (event.target.type === 'checkbox' && event.target.name.endsWith('-DELETE')) {
            toggleFormVisibilityNews(event.target);
        }
    });

    reindexFormsNews();
});