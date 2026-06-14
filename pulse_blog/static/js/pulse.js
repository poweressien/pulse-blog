/* PULSE Blog — interactive layer */
(function () {
  'use strict';

  var ACCENTS = { nigeria: '#00D97E', africa: '#F5C518', world: '#FF5533' };

  /* ── TABS */
  function initTabs() {
    var tabs   = document.querySelectorAll('.pulse-tab');
    var panels = document.querySelectorAll('.pulse-tab-panel');
    if (!tabs.length) return;

    tabs.forEach(function (tab) {
      tab.addEventListener('click', function () {
        var target = this.dataset.tab;

        tabs.forEach(function (t) { t.classList.remove('active'); });
        panels.forEach(function (p) { p.classList.remove('active'); });
        this.classList.add('active');

        var panel = document.querySelector('[data-panel="' + target + '"]');
        if (panel) panel.classList.add('active');

        // Update CSS accent variable
        var accent = ACCENTS[target] || '#00D97E';
        document.documentElement.style.setProperty('--accent', accent);
        document.documentElement.style.setProperty('--accent-glow', accent + '18');

        // Sync ticker + logo tagline colour
        var ticker = document.getElementById('pulseTicker');
        var badge  = ticker && ticker.querySelector('.pulse-ticker__badge');
        var tagline = document.querySelector('.pulse-logo__tagline');
        if (ticker)  ticker.style.background = accent;
        if (badge)   badge.style.color = accent;
        if (tagline) tagline.style.color = accent;
      });
    });
  }

  /* ── BREAKING TICKER */
  function initTicker() {
    var items = document.querySelectorAll('.pulse-ticker__item');
    var dots  = document.querySelectorAll('.pulse-ticker__dot');
    if (!items.length) return;

    var idx = 0;

    function show(i) {
      items.forEach(function (el) { el.classList.remove('active'); });
      dots.forEach(function (el)  { el.classList.remove('active'); });
      items[i].classList.add('active');
      if (dots[i]) dots[i].classList.add('active');
    }

    show(0);
    var timer = setInterval(function () {
      idx = (idx + 1) % items.length;
      show(idx);
    }, 4000);

    dots.forEach(function (dot, i) {
      dot.addEventListener('click', function () {
        clearInterval(timer);
        idx = i;
        show(idx);
      });
    });
  }

  /* ── NEWSLETTER AJAX */
  function initNewsletter() {
    document.querySelectorAll('.pulse-newsletter-form').forEach(function (form) {
      form.addEventListener('submit', function (e) {
        e.preventDefault();
        var input = this.querySelector('input[type="email"]');
        var btn   = this.querySelector('button[type="submit"]');
        var email = input.value.trim();
        if (!email) return;

        btn.textContent = 'SUBSCRIBING...';
        btn.disabled = true;

        fetch(this.action || '/newsletter/', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-CSRFToken': getCookie('csrftoken'),
            'X-Requested-With': 'XMLHttpRequest',
          },
          body: 'email=' + encodeURIComponent(email),
        })
        .then(function (r) { return r.json(); })
        .then(function (data) {
          if (data.success) {
            form.innerHTML = '<p class="pulse-success">Subscribed! Check your inbox.</p>';
          } else {
            btn.textContent = 'SUBSCRIBE FREE';
            btn.disabled = false;
          }
        })
        .catch(function () {
          btn.textContent = 'SUBSCRIBE FREE';
          btn.disabled = false;
        });
      });
    });
  }

  /* ── UTILITY */
  function getCookie(name) {
    var v = '; ' + document.cookie;
    var parts = v.split('; ' + name + '=');
    if (parts.length === 2) return parts.pop().split(';').shift();
    return '';
  }

  /* ── INIT */
  document.addEventListener('DOMContentLoaded', function () {
    initTabs();
    initTicker();
    initNewsletter();
  });
}());
