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

/* ── SITE SEARCH ──
   The nav is repeated on every page, so the control is injected here rather
   than hand-added to each one. Index is fetched lazily on first open. */
(function () {
  var nav = document.querySelector('.nav-container');
  if (!nav || document.getElementById('al-search-overlay')) return;

  var LABEL = {book: 'Book', article: 'Article', talk: 'Appearance',
               page: 'Page', section: 'Section'};

  var btn = document.createElement('button');
  btn.className = 'nav-search-btn';
  btn.type = 'button';
  btn.setAttribute('aria-label', 'Search this site');
  btn.title = 'Search';
  btn.innerHTML = '<svg viewBox="0 0 24 24" width="17" height="17" fill="none" ' +
    'stroke="currentColor" stroke-width="1.8" stroke-linecap="round">' +
    '<circle cx="11" cy="11" r="7"></circle>' +
    '<line x1="16.5" y1="16.5" x2="21" y2="21"></line></svg>';
  nav.appendChild(btn);

  var ov = document.createElement('div');
  ov.id = 'al-search-overlay';
  ov.innerHTML =
    '<div class="al-s-panel" role="dialog" aria-modal="true" aria-label="Search">' +
      '<button class="al-s-close" aria-label="Close search">&times;</button>' +
      '<input type="search" class="al-s-input" placeholder="Search books, articles, talks…" ' +
        'autocomplete="off" spellcheck="false">' +
      '<div class="al-s-hint">Searches every book, article, talk and page.</div>' +
      '<div class="al-s-results" aria-live="polite"></div>' +
    '</div>';
  document.body.appendChild(ov);

  var input = ov.querySelector('.al-s-input'),
      out   = ov.querySelector('.al-s-results'),
      hint  = ov.querySelector('.al-s-hint'),
      INDEX = null, loading = null, timer;

  function load() {
    if (INDEX || loading) return loading;
    loading = fetch('/search-index.json').then(function (r) { return r.json(); })
      .then(function (d) { INDEX = d; return d; })
      .catch(function () { INDEX = []; return []; });
    return loading;
  }
  function esc(t) {
    return String(t).replace(/[&<>"]/g, function (c) {
      return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c];
    });
  }
  function snip(text, q) {
    var i = text.toLowerCase().indexOf(q);
    if (i < 0) return esc(text.slice(0, 140)) + '…';
    var a = Math.max(0, i - 55), b = Math.min(text.length, i + q.length + 105);
    if (a > 0) { var sp = text.indexOf(' ', a); if (sp > -1 && sp < i) a = sp + 1; }
    return (a > 0 ? '…' : '') + esc(text.slice(a, i)) + '<mark>' +
      esc(text.slice(i, i + q.length)) + '</mark>' + esc(text.slice(i + q.length, b)) +
      (b < text.length ? '…' : '');
  }
  function render(q) {
    if (!INDEX) { out.innerHTML = '<p class="al-s-empty">Loading…</p>'; return; }
    var hits = [];
    for (var i = 0; i < INDEX.length; i++) {
      var d = INDEX[i],
          inT = d.t.toLowerCase().indexOf(q) > -1,
          at  = d.x.toLowerCase().indexOf(q);
      if (!inT && at < 0) continue;
      hits.push({d: d, inT: inT, at: inT ? -1 : at, main: d.c !== 'section'});
    }
    if (!hits.length) {
      out.innerHTML = '<p class="al-s-empty">Nothing matched &ldquo;' + esc(q) + '&rdquo;.</p>';
      return;
    }
    hits.sort(function (a, b) {
      return (b.inT - a.inT) || (b.main - a.main) || (a.at - b.at);
    });
    out.innerHTML = '<p class="al-s-count">' + hits.length +
      (hits.length === 1 ? ' result' : ' results') + '</p>' +
      hits.slice(0, 80).map(function (h) {
        var ext = /^https?:/i.test(h.d.u);
        return '<a class="al-s-hit" href="' + esc(h.d.u) + '"' +
          (ext ? ' target="_blank" rel="noopener"' : '') + '>' +
          '<span class="al-s-kind">' + esc(LABEL[h.d.c] || h.d.c) + '</span>' +
          '<span class="al-s-title">' + esc(h.d.t) + '</span>' +
          '<span class="al-s-snip">' + snip(h.d.x, q) + '</span></a>';
      }).join('') +
      (hits.length > 80 ? '<p class="al-s-empty">Showing the first 80. Keep typing to narrow.</p>' : '');
  }
  function open() {
    ov.classList.add('open');
    document.body.style.overflow = 'hidden';
    load();
    setTimeout(function () { input.focus(); }, 40);
  }
  function close() {
    ov.classList.remove('open');
    document.body.style.overflow = '';
    input.value = ''; out.innerHTML = ''; hint.style.display = '';
  }

  btn.addEventListener('click', open);
  ov.querySelector('.al-s-close').addEventListener('click', close);
  ov.addEventListener('click', function (e) { if (e.target === ov) close(); });

  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape' && ov.classList.contains('open')) close();
    else if ((e.metaKey || e.ctrlKey) && e.key.toLowerCase() === 'k') { e.preventDefault(); open(); }
    else if (e.key === '/' && !ov.classList.contains('open') &&
             !/^(INPUT|TEXTAREA|SELECT)$/.test(document.activeElement.tagName) &&
             !document.activeElement.isContentEditable) { e.preventDefault(); open(); }
  });

  input.addEventListener('input', function () {
    var q = this.value.trim().toLowerCase();
    clearTimeout(timer);
    hint.style.display = q ? 'none' : '';
    if (!q) { out.innerHTML = ''; return; }
    timer = setTimeout(function () {
      if (INDEX) render(q); else { render(q); load().then(function () { render(q); }); }
    }, 110);
  });

  /* /books#slug opens that book's modal */
  if (/\/books(\.html)?\/?$/.test(location.pathname)) {
    var slug = (location.hash || '').replace(/^#/, '');
    if (slug && typeof window.openBookModal === 'function') {
      setTimeout(function () { window.openBookModal(slug); }, 60);
    }
  }
})();
