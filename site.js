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
