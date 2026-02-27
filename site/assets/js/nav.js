// ═══════════════════════════════════════════════════════════
// Earthback — Shared Navigation Component
// Include this on ALL public-facing pages (not app pages).
// Handles: visible link row, More dropdown, auth state, page tracking.
// ═══════════════════════════════════════════════════════════

(function() {
  const SUPABASE_URL = 'https://yptktmzagctusbeqdaty.supabase.co';
  const SUPABASE_KEY = 'sb_publishable_zp8dWs1CaN-A5oeR94qRdw_n7jNDhmC';

  const path = window.location.pathname.split('/').pop() || 'index.html';

  function isActive(href) {
    if (href === '/' || href === 'index.html') return path === '' || path === 'index.html';
    return path === href;
  }

  function lc(href, extra) {
    var cls = 'nav-link';
    if (extra) cls += ' ' + extra;
    if (isActive(href)) cls += ' active';
    return cls;
  }

  function ac(href) { return isActive(href) ? ' class="active"' : ''; }

  // ── Primary links (always visible, progressively collapse on smaller screens)
  // hide-md = hidden below ~960px, hide-sm = hidden below ~720px
  const PRIMARY = [
    { href: 'feed.html',       label: 'The Feed'   },
    { href: 'circles.html',    label: 'Circles'    },
    { href: 'map.html',        label: 'Map'        },
    { href: 'visualizer.html', label: 'Visualizer', hide: 'hide-md' },
    { href: 'designer.html',   label: 'Estimator',  hide: 'hide-md' },
    { href: 'gallery.html',    label: 'Gallery',    hide: 'hide-sm' },
  ];

  // ── More dropdown links (everything not in the primary row)
  const MORE = [
    { href: 'visualizer.html', label: 'AI Visualizer',    group: 'Tools'     },
    { href: 'designer.html',   label: 'Estimator',        group: 'Tools'     },
    { href: 'gallery.html',    label: 'Gallery',          group: 'Community' },
    { href: 'how-it-works.html', label: 'How It Works',   group: 'Learn'     },
    { href: 'use-cases.html',  label: 'Use Cases',        group: 'Learn'     },
    { href: 'about.html',      label: 'About',            group: 'Learn'     },
    { href: 'training.html',   label: 'Training Partners',group: 'Learn'     },
    { href: 'safety.html',     label: 'Safety & Trust',   group: 'Info'      },
    { href: 'terms.html',      label: 'Terms',            group: 'Info'      },
    { href: 'privacy.html',    label: 'Privacy',          group: 'Info'      },
    { href: 'sitemap.html',    label: 'Site Map',         group: 'Info'      },
  ];

  // Build primary link HTML
  const primaryHTML = PRIMARY.map(function(p) {
    return `<a href="${p.href}" class="${lc(p.href, p.hide || '')}">${p.label}</a>`;
  }).join('');

  // Build More dropdown — group the links
  var groups = {};
  MORE.forEach(function(m) {
    if (!groups[m.group]) groups[m.group] = [];
    groups[m.group].push(m);
  });
  const moreDropHTML = Object.keys(groups).map(function(g) {
    var links = groups[g].map(function(m) {
      return `<a href="${m.href}"${ac(m.href)}>${m.label}</a>`;
    }).join('');
    return `<div class="more-group"><div class="more-group-label">${g}</div>${links}</div>`;
  }).join('');

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
  }

  /* ── INNER BAR ── */
  #site-nav .nav-inner {
    display: flex; align-items: center;
    padding: 0 1.25rem; height: 56px; gap: 0;
    max-width: 1400px; margin: 0 auto;
  }

  /* ── LOGO ── */
  #site-nav .nav-logo {
    display: flex; align-items: center; gap: 0.4em; flex-shrink: 0;
    font-family: Georgia, 'Times New Roman', serif;
    font-size: 1.1rem; font-weight: 700; color: #F2EFE6;
    text-decoration: none; letter-spacing: 0.01em;
    margin-right: 1.25rem;
  }
  #site-nav .nav-logo img { width: 1.1em; height: 1.1em; opacity: 0.7; }
  #site-nav .nav-logo .brand-the    { font-size: 0.65em; font-weight: 300; color: rgba(242,239,230,0.45); letter-spacing: 0.02em; margin-right: 0.15em; }
  #site-nav .nav-logo .brand-back   { color: #C2A56C; }
  #site-nav .nav-logo .brand-project{ font-size: 0.55em; font-weight: 400; color: rgba(242,239,230,0.28); letter-spacing: 0.08em; margin-left: 0.3em; }

  /* ── LINK ROW ── */
  #site-nav .nav-links {
    display: flex; align-items: center; gap: 0; flex: 1; min-width: 0;
  }

  #site-nav .nav-link {
    font-size: 0.84rem; color: rgba(242,239,230,0.6);
    text-decoration: none; padding: 6px 11px; border-radius: 5px;
    white-space: nowrap; transition: color 0.15s, background 0.15s;
    flex-shrink: 0;
  }
  #site-nav .nav-link:hover  { color: #F2EFE6; background: rgba(255,255,255,0.07); }
  #site-nav .nav-link.active { color: #F2EFE6; background: rgba(255,255,255,0.09); font-weight: 500; }

  /* Progressive collapse */
  @media (max-width: 960px)  { #site-nav .nav-link.hide-md { display: none; } }
  @media (max-width: 720px)  { #site-nav .nav-link.hide-sm { display: none; } }

  /* ── MORE BUTTON + DROPDOWN ── */
  #site-nav .nav-more { position: relative; flex-shrink: 0; }

  #site-nav .nav-more-btn {
    display: flex; align-items: center; gap: 5px;
    font-size: 0.84rem; color: rgba(242,239,230,0.6);
    background: none; border: none; cursor: pointer;
    padding: 6px 11px; border-radius: 5px;
    font-family: 'Inter', system-ui, sans-serif;
    transition: color 0.15s, background 0.15s;
    white-space: nowrap;
  }
  #site-nav .nav-more-btn:hover  { color: #F2EFE6; background: rgba(255,255,255,0.07); }
  #site-nav .nav-more-btn.open   { color: #F2EFE6; background: rgba(255,255,255,0.09); }
  #site-nav .nav-more-btn svg    { transition: transform 0.2s; }
  #site-nav .nav-more-btn.open svg { transform: rotate(180deg); }

  #site-nav .nav-more-dropdown {
    position: absolute; top: calc(100% + 8px); left: 0;
    background: rgba(10, 20, 14, 0.98);
    backdrop-filter: blur(16px); -webkit-backdrop-filter: blur(16px);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 10px; box-shadow: 0 16px 48px rgba(0,0,0,0.5);
    padding: 1rem; min-width: 580px;
    display: grid; grid-template-columns: repeat(3, 1fr); gap: 0.25rem 1.5rem;
    opacity: 0; pointer-events: none; transform: translateY(-6px);
    transition: opacity 0.17s ease, transform 0.17s ease;
    z-index: 10;
  }
  #site-nav .nav-more-dropdown.open {
    opacity: 1; pointer-events: auto; transform: translateY(0);
  }
  /* On narrow screens, dropdown goes right-aligned and narrower */
  @media (max-width: 720px) {
    #site-nav .nav-more-dropdown { left: auto; right: 0; min-width: 260px; grid-template-columns: 1fr; }
  }

  #site-nav .more-group { }
  #site-nav .more-group-label {
    font-size: 0.62rem; font-weight: 700; letter-spacing: 0.14em;
    text-transform: uppercase; color: #C2A56C;
    padding: 4px 8px 2px; margin-bottom: 2px;
  }
  #site-nav .more-group a {
    display: block; font-size: 0.85rem; color: rgba(242,239,230,0.55);
    text-decoration: none; padding: 5px 8px; border-radius: 5px;
    transition: color 0.13s, background 0.13s;
  }
  #site-nav .more-group a:hover  { color: #F2EFE6; background: rgba(255,255,255,0.06); }
  #site-nav .more-group a.active { color: #C2A56C; font-weight: 500; }

  /* ── AUTH ── */
  #site-nav .nav-auth {
    display: flex; align-items: center; gap: 0.25rem;
    margin-left: auto; flex-shrink: 0; padding-left: 0.75rem;
  }
  #site-nav #nav-signin-link {
    font-size: 0.84rem; color: rgba(242,239,230,0.45);
    text-decoration: none; padding: 5px 11px; border-radius: 5px;
    transition: color 0.15s; white-space: nowrap;
  }
  #site-nav #nav-signin-link:hover { color: rgba(242,239,230,0.85); }

  #site-nav #nav-join-link {
    font-size: 0.82rem; font-weight: 600; color: #1F3A2E;
    background: #C2A56C; text-decoration: none;
    padding: 6px 15px; border-radius: 20px; margin-left: 0.35rem;
    transition: background 0.15s, transform 0.1s; white-space: nowrap;
  }
  #site-nav #nav-join-link:hover { background: #d4b87e; transform: translateY(-1px); }

  @media (max-width: 480px) {
    #site-nav #nav-signin-link { display: none; }
    #site-nav .nav-logo .brand-project { display: none; }
  }

  /* ── EARLY ACCESS BANNER ── */
  #site-nav #prelaunch-banner {
    background: linear-gradient(90deg, #1a3026 0%, #243d1e 50%, #1a3026 100%);
    color: rgba(255,255,255,0.85); text-align: center; padding: 5px 16px;
    font-size: 0.7rem; font-family: 'Inter', system-ui, sans-serif;
    letter-spacing: 0.03em; line-height: 1.4;
    border-top: 1px solid rgba(255,255,255,0.06);
  }

  /* ── BACKDROP ── */
  #nav-backdrop {
    position: fixed; inset: 0; z-index: 999;
    opacity: 0; pointer-events: none; transition: opacity 0.17s;
  }
  #nav-backdrop.open { opacity: 1; pointer-events: auto; }
