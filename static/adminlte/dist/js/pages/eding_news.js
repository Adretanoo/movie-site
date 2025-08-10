const translationsCache = {
    uk: {},
    ru: {}
};

let currentLang = "ru";  // Мова за замовчуванням, можеш замінити

function cacheCurrentTranslations(lang) {
    if (!lang) return;

    translationsCache[lang].title = document.querySelector(`[name="title_${lang}"]`)?.value || '';
    translationsCache[lang].description = document.querySelector(`[name="description_${lang}"]`)?.value || '';
}

function restoreCachedTranslations(lang) {
    const cached = translationsCache[lang] || {};

    const title = document.querySelector(`[name="title_${lang}"]`);
    if (title) title.value = cached.title || title.value;

    const description = document.querySelector(`[name="description_${lang}"]`);
    if (description) description.value = cached.description || description.value;
}

function switchLanguage(lang) {
    cacheCurrentTranslations(currentLang);
    restoreCachedTranslations(lang);

    // Показуємо тільки потрібну мову
    document.querySelectorAll('.lang-field').forEach(el => {
        el.style.display = el.classList.contains(`lang-${lang}`) ? '' : 'none';
    });

    // Активна кнопка
    document.querySelectorAll('.lang-buttons a').forEach(btn => {
        btn.classList.remove('active');
    });
    document.querySelector(`.lang-buttons a[data-lang="${lang}"]`)?.classList.add('active');

    currentLang = lang;
}

document.addEventListener("DOMContentLoaded", () => {
    const langButtons = document.querySelectorAll(".lang-buttons a");

    // Перехоплюємо кліки
    langButtons.forEach(button => {
        button.addEventListener("click", function (e) {
            e.preventDefault();
            const selectedLang = this.dataset.lang;
            if (selectedLang !== currentLang) {
                switchLanguage(selectedLang);
            }
        });
    });

    // Ініціалізуємо на старті
    switchLanguage(currentLang);
});
