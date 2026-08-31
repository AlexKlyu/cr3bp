/* Bilingual layer (en / ru).
 *
 * Markup contract:
 *   <p data-i18n="key">                  -> innerHTML swapped
 *   <meta data-i18n-attr-content="key">  -> attribute swapped (content/alt/title/...)
 *
 * Strings live in a per-page dictionary that sets window.I18N_STRINGS to
 * { key: { en: "...", ru: "..." } }. English is what sits in the HTML itself,
 * so the page is fully readable with JavaScript disabled.
 *
 * Language choice, highest priority first:
 *   1. ?lang=ru | ?lang=en          explicit link or shared URL
 *   2. localStorage                 the visitor's own earlier choice
 *   3. navigator.languages          browser UI / accept-language
 *   4. IANA timezone                geographic fallback (Russian zones)
 *   5. 'en'
 */
(function () {
  'use strict';

  var LANGS = ['en', 'ru'];
  var current = 'en';
  var STORAGE_KEY = 'cr3bp_lang';

  // Russian timezones - the offline stand-in for a GeoIP lookup. A visitor whose
  // browser is English but whose clock is set to Russia still lands on Russian.
  var RU_ZONES = [
    'Europe/Moscow', 'Europe/Kaliningrad', 'Europe/Samara', 'Europe/Saratov',
    'Europe/Volgograd', 'Europe/Astrakhan', 'Europe/Ulyanovsk', 'Europe/Kirov',
    'Asia/Yekaterinburg', 'Asia/Omsk', 'Asia/Novosibirsk', 'Asia/Novokuznetsk',
    'Asia/Barnaul', 'Asia/Tomsk', 'Asia/Krasnoyarsk', 'Asia/Irkutsk',
    'Asia/Chita', 'Asia/Yakutsk', 'Asia/Khandyga', 'Asia/Ust-Nera',
    'Asia/Vladivostok', 'Asia/Srednekolymsk', 'Asia/Magadan', 'Asia/Sakhalin',
    'Asia/Kamchatka', 'Asia/Anadyr'
  ];

  function safeStorage(fn, fallback) {
    try { return fn(); } catch (e) { return fallback; }
  }

  function detect() {
    var q = new URLSearchParams(location.search).get('lang');
    if (q && LANGS.indexOf(q) !== -1) return q;

    var saved = safeStorage(function () { return localStorage.getItem(STORAGE_KEY); }, null);
    if (saved && LANGS.indexOf(saved) !== -1) return saved;

    var navLangs = navigator.languages || [navigator.language || ''];
    for (var i = 0; i < navLangs.length; i++) {
      var tag = String(navLangs[i]).toLowerCase();
      if (tag.indexOf('ru') === 0) return 'ru';
      if (tag.indexOf('en') === 0) return 'en';
    }

    var zone = safeStorage(function () {
      return Intl.DateTimeFormat().resolvedOptions().timeZone;
    }, null);
    if (zone && RU_ZONES.indexOf(zone) !== -1) return 'ru';

    return 'en';
  }

  // Resolve eagerly so t() is already correct for any page script that runs
  // before DOMContentLoaded.
  current = detect();

  function apply(lang) {
    var dict = window.I18N_STRINGS || {};

    document.documentElement.lang = lang;

    document.querySelectorAll('[data-i18n]').forEach(function (el) {
      var entry = dict[el.getAttribute('data-i18n')];
      if (entry && entry[lang] != null) el.innerHTML = entry[lang];
    });

    document.querySelectorAll('*').forEach(function (el) {
      for (var i = 0; i < el.attributes.length; i++) {
        var attr = el.attributes[i];
        if (attr.name.indexOf('data-i18n-attr-') !== 0) continue;
        var target = attr.name.slice('data-i18n-attr-'.length);
        var entry = dict[attr.value];
        if (entry && entry[lang] != null) el.setAttribute(target, entry[lang]);
      }
    });

    // <title> carries no innerHTML hook of its own in some browsers' parsing,
    // so mirror whatever the title element ended up holding.
    var t = document.querySelector('title[data-i18n]');
    if (t) document.title = t.textContent;

    var canonical = document.querySelector('link[rel="canonical"]');
    if (canonical) {
      var url = new URL(canonical.href, location.href);
      if (lang === 'en') url.searchParams.delete('lang');
      else url.searchParams.set('lang', lang);
      canonical.href = url.href;
    }

    current = lang;
    document.documentElement.setAttribute('data-lang', lang);
    // Content was hidden until now to avoid flashing the source language.
    document.documentElement.classList.remove('i18n-pending');
    document.dispatchEvent(new CustomEvent('i18n:applied', { detail: { lang: lang } }));
  }

  function setLang(lang) {
    if (LANGS.indexOf(lang) === -1) return;
    safeStorage(function () { return localStorage.setItem(STORAGE_KEY, lang); }, null);
    var url = new URL(location.href);
    url.searchParams.set('lang', lang);
    history.replaceState(null, '', url);
    apply(lang);
    renderSwitcher(lang);
  }

  function renderSwitcher(current) {
    var host = document.getElementById('langSwitch');
    if (!host) {
      host = document.createElement('div');
      host.id = 'langSwitch';
      document.body.appendChild(host);
    }
    host.innerHTML = '';
    LANGS.forEach(function (lang) {
      var b = document.createElement('button');
      b.type = 'button';
      b.className = 'lang-btn' + (lang === current ? ' active' : '');
      b.textContent = lang.toUpperCase();
      b.setAttribute('lang', lang);
      b.setAttribute('aria-label', lang === 'ru' ? 'Русская версия' : 'English version');
      b.setAttribute('aria-pressed', String(lang === current));
      b.addEventListener('click', function () { setLang(lang); });
      host.appendChild(b);
    });
  }

  function init() {
    var lang = detect();
    // An explicit ?lang= is a deliberate choice (a shared link, or arriving from
    // another page of the site): remember it so it survives navigation between
    // index.html and the simulator. Auto-detected values are left unsaved so
    // detection can still adapt.
    var explicit = new URLSearchParams(location.search).get('lang');
    if (explicit && LANGS.indexOf(explicit) !== -1) {
      safeStorage(function () { return localStorage.setItem(STORAGE_KEY, explicit); }, null);
    }
    apply(lang);
    renderSwitcher(lang);
  }

  /* Runtime lookup for strings assembled in JavaScript (units, status messages,
     scenario names). Falls back to the key itself so a missing entry is visible
     rather than silently blank. */
  function t(key, fallback) {
    var entry = (window.I18N_STRINGS || {})[key];
    if (entry && entry[current] != null) return entry[current];
    return fallback != null ? fallback : key;
  }

  window.i18nT = t;
  window.I18N = {
    detect: detect, apply: apply, setLang: setLang, t: t, langs: LANGS,
    get lang() { return current; }
  };

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