</style>

<nav>
  <div class="nav-inner">

    <a href="/" class="nav-logo">
      <img src="assets/img/icons/icon-leaf.svg" alt="">
      <span><span class="brand-the">the</span> Earth<span class="brand-back">back</span><span class="brand-project"> Project</span></span>
    </a>

    <div class="nav-links">
      ${primaryHTML}
      <div class="nav-more">
        <button class="nav-more-btn" id="nav-more-btn" aria-label="More pages" aria-expanded="false">
          More
          <svg width="12" height="12" viewBox="0 0 12 12" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round">
            <polyline points="2,4 6,8 10,4"/>
          </svg>
        </button>
        <div class="nav-more-dropdown" id="nav-more-dropdown" role="menu">
          ${moreDropHTML}
        </div>
      </div>
    </div>

    <div class="nav-auth">
      <a href="login.html" id="nav-signin-link">Sign In</a>
      <a href="join.html" class="nav-join" id="nav-join-link">Join free &rarr;</a>
    </div>

  </div>

  <div id="prelaunch-banner">
    <span style="font-weight:600;color:#C2A56C;margin-right:6px">EARLY ACCESS</span>
    <span>Claim your username and get in early &mdash; your voice shapes what gets built.</span>
    <a href="join.html" style="color:#C2A56C;text-decoration:none;font-weight:600;margin-left:8px">Join free &rarr;</a>
  </div>
