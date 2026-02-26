// ═══════════════════════════════════════════════════════════
// Earthback — Shared Navigation Component
// Include this on ALL public-facing pages (not app pages).
// Handles: nav links, mobile menu, auth state, active page.
// ═══════════════════════════════════════════════════════════

(function() {
  const SUPABASE_URL = 'https://yptktmzagctusbeqdaty.supabase.co';
  const SUPABASE_KEY = 'sb_publishable_zp8dWs1CaN-A5oeR94qRdw_n7jNDhmC';

  // Determine current page for active state
  const path = window.location.pathname.split('/').pop() || 'index.html';

  function isActive(href) {
    if (href === '/' || href === 'index.html') return path === '' || path === 'index.html';
    return path === href;
  }

  function activeClass(href) {
    return isActive(href) ? ' class="active"' : '';
  }

  function activeMobileClass(href) {
    return isActive(href) ? ' class="active"' : '';
  }

  // ── NAV HTML (includes pre-launch banner below nav-inner) ──
  const navHTML = `
<nav>
  <div class="nav-inner">
    <a href="/" class="nav-logo"><img src="assets/img/icons/icon-leaf.svg" alt="" style="width:1.1em;height:1.1em;vertical-align:-0.12em;margin-right:0.3em;opacity:0.75;"><span class="brand-the">the</span> Earth<span class="brand-back">back</span><span class="brand-project"> Project</span></a>
    <ul>
      <li><a href="feed.html">The Feed</a></li>
      <li><a href="circles.html">Circles</a></li>
      <li><a href="how-it-works.html">How It Works</a></li>
      <li><a href="use-cases.html">Use Cases</a></li>
      <li><a href="map.html"${isActive('map.html') ? ' class="active"' : ''}>Map</a></li>
      <li><a href="visualizer.html"${isActive('visualizer.html') ? ' class="active"' : ''}>Visualizer</a></li>
      <li><a href="gallery.html"${isActive('gallery.html') ? ' class="active"' : ''}>Gallery</a></li>
      <li><a href="about.html">About</a></li>
      <li><a href="safety.html">Safety</a></li>
      <li><a href="login.html" id="nav-signin-link" style="opacity:0.75;">Sign In</a></li>
      <li><a href="join.html" class="nav-join" id="nav-join-link">Join</a></li>
    </ul>
    <button class="nav-hamburger" id="nav-hamburger" aria-label="Menu">
      <span></span><span></span><span></span>
    </button>
  </div>
  <div id="prelaunch-banner" style="
    background: linear-gradient(90deg, #1a3026 0%, #243d1e 50%, #1a3026 100%);
    color: rgba(255,255,255,0.85);
    text-align: center;
    padding: 5px 16px;
    font-size: 0.7rem;
    font-family: 'Inter', system-ui, sans-serif;
    letter-spacing: 0.03em;
    line-height: 1.4;
    border-top: 1px solid rgba(255,255,255,0.06);
  ">
    <span style="font-weight:600;color:#C2A56C;margin-right:6px">EARLY ACCESS</span>
    <span>You're among the first to explore Earthback. We're building in the open — things may change as we grow.</span>
    <a href="mailto:earthbackproject@gmail.com" style="color:#C2A56C;text-decoration:none;font-weight:600;margin-left:8px">Share feedback &rarr;</a>
  </div>
</nav>
<div class="mobile-nav-overlay" id="mobile-nav-overlay">
  <a href="feed.html">The Feed</a>
  <a href="circles.html">Circles</a>
  <a href="how-it-works.html">How It Works</a>
  <a href="use-cases.html">Use Cases</a>
  <a href="map.html">Map</a>
  <a href="visualizer.html">Visualizer</a>
  <a href="gallery.html">Gallery</a>
  <a href="about.html">About</a>
  <a href="safety.html">Safety</a>
  <a href="join.html" class="join-mobile">Join / Sign In →</a>
</div>`;

  // ── INJECT BANNER + NAV ──
  const navTarget = document.getElementById('site-nav');
  if (navTarget) {
    navTarget.innerHTML = navHTML;
  }

  // ── PAGE VIEW TRACKING (fire-and-forget, completely silent) ──
  (function() {
    try {
      // Session ID: persists across page navigations in the same browser tab session
      var sid = sessionStorage.getItem('eb_sid');
      if (!sid) {
        sid = Math.random().toString(36).slice(2) + Date.now().toString(36);
        sessionStorage.setItem('eb_sid', sid);
      }
      var pg = location.pathname.split('/').pop() || 'index.html';
      // Only log internal referrers (same site page hops)
      var refPg = null;
      if (document.referrer) {
        try {
          var refUrl = new URL(document.referrer);
          if (refUrl.hostname === location.hostname) {
            refPg = refUrl.pathname.split('/').pop() || 'index.html';
          }
        } catch(e) {}
      }
      fetch(SUPABASE_URL + '/rest/v1/page_views', {
        method: 'POST',
        headers: {
          'apikey': SUPABASE_KEY,
          'Authorization': 'Bearer ' + SUPABASE_KEY,
          'Content-Type': 'application/json',
          'Prefer': 'return=minimal'
        },
        body: JSON.stringify({ page: pg, referrer: refPg, session_id: sid })
      });
    } catch(e) { /* tracking never breaks the page */ }
  })();

  // ── HAMBURGER TOGGLE ──
  document.addEventListener('click', function(e) {
    const btn = e.target.closest('#nav-hamburger');
    if (btn) {
      btn.classList.toggle('open');
      document.getElementById('mobile-nav-overlay').classList.toggle('open');
      document.body.style.overflow = document.getElementById('mobile-nav-overlay').classList.contains('open') ? 'hidden' : '';
    }
  });

  // Close mobile nav on link click
  document.addEventListener('click', function(e) {
    const link = e.target.closest('.mobile-nav-overlay a');
    if (link) {
      document.getElementById('nav-hamburger').classList.remove('open');
      document.getElementById('mobile-nav-overlay').classList.remove('open');
      document.body.style.overflow = '';
    }
  });

  // ── NAV SCROLL EFFECT ──
  var navEl = document.querySelector('nav');
  if (navEl) {
    window.addEventListener('scroll', function() {
      navEl.style.background = window.scrollY > 40
        ? 'rgba(9, 18, 13, 0.99)'
        : 'rgba(20, 38, 28, 0.97)';
    });
  }

  // ── AUTH STATE ──
  // Wait for Supabase SDK to load, then check session
  function checkAuth() {
    if (typeof supabase === 'undefined') {
      setTimeout(checkAuth, 100);
      return;
    }
    try {
      var sb = supabase.createClient(SUPABASE_URL, SUPABASE_KEY);
      sb.auth.getSession().then(function(result) {
        var session = result.data.session;
        var link = document.getElementById('nav-signin-link');
        var joinLink = document.getElementById('nav-join-link');
        if (session) {
          if (link) {
            link.textContent = 'Sign Out';
            link.href = '#';
            link.style.opacity = '1';
            link.addEventListener('click', function(e) {
              e.preventDefault();
              sb.auth.signOut().then(function() {
                window.location.reload();
              });
            });
          }
          if (joinLink) {
            joinLink.textContent = 'My Feed';
            joinLink.href = 'feed.html';
          }
        }
      });
    } catch(e) { /* silent fail */ }
  }
  checkAuth();
})();
