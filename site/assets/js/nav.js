// ═══════════════════════════════════════════════════════════
// Earthback — Shared Navigation Component
// Include this on ALL public-facing pages (not app pages).
// Handles: hamburger dropdown, quick links, auth state, page tracking.
// ═══════════════════════════════════════════════════════════

(function() {
  const SUPABASE_URL = 'https://yptktmzagctusbeqdaty.supabase.co';
  const SUPABASE_KEY = 'sb_publishable_zp8dWs1CaN-A5oeR94qRdw_n7jNDhmC';

  const path = window.location.pathname.split('/').pop() || 'index.html';

  function isActive(href) {
    if (href === '/' || href === 'index.html') return path === '' || path === 'index.html';
    return path === href;
  }

  // Active class for dropdown links
  function ac(href) {
    return isActive(href) ? ' class="active"' : '';
  }

  // Class string for right-rail quick links (optional extra classes)
  function qc(href, extra) {
    var cls = 'nav-quick-link';
    if (extra) cls += ' ' + extra;
    if (isActive(href)) cls += ' active';
    return cls;
  }

  // ── NAV HTML ──────────────────────────────────────────────
  const navHTML = `
<style>
  /* ── BASE ── */
  #site-nav * { box-sizing: border-box; }
  #site-nav nav {
    position: fixed; top: 0; left: 0; right: 0; z-index: 1000;
    background: rgba(20, 38, 28, 0.97);
    backdrop-filter: blur(10px); -webkit-backdrop-filter: blur(10px);
    font-family: 'Inter', system-ui, sans-serif;
    overflow: visible;
  }

  /* ── INNER BAR ── */
  #site-nav .nav-inner {
    display: flex; align-items: center; justify-content: space-between;
    padding: 0 1.25rem; height: 56px; max-width: 1400px; margin: 0 auto;
  }

  /* ── LEFT: HAMBURGER + LOGO ── */
  #site-nav .nav-left { display: flex; align-items: center; gap: 0.8rem; }

  #site-nav .nav-menu-btn {
    display: flex; flex-direction: column; justify-content: center;
    gap: 5px; padding: 8px 6px; background: none; border: none; cursor: pointer;
    border-radius: 5px; flex-shrink: 0; transition: background 0.15s;
  }
  #site-nav .nav-menu-btn:hover { background: rgba(255,255,255,0.07); }
  #site-nav .nav-menu-btn span {
    display: block; width: 20px; height: 1.5px;
    background: rgba(242,239,230,0.75);
    transition: transform 0.22s cubic-bezier(.4,0,.2,1), opacity 0.15s, transform 0.22s;
    transform-origin: center;
  }
  #site-nav .nav-menu-btn.open span:nth-child(1) { transform: translateY(6.5px) rotate(45deg); }
  #site-nav .nav-menu-btn.open span:nth-child(2) { opacity: 0; transform: scaleX(0); }
  #site-nav .nav-menu-btn.open span:nth-child(3) { transform: translateY(-6.5px) rotate(-45deg); }

  #site-nav .nav-logo {
    display: flex; align-items: center; gap: 0.4em;
    font-family: Georgia, 'Times New Roman', serif;
    font-size: 1.1rem; font-weight: 700; color: #F2EFE6;
    text-decoration: none; letter-spacing: 0.01em; white-space: nowrap;
  }
  #site-nav .nav-logo img { width: 1.1em; height: 1.1em; opacity: 0.7; flex-shrink: 0; }
  #site-nav .nav-logo .brand-the { font-size: 0.65em; font-weight: 300; color: rgba(242,239,230,0.45); letter-spacing: 0.02em; margin-right: 0.15em; }
  #site-nav .nav-logo .brand-back { color: #C2A56C; }
  #site-nav .nav-logo .brand-project { font-size: 0.55em; font-weight: 400; color: rgba(242,239,230,0.28); letter-spacing: 0.08em; margin-left: 0.3em; }

  /* ── RIGHT: QUICK LINKS + AUTH ── */
  #site-nav .nav-right { display: flex; align-items: center; gap: 0.1rem; }

  #site-nav .nav-quick-link {
    font-size: 0.84rem; color: rgba(242,239,230,0.55);
    text-decoration: none; padding: 5px 11px; border-radius: 5px;
    transition: color 0.15s, background 0.15s; white-space: nowrap;
  }
  #site-nav .nav-quick-link:hover { color: #F2EFE6; background: rgba(255,255,255,0.06); }
  #site-nav .nav-quick-link.active { color: #F2EFE6; background: rgba(255,255,255,0.07); }

  #site-nav #nav-signin-link {
    font-size: 0.84rem; color: rgba(242,239,230,0.45); text-decoration: none;
    padding: 5px 11px; border-radius: 5px; margin-left: 0.35rem;
    transition: color 0.15s;
  }
  #site-nav #nav-signin-link:hover { color: rgba(242,239,230,0.85); }

  #site-nav #nav-join-link {
    font-size: 0.82rem; font-weight: 600; color: #1F3A2E;
    background: #C2A56C; text-decoration: none;
    padding: 6px 15px; border-radius: 20px; margin-left: 0.5rem;
    transition: background 0.15s, transform 0.1s; white-space: nowrap;
  }
  #site-nav #nav-join-link:hover { background: #d4b87e; transform: translateY(-1px); }

  /* Responsive: collapse quick links on small screens */
  @media (max-width: 620px) {
    #site-nav .nav-quick-link { display: none; }
    #site-nav #nav-signin-link { display: none; }
  }
  @media (max-width: 860px) {
    #site-nav .nav-quick-link.hide-sm { display: none; }
  }

  /* ── EARLY ACCESS BANNER ── */
  #site-nav #prelaunch-banner {
    background: linear-gradient(90deg, #1a3026 0%, #243d1e 50%, #1a3026 100%);
    color: rgba(255,255,255,0.85); text-align: center; padding: 5px 16px;
    font-size: 0.7rem; font-family: 'Inter', system-ui, sans-serif;
    letter-spacing: 0.03em; line-height: 1.4;
    border-top: 1px solid rgba(255,255,255,0.06);
  }

  /* ── DROPDOWN PANEL ── */
  #site-nav .nav-dropdown {
    position: absolute; left: 0; right: 0; top: 100%;
    background: rgba(10, 20, 14, 0.98);
    backdrop-filter: blur(16px); -webkit-backdrop-filter: blur(16px);
    border-bottom: 1px solid rgba(255,255,255,0.07);
    box-shadow: 0 20px 60px rgba(0,0,0,0.5);
    opacity: 0; pointer-events: none;
    transform: translateY(-6px);
    transition: opacity 0.18s ease, transform 0.18s ease;
    max-height: calc(100vh - 90px); overflow-y: auto;
  }
  #site-nav .nav-dropdown.open {
    opacity: 1; pointer-events: auto; transform: translateY(0);
  }
  #site-nav .nav-dropdown-inner {
    max-width: 1000px; margin: 0 auto; padding: 2rem 2rem 1.75rem;
  }
  #site-nav .nav-dropdown-grid {
    display: grid; grid-template-columns: repeat(4, 1fr); gap: 2.5rem;
    padding-bottom: 1.5rem; margin-bottom: 1.25rem;
    border-bottom: 1px solid rgba(255,255,255,0.05);
  }
  @media (max-width: 680px) {
    #site-nav .nav-dropdown-grid { grid-template-columns: repeat(2, 1fr); gap: 1.5rem 2rem; }
  }
  #site-nav .nav-dropdown-group h4 {
    margin: 0 0 0.7rem; font-size: 0.64rem; font-weight: 700;
    letter-spacing: 0.15em; text-transform: uppercase; color: #C2A56C;
  }
  #site-nav .nav-dropdown-group a {
    display: block; font-size: 0.87rem; color: rgba(242,239,230,0.5);
    text-decoration: none; padding: 4px 0; line-height: 1.6;
    transition: color 0.13s;
  }
  #site-nav .nav-dropdown-group a:hover { color: #F2EFE6; }
  #site-nav .nav-dropdown-group a.active { color: #C2A56C; font-weight: 500; }
  #site-nav .nav-dropdown-footer {
    display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 0.5rem;
  }
  #site-nav .nav-dropdown-footer .cta-link {
    font-size: 0.84rem; font-weight: 600; color: #C2A56C; text-decoration: none;
    transition: color 0.15s;
  }
  #site-nav .nav-dropdown-footer .cta-link:hover { color: #d4b87e; }
  #site-nav .nav-dropdown-footer .tagline {
    font-family: Georgia, serif; font-style: italic;
    font-size: 0.75rem; color: rgba(242,239,230,0.18);
  }

  /* ── BACKDROP ── */
  #nav-backdrop {
    position: fixed; inset: 0; z-index: 999;
    background: rgba(0,0,0,0.25);
    opacity: 0; pointer-events: none;
    transition: opacity 0.18s;
  }
  #nav-backdrop.open { opacity: 1; pointer-events: auto; }
</style>

<nav>
  <div class="nav-inner">

    <!-- Left: hamburger + logo -->
    <div class="nav-left">
      <button class="nav-menu-btn" id="nav-menu-btn" aria-label="Open site navigation">
        <span></span><span></span><span></span>
      </button>
      <a href="/" class="nav-logo">
        <img src="assets/img/icons/icon-leaf.svg" alt="">
        <span><span class="brand-the">the</span> Earth<span class="brand-back">back</span><span class="brand-project"> Project</span></span>
      </a>
    </div>

    <!-- Right: key quick links + auth -->
    <div class="nav-right">
      <a href="feed.html" class="${qc('feed.html')}">Feed</a>
      <a href="circles.html" class="${qc('circles.html', 'hide-sm')}">Circles</a>
      <a href="map.html" class="${qc('map.html')}">Map</a>
      <a href="login.html" id="nav-signin-link">Sign In</a>
      <a href="join.html" class="nav-join" id="nav-join-link">Join free &rarr;</a>
    </div>

  </div>

  <!-- Early access banner -->
  <div id="prelaunch-banner">
    <span style="font-weight:600;color:#C2A56C;margin-right:6px">EARLY ACCESS</span>
    <span>Claim your username and get in early &mdash; your voice shapes what gets built.</span>
    <a href="join.html" style="color:#C2A56C;text-decoration:none;font-weight:600;margin-left:8px">Join free &rarr;</a>
  </div>

  <!-- Full dropdown: all pages organized by group -->
  <div class="nav-dropdown" id="nav-dropdown">
    <div class="nav-dropdown-inner">
      <div class="nav-dropdown-grid">

        <div class="nav-dropdown-group">
          <h4>Community</h4>
          <a href="feed.html"${ac('feed.html')}>The Feed</a>
          <a href="circles.html"${ac('circles.html')}>Circles</a>
          <a href="map.html"${ac('map.html')}>Map</a>
          <a href="gallery.html"${ac('gallery.html')}>Gallery</a>
        </div>

        <div class="nav-dropdown-group">
          <h4>Tools</h4>
          <a href="visualizer.html"${ac('visualizer.html')}>AI Visualizer</a>
          <a href="designer.html"${ac('designer.html')}>Estimator</a>
        </div>

        <div class="nav-dropdown-group">
          <h4>Learn</h4>
          <a href="how-it-works.html"${ac('how-it-works.html')}>How It Works</a>
          <a href="use-cases.html"${ac('use-cases.html')}>Use Cases</a>
          <a href="about.html"${ac('about.html')}>About</a>
          <a href="training.html"${ac('training.html')}>Training Partners</a>
        </div>

        <div class="nav-dropdown-group">
          <h4>Info</h4>
          <a href="safety.html"${ac('safety.html')}>Safety &amp; Trust</a>
          <a href="terms.html"${ac('terms.html')}>Terms</a>
          <a href="privacy.html"${ac('privacy.html')}>Privacy</a>
          <a href="sitemap.html"${ac('sitemap.html')}>Site Map</a>
        </div>

      </div>
      <div class="nav-dropdown-footer">
        <a href="join.html" class="cta-link">Join the community free &rarr;</a>
        <span class="tagline">The work that matters.</span>
      </div>
    </div>
  </div>

</nav>
<div id="nav-backdrop"></div>`;

  // ── INJECT NAV ──────────────────────────────────────────────
  const navTarget = document.getElementById('site-nav');
  if (navTarget) {
    navTarget.innerHTML = navHTML;
  }

  // ── PAGE VIEW TRACKING (fire-and-forget, completely silent) ──
  (function() {
    try {
      var sid = sessionStorage.getItem('eb_sid');
      if (!sid) {
        sid = Math.random().toString(36).slice(2) + Date.now().toString(36);
        sessionStorage.setItem('eb_sid', sid);
      }
      var pg = location.pathname.split('/').pop() || 'index.html';
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

  // ── DROPDOWN OPEN / CLOSE ──────────────────────────────────
  function openMenu() {
    var btn = document.getElementById('nav-menu-btn');
    var dd  = document.getElementById('nav-dropdown');
    var bd  = document.getElementById('nav-backdrop');
    if (btn) btn.classList.add('open');
    if (dd)  dd.classList.add('open');
    if (bd)  bd.classList.add('open');
    document.body.style.overflow = 'hidden';
  }

  function closeMenu() {
    var btn = document.getElementById('nav-menu-btn');
    var dd  = document.getElementById('nav-dropdown');
    var bd  = document.getElementById('nav-backdrop');
    if (btn) btn.classList.remove('open');
    if (dd)  dd.classList.remove('open');
    if (bd)  bd.classList.remove('open');
    document.body.style.overflow = '';
  }

  document.addEventListener('click', function(e) {
    if (e.target.closest('#nav-menu-btn')) {
      var dd = document.getElementById('nav-dropdown');
      dd && dd.classList.contains('open') ? closeMenu() : openMenu();
      return;
    }
    if (e.target.closest('#nav-backdrop'))    { closeMenu(); return; }
    if (e.target.closest('#nav-dropdown a'))  { closeMenu(); return; }
  });

  document.addEventListener('keydown', function(e) {
    if (e.key === 'Escape') closeMenu();
  });

  // ── NAV SCROLL EFFECT ──────────────────────────────────────
  var navEl = document.querySelector('#site-nav nav');
  if (navEl) {
    window.addEventListener('scroll', function() {
      navEl.style.background = window.scrollY > 40
        ? 'rgba(9, 18, 13, 0.99)'
        : 'rgba(20, 38, 28, 0.97)';
    });
  }

  // ── AUTH STATE ─────────────────────────────────────────────
  function checkAuth() {
    if (typeof supabase === 'undefined') { setTimeout(checkAuth, 100); return; }
    try {
      var sb = supabase.createClient(SUPABASE_URL, SUPABASE_KEY);
      sb.auth.getSession().then(function(result) {
        var session  = result.data.session;
        var link     = document.getElementById('nav-signin-link');
        var joinLink = document.getElementById('nav-join-link');
        if (session) {
          if (link) {
            link.textContent = 'Sign Out';
            link.href = '#';
            link.addEventListener('click', function(e) {
              e.preventDefault();
              sb.auth.signOut().then(function() { window.location.reload(); });
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