</nav>
<div id="nav-backdrop"></div>`;

  // ── INJECT ────────────────────────────────────────────────
  const navTarget = document.getElementById('site-nav');
  if (navTarget) navTarget.innerHTML = navHTML;

  // ── PAGE VIEW TRACKING ────────────────────────────────────
  // Tries to include member user_id if logged in; fires without it for anon visitors.
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
          if (refUrl.hostname === location.hostname) refPg = refUrl.pathname.split('/').pop() || 'index.html';
        } catch(e) {}
      }
      function firePageView(userId) {
        var payload = { p_page: pg, p_referrer: refPg, p_session_id: sid };
        if (userId) payload.p_user_id = userId;
        fetch(SUPABASE_URL + '/rest/v1/rpc/insert_page_view', {
          method: 'POST',
          headers: {
            'apikey': SUPABASE_KEY, 'Authorization': 'Bearer ' + SUPABASE_KEY,
            'Content-Type': 'application/json', 'Prefer': 'return=minimal'
          },
          body: JSON.stringify(payload)
        });
      }
      // Try to get auth session for member tracking; timeout after 200ms for anon visitors
      if (typeof supabase !== 'undefined') {
        var sb = supabase.createClient(SUPABASE_URL, SUPABASE_KEY);
        var fired = false;
        sb.auth.getSession().then(function(result) {
          if (!fired) {
            fired = true;
            var uid = result.data.session ? result.data.session.user.id : null;
            firePageView(uid);
          }
        });
        setTimeout(function() { if (!fired) { fired = true; firePageView(null); } }, 200);
      } else {
        firePageView(null);
      }
    } catch(e) {}
  })();

  // ── MORE DROPDOWN ─────────────────────────────────────────
  function openMore() {
    var btn = document.getElementById('nav-more-btn');
    var dd  = document.getElementById('nav-more-dropdown');
    var bd  = document.getElementById('nav-backdrop');
    if (btn) { btn.classList.add('open'); btn.setAttribute('aria-expanded', 'true'); }
    if (dd)  dd.classList.add('open');
    if (bd)  bd.classList.add('open');
  }

  function closeMore() {
    var btn = document.getElementById('nav-more-btn');
    var dd  = document.getElementById('nav-more-dropdown');
    var bd  = document.getElementById('nav-backdrop');
    if (btn) { btn.classList.remove('open'); btn.setAttribute('aria-expanded', 'false'); }
    if (dd)  dd.classList.remove('open');
    if (bd)  bd.classList.remove('open');
  }

  document.addEventListener('click', function(e) {
    if (e.target.closest('#nav-more-btn')) {
      var dd = document.getElementById('nav-more-dropdown');
      dd && dd.classList.contains('open') ? closeMore() : openMore();
      return;
    }
    if (e.target.closest('#nav-backdrop'))         { closeMore(); return; }
    if (e.target.closest('#nav-more-dropdown a'))  { closeMore(); return; }
  });

  document.addEventListener('keydown', function(e) {
    if (e.key === 'Escape') closeMore();
  });

  // ── NAV SCROLL EFFECT ─────────────────────────────────────
  var navEl = document.querySelector('#site-nav nav');
  if (navEl) {
    window.addEventListener('scroll', function() {
      navEl.style.background = window.scrollY > 40
        ? 'rgba(9, 18, 13, 0.99)'
        : 'rgba(20, 38, 28, 0.97)';
    });
  }

  // ── AUTH STATE ────────────────────────────────────────────
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
          if (joinLink) { joinLink.textContent = 'My Feed'; joinLink.href = 'feed.html'; }
        }
      });
    } catch(e) {}
  }
  checkAuth();

})();
