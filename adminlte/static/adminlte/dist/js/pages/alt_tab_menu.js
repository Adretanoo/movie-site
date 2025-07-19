document.addEventListener("keydown", function (e) {
    const activeElement = document.activeElement;
    const isInputFocused = activeElement.tagName === 'INPUT' || activeElement.tagName === 'TEXTAREA';

    if (e.key === "Tab" && !isInputFocused) {
        e.preventDefault();

        const currentLang = document.querySelector(".lang-buttons a.active")?.dataset.lang;
        const newLang = currentLang === "uk" ? "ru" : "uk";

        cacheCurrentTranslations(currentLang);

        const langButtons = document.querySelectorAll(".lang-buttons a");
        langButtons.forEach(btn => btn.classList.remove("active"));

        const newLangBtn = document.querySelector(`.lang-buttons a[data-lang="${newLang}"]`);
        if (newLangBtn) {
            newLangBtn.classList.add("active");
        }

        restoreCachedTranslations(newLang);
        updateFieldVisibility(newLang);
    }
});


document.addEventListener("DOMContentLoaded", function () {
    const form = document.getElementById("movieForm");
    const saveButton = form.querySelector(".all-save-button");

    saveButton.addEventListener("click", function (e) {
        const langs = ["uk", "ru"];
        let switchToLang = null;

        langs.forEach(lang => {
            const requiredFields = document.querySelectorAll(`.lang-${lang} [required]`);
            for (const field of requiredFields) {
                if (!field.value.trim()) {
                    switchToLang = lang;
                    break;
                }
            }
        });

        if (switchToLang) {
            document.querySelectorAll(".lang-buttons a").forEach(btn => {
                btn.classList.remove("active");
            });
            const btn = document.querySelector(`.lang-buttons a[data-lang="${switchToLang}"]`);
            btn?.classList.add("active");

            updateFieldVisibility(switchToLang);
        }
    });
});