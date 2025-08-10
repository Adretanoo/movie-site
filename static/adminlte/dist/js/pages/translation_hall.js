const translationsCache = { uk: {}, ru: {} };

function updateFieldVisibility(lang) {
    document.querySelectorAll('.lang-field').forEach(field => {
        field.style.display = 'none';
    });
    document.querySelectorAll(`.lang-${lang}`).forEach(field => {
        field.style.display = 'flex';
    });
}

function cacheCurrentTranslations(lang) {
    if (!lang) return;
    translationsCache[lang].title = document.querySelector(`[name="name_${lang}"]`)?.value || '';
    translationsCache[lang].description = document.querySelector(`[name="description_${lang}"]`)?.value || '';
}

function restoreCachedTranslations(lang) {
    const cached = translationsCache[lang] || {};
    const setValue = (selector, value) => {
        const el = document.querySelector(selector);
        if (el) el.value = value || '';
    };
    setValue(`[name="name_${lang}"]`, cached.title);
    setValue(`[name="description_${lang}"]`, cached.description);
}

document.addEventListener("DOMContentLoaded", () => {
    const langButtons = document.querySelectorAll(".lang-buttons a");
    const currentLang = new URLSearchParams(window.location.search).get("lang") || "ru";

    updateFieldVisibility(currentLang);
    cacheCurrentTranslations(currentLang);

    langButtons.forEach(button => {
        button.addEventListener("click", function (e) {
            e.preventDefault();
            const newLang = this.dataset.lang;

            const current = document.querySelector(".lang-buttons a.active")?.dataset.lang;
            if (current) cacheCurrentTranslations(current);

            langButtons.forEach(btn => btn.classList.remove("active"));
            this.classList.add("active");

            restoreCachedTranslations(newLang);
            updateFieldVisibility(newLang);
        });
    });
});


