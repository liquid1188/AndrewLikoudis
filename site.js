(function(){
  var cta = document.querySelector('.floating-wwm');
  if (!cta) return;
  if (location.pathname.indexOf('work-with-me') !== -1) { cta.style.display = 'none'; return; }
  var targets = document.querySelectorAll('footer, .contact-cta-section, .site-footer');
  if (!targets.length) return;
  var visible = new Set();
  var io = new IntersectionObserver(function(es){
    es.forEach(function(e){ e.isIntersecting ? visible.add(e.target) : visible.delete(e.target); });
    cta.classList.toggle('hidden', visible.size > 0);
  }, { threshold: 0.05 });
  targets.forEach(function(t){ io.observe(t); });
})();

/* ============================================================
   Site search
   Self-contained, no dependencies. Injects its own trigger into
   the nav and its own overlay into <body>, so no page markup
   needs to change. Index is built by build-search-index.py and
   fetched lazily on first use.
   ============================================================ */
(function () {
  'use strict';

  var INDEX_URL = '/search-index.json';
  var KIND_LABEL = { book: 'Book', article: 'Article', talk: 'Appearance', page: 'Page', section: 'Section' };
  var KIND_BOOST = { book: 26, article: 22, talk: 18, page: 14, section: 5 };

  var index = null, loadPromise = null, results = [], active = -1, lastFocus = null;
  var overlay, panel, input, list, status, isOpen = false;

  function esc(s) {
    return String(s).replace(/[&<>"']/g, function (c) {
      return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c];
    });
  }
  function rxEsc(s) { return s.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'); }

  function highlight(text, tokens) {
    var safe = esc(text);
    if (!tokens.length) return safe;
    var rx = new RegExp('(' + tokens.map(rxEsc).join('|') + ')', 'gi');
    return safe.replace(rx, '<mark>$1</mark>');
  }

  /* ---------- index ---------- */
  function loadIndex() {
    if (loadPromise) return loadPromise;
    loadPromise = fetch(INDEX_URL, { credentials: 'same-origin' })
      .then(function (r) { if (!r.ok) throw new Error(r.status); return r.json(); })
      .then(function (d) { index = d.records || []; return index; });
    return loadPromise;
  }

  /* ---------- scoring ---------- */
  function score(rec, tokens, phrase) {
    var t = rec._t || (rec._t = (rec.t || '').toLowerCase());
    var s = rec._s || (rec._s = ((rec.s || '') + ' ' + (rec.m || '') + ' ' + (rec.kw || '')).toLowerCase());
    var b = rec._b || (rec._b = (rec.b || '').toLowerCase());
    var total = 0;

    for (var i = 0; i < tokens.length; i++) {
      var tok = tokens[i], pts = 0;
      if (t.indexOf(tok) === 0) pts = 130;
      else if (new RegExp('\\b' + rxEsc(tok)).test(t)) pts = 95;
      else if (t.indexOf(tok) > -1) pts = 60;
      else if (new RegExp('\\b' + rxEsc(tok)).test(s)) pts = 34;
      else if (s.indexOf(tok) > -1) pts = 24;
      else if (b.indexOf(tok) > -1) pts = 11;
      else return 0;                        // every token must appear somewhere
      total += pts;
    }
    if (phrase.length > 2) {
      if (t.indexOf(phrase) > -1) total += 70;
      else if (s.indexOf(phrase) > -1) total += 25;
    }
    total += KIND_BOOST[rec.k] || 0;
    if (rec.t.length < 46) total += 6;       // prefer tight, specific titles
    return total;
  }

  function search(q) {
    var phrase = q.trim().toLowerCase();
    var tokens = phrase.split(/\s+/).filter(Boolean);
    if (!tokens.length || !index) return [];
    var out = [];
    for (var i = 0; i < index.length; i++) {
      var sc = score(index[i], tokens, phrase);
      if (sc > 0) out.push({ r: index[i], sc: sc, tokens: tokens });
    }
    out.sort(function (a, b) { return b.sc - a.sc || a.r.t.length - b.r.t.length; });
    return out.slice(0, 24);
  }

  /* pick the most useful snippet: the stored one, or a window around a body hit */
  function snippetFor(rec, tokens) {
    if (rec.s) {
      for (var i = 0; i < tokens.length; i++) {
        if (rec.s.toLowerCase().indexOf(tokens[i]) > -1) return rec.s;
      }
    }
    var body = rec.b || '';
    var low = body.toLowerCase(), at = -1;
    for (var j = 0; j < tokens.length && at < 0; j++) at = low.indexOf(tokens[j]);
    if (at > -1) {
      var start = Math.max(0, at - 60);
      return (start > 0 ? '… ' : '') + body.slice(start, start + 190).trim() + '…';
    }
    return rec.s || body.slice(0, 160);
  }

  /* ---------- rendering ---------- */
  function render(q) {
    if (!q.trim()) {
      list.innerHTML = '';
      status.textContent = index
        ? 'Search books, articles, talks and pages.'
        : 'Loading…';
      status.style.display = 'block';
      results = []; active = -1;
      return;
    }
    results = search(q);
    active = results.length ? 0 : -1;

    if (!results.length) {
      list.innerHTML = '';
      status.textContent = 'No matches for “' + q.trim() + '”.';
      status.style.display = 'block';
      return;
    }
    status.style.display = 'none';

    list.innerHTML = results.map(function (hit, i) {
      var r = hit.r, ext = /^https?:/i.test(r.u);
      return '<a class="ss-item' + (i === 0 ? ' active' : '') + '" role="option" id="ss-opt-' + i +
        '" aria-selected="' + (i === 0) + '" href="' + esc(r.u) + '"' +
        (ext ? ' target="_blank" rel="noopener"' : '') + ' data-i="' + i + '">' +
        '<span class="ss-item-main">' +
        '<span class="ss-title">' + highlight(r.t, hit.tokens) + '</span>' +
        '<span class="ss-snippet">' + highlight(snippetFor(r, hit.tokens), hit.tokens) + '</span>' +
        (r.m ? '<span class="ss-meta">' + esc(r.m) + '</span>' : '') +
        '</span>' +
        (ext ? '<span class="ss-ext" aria-hidden="true">↗</span>' : '') +
        '<span class="ss-kind">' + (KIND_LABEL[r.k] || r.k) + '</span>' +
        '</a>';
    }).join('');

    Array.prototype.forEach.call(list.querySelectorAll('.ss-item'), function (el) {
      el.addEventListener('mousemove', function () { setActive(+el.dataset.i); });
      el.addEventListener('click', function (e) { choose(+el.dataset.i, e); });
    });
  }

  function setActive(i) {
    var items = list.querySelectorAll('.ss-item');
    if (!items.length) return;
    active = Math.max(0, Math.min(i, items.length - 1));
    Array.prototype.forEach.call(items, function (el, n) {
      el.classList.toggle('active', n === active);
      el.setAttribute('aria-selected', n === active);
    });
    input.setAttribute('aria-activedescendant', 'ss-opt-' + active);
    items[active].scrollIntoView({ block: 'nearest' });
  }

  function choose(i, e) {
    var hit = results[i];
    if (!hit) return;
    var u = hit.r.u;
    if (typeof gtag === 'function') {
      try { gtag('event', 'search', { search_term: input.value.trim() }); } catch (err) {}
    }
    if (/^https?:/i.test(u)) return;                     // let the browser open it
    var m = u.match(/^\/books#(.+)$/);
    if (m) {
      if (e) e.preventDefault();
      close();
      if (/\/books(\.html)?\/?$/.test(location.pathname) && typeof window.openBookModal === 'function') {
        window.openBookModal(m[1]);
        history.replaceState && history.replaceState(null, '', u);
      } else {
        location.href = u;
      }
    }
  }

  /* ---------- open / close ---------- */
  function open() {
    if (isOpen) return;
    isOpen = true;
    lastFocus = document.activeElement;
    overlay.classList.add('open');
    document.body.style.overflow = 'hidden';
    input.value = '';
    render('');
    input.focus();
    loadIndex().then(function () { render(input.value); })
      .catch(function () { status.textContent = 'Search is unavailable right now.'; });
  }

  function close() {
    if (!isOpen) return;
    isOpen = false;
    overlay.classList.remove('open');
    document.body.style.overflow = '';
    if (lastFocus && lastFocus.focus) lastFocus.focus();
  }

  /* ---------- build UI ---------- */
  function build() {
    var nav = document.querySelector('.nav-container');
    if (!nav || document.querySelector('.site-search-btn')) return;

    var icon = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" ' +
      'stroke-linecap="round" aria-hidden="true"><circle cx="11" cy="11" r="7"/><path d="m20 20-3.5-3.5"/></svg>';

    var btn = document.createElement('button');
    btn.type = 'button';
    btn.className = 'site-search-btn';
    btn.setAttribute('aria-label', 'Search this site');
    btn.innerHTML = icon + '<span class="ss-label">Search</span>' +
      '<span class="ss-kbd">' + (/Mac|iPhone|iPad/.test(navigator.platform) ? '⌘K' : 'Ctrl K') + '</span>';
    // Append last; CSS `order` places it after the links and before the
    // hamburger on every breakpoint.
    nav.appendChild(btn);
    btn.addEventListener('click', open);

    overlay = document.createElement('div');
    overlay.className = 'ss-overlay';
    overlay.innerHTML =
      '<div class="ss-panel" role="dialog" aria-modal="true" aria-label="Site search">' +
        '<div class="ss-inputwrap">' + icon +
          '<input class="ss-input" type="search" autocomplete="off" spellcheck="false" ' +
            'placeholder="Search books, articles, talks…" aria-label="Search this site" ' +
            'role="combobox" aria-expanded="true" aria-controls="ss-list" aria-autocomplete="list">' +
          '<button class="ss-close" type="button">Esc</button>' +
        '</div>' +
        '<div class="ss-status" role="status"></div>' +
        '<div class="ss-results" id="ss-list" role="listbox" aria-label="Search results"></div>' +
        '<div class="ss-foot"><span>↑ ↓ to navigate</span><span>↵ to open</span><span>Esc to close</span></div>' +
      '</div>';
    document.body.appendChild(overlay);

    panel = overlay.querySelector('.ss-panel');
    input = overlay.querySelector('.ss-input');
    list = overlay.querySelector('.ss-results');
    status = overlay.querySelector('.ss-status');

    overlay.querySelector('.ss-close').addEventListener('click', close);
    overlay.addEventListener('mousedown', function (e) { if (e.target === overlay) close(); });

    var timer;
    input.addEventListener('input', function () {
      clearTimeout(timer);
      var v = input.value;
      timer = setTimeout(function () { render(v); }, 90);
    });

    input.addEventListener('keydown', function (e) {
      if (e.key === 'ArrowDown') { e.preventDefault(); setActive(active + 1); }
      else if (e.key === 'ArrowUp') { e.preventDefault(); setActive(active - 1); }
      else if (e.key === 'Enter') {
        var el = list.querySelectorAll('.ss-item')[active];
        if (el) { e.preventDefault(); el.click(); if (el.target !== '_blank') close(); }
      }
    });

    document.addEventListener('keydown', function (e) {
      if (isOpen && e.key === 'Escape') { e.preventDefault(); close(); return; }
      if (isOpen && e.key === 'Tab') {                       // keep focus inside
        e.preventDefault();
        input.focus();
        return;
      }
      if ((e.metaKey || e.ctrlKey) && e.key.toLowerCase() === 'k') { e.preventDefault(); open(); return; }
      var tag = (e.target.tagName || '').toLowerCase();
      if (e.key === '/' && !isOpen && tag !== 'input' && tag !== 'textarea' && !e.target.isContentEditable) {
        e.preventDefault(); open();
      }
    });
  }

  /* deep link: /books#slug opens that book's modal */
  function openBookFromHash() {
    if (!/\/books(\.html)?\/?$/.test(location.pathname)) return;
    var slug = (location.hash || '').replace(/^#/, '');
    if (slug && typeof window.openBookModal === 'function') {
      setTimeout(function () { window.openBookModal(slug); }, 60);
    }
  }

  function init() { build(); openBookFromHash(); }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else { init(); }
})();
