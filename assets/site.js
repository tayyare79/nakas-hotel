(function () {
  // The former JS-only switcher stored a language here on every visit; pages are now per-language URLs.
  try { localStorage.removeItem('nakas_lang'); } catch (e) {}

  var bookMenu = document.getElementById('bookMenu');
  var bookToggle = document.getElementById('bookToggle');
  if (bookToggle && bookMenu) {
    bookToggle.addEventListener('click', function (e) {
      e.stopPropagation();
      var open = bookMenu.classList.toggle('open');
      bookToggle.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
    document.addEventListener('click', function () {
      bookMenu.classList.remove('open');
      bookToggle.setAttribute('aria-expanded', 'false');
    });
  }

  var nav = document.getElementById('nav');
  var bookingBar = document.getElementById('bookingBar');
  function onScroll() {
    var y = window.scrollY;
    nav.classList.toggle('scrolled', y > 60);
    if (bookingBar) bookingBar.classList.toggle('visible', y > window.innerHeight * 0.7);
  }
  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll();

  var animated = document.querySelectorAll('.anim-el');
  if ('IntersectionObserver' in window) {
    var observer = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) { if (e.isIntersecting) e.target.classList.add('visible'); });
    }, { threshold: 0.1 });
    animated.forEach(function (el) { observer.observe(el); });
  } else {
    animated.forEach(function (el) { el.classList.add('visible'); });
  }

  var lightbox = document.getElementById('lightbox');
  var lightboxImg = document.getElementById('lightboxImg');
  function closeLightbox() {
    if (!lightbox) return;
    lightbox.classList.remove('open');
    document.body.style.overflow = '';
  }
  if (lightbox) {
    document.querySelectorAll('a[data-lightbox]').forEach(function (a) {
      a.addEventListener('click', function (e) {
        e.preventDefault();
        var img = a.querySelector('img');
        lightboxImg.src = a.getAttribute('href');
        lightboxImg.alt = img ? img.alt : '';
        lightbox.classList.add('open');
        document.body.style.overflow = 'hidden';
      });
    });
    lightbox.addEventListener('click', closeLightbox);
    lightboxImg.addEventListener('click', function (e) { e.stopPropagation(); });
    document.addEventListener('keydown', function (e) { if (e.key === 'Escape') closeLightbox(); });
  }

  var checkin = document.getElementById('barCheckin');
  var checkout = document.getElementById('barCheckout');
  if (checkin && checkout) {
    var today = new Date();
    var tomorrow = new Date(today); tomorrow.setDate(today.getDate() + 1);
    var nextWeek = new Date(today); nextWeek.setDate(today.getDate() + 7);
    var fmt = function (d) { return d.toISOString().split('T')[0]; };
    checkin.value = fmt(tomorrow);
    checkout.value = fmt(nextWeek);
  }

  if ('serviceWorker' in navigator) {
    window.addEventListener('load', function () { navigator.serviceWorker.register('/sw.js'); });
  }

  // GoatCounter events: PWA install and launches in app mode
  function gcEvent(name) {
    var tries = 0;
    (function attempt() {
      if (window.goatcounter && window.goatcounter.count) {
        window.goatcounter.count({ path: name, title: name, event: true });
      } else if (++tries < 20) {
        setTimeout(attempt, 500);
      }
    })();
  }
  window.addEventListener('appinstalled', function () { gcEvent('pwa-install'); });
  if (window.matchMedia('(display-mode: standalone)').matches || window.navigator.standalone === true) {
    gcEvent('pwa-open');
  }
})();
