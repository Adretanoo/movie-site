document.addEventListener('DOMContentLoaded', () => {
    const addBtn = document.getElementById('add-more-cinemas');
    const container = document.getElementById('forms-container');
    const emptyTemplate = document.getElementById('empty-form-template'); // Теперь это <template>
    const totalFormsInput = document.querySelector('#id_location_set-TOTAL_FORMS');
    const formPrefix = 'location_set';

    let formIdx = parseInt(totalFormsInput.value);

    const updateElementIndex = (el, prefix, newIndex) => {
        const idPattern = new RegExp(`(${prefix}-)(?:\\d+|__prefix__)(-)`);

        if (el.name) {
            el.name = el.name.replace(idPattern, `$1${newIndex}$2`);
        }
        if (el.id) {
            el.id = el.id.replace(idPattern, `$1${newIndex}$2`);
        }
        if (el.htmlFor) {
            el.htmlFor = el.htmlFor.replace(idPattern, `$1${newIndex}$2`);
        }
        if (el.dataset.inputId) {
            el.dataset.inputId = el.dataset.inputId.replace(idPattern, `$1${newIndex}$2`);
        }
    };

    const initFormEventListeners = (formElement, isFirstForm = false) => {
        const logoInput = formElement.querySelector('input[type="file"][name$="-logo"]');
        const logoPreview = formElement.querySelector('.logo-image img'); // Обновлено для logo-image img
        const uploadBtn = formElement.querySelector('.upload-button');
        const resetBtn = formElement.querySelector('.reset-button');

        if (logoInput) {
            if (uploadBtn) {
                uploadBtn.setAttribute('data-input-id', logoInput.id);
                uploadBtn.onclick = () => logoInput.click();
            }
            if (resetBtn) {
                resetBtn.setAttribute('data-input-id', logoInput.id);
                resetBtn.onclick = () => resetImage(logoInput, logoPreview);
            }
            logoInput.onchange = () => updatePreview(logoInput, logoPreview);
        }
        formElement.querySelectorAll('.text-danger').forEach(err => err.textContent = '');


        if (!isFirstForm) {
            const deleteButton = formElement.querySelector('.delete-button');
            if (deleteButton) {
                deleteButton.onclick = (e) => {
                    e.preventDefault(); // Предотвращаем стандартное действие ссылки
                    const formToDelete = deleteButton.closest('.formset-form');
                    if (formToDelete) {
                        const deleteInput = formToDelete.querySelector(`input[name$="-DELETE"]`);
                        if (deleteInput) {
                            deleteInput.checked = true;
                            formToDelete.style.display = 'none';
                        } else {
                            formToDelete.remove();
                            formIdx--;
                            totalFormsInput.value = formIdx;
                            reindexForms();
                        }
                    }
                };
            }
        }
    };

    const resetImage = (input, img) => {
        input.value = '';
        img.src = img.dataset.default;
    };

    const updatePreview = (input, img) => {
        const file = input.files[0];
        if (!file) {
            img.src = img.dataset.default;
            return;
        }
        const reader = new FileReader();
        reader.onload = e => img.src = e.target.result;
        reader.readAsDataURL(file);
    };

    addBtn.addEventListener('click', () => {
        const cloneContent = emptyTemplate.content.cloneNode(true);
        const newFormElement = cloneContent.querySelector('.block-upper-contacts-one');

        newFormElement.classList.add('formset-form');
        newFormElement.removeAttribute('id');

        newFormElement.querySelectorAll('[name], [id], label, [data-input-id]').forEach(el => updateElementIndex(el, formPrefix, formIdx));

        newFormElement.querySelectorAll('input, textarea').forEach(el => {
            if (el.type === 'checkbox') el.checked = false;
            else if (el.type !== 'hidden') el.value = '';
        });

        container.appendChild(newFormElement);

        initFormEventListeners(newFormElement, false);

        formIdx++; // Увеличиваем общий счетчик форм
        totalFormsInput.value = formIdx;
    });


    container.addEventListener('click', (e) => {
        const uploadButton = e.target.closest('.upload-button');
        if (uploadButton) {
            const inputId = uploadButton.dataset.inputId;
            const fileInput = document.getElementById(inputId);
            if (fileInput) {
                fileInput.click();
            }
        }

        const resetButton = e.target.closest('.reset-button');
        if (resetButton) {
            const inputId = resetButton.dataset.inputId;
            const fileInput = document.getElementById(inputId);
            const currentForm = resetButton.closest('.formset-form');
            const previewImage = currentForm.querySelector('.logo-image img');
            if (fileInput && previewImage) {
                resetImage(fileInput, previewImage);
            }
        }
    });

    container.addEventListener('change', (e) => {
        if (e.target.matches(`input[type="file"][name$="-logo"]`)) {
            const currentForm = e.target.closest('.formset-form');
            const previewImage = currentForm.querySelector('.logo-image img');
            if (previewImage) {
                updatePreview(e.target, previewImage);
            }
        }
    });

    const reindexForms = () => {
        const visibleForms = Array.from(container.querySelectorAll('.formset-form:not([style*="display: none"])'));

        visibleForms.forEach((formEl, index) => {
            formEl.querySelectorAll('[name], [id], label, [data-input-id]').forEach(el => updateElementIndex(el, formPrefix, index));

            const previewImg = formEl.querySelector('.logo-image img');
            if (previewImg) {
                previewImg.id = `logoPreview${index}`;
            }

            initFormEventListeners(formEl, index === 0);
        });
        formIdx = visibleForms.length;
        totalFormsInput.value = formIdx;
    };

    Array.from(document.querySelectorAll('.formset-form')).forEach((formEl, index) => {
        // Убеждаемся, что индексы актуальны при загрузке
        formEl.querySelectorAll('[name], [id], label, [data-input-id]').forEach(el => updateElementIndex(el, formPrefix, index));

        const previewImg = formEl.querySelector('.logo-image img');
        if (previewImg) {
            previewImg.id = `logoPreview${index}`;
        }
        initFormEventListeners(formEl, index === 0);
    });
});