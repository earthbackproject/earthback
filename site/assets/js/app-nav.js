// ═══════════════════════════════════════════════════════════
// Earthback — Shared App Navigation Component
// Include this on all authenticated/app pages
// (feed, circles, profile, projects, messages, etc.)
//
// Self-contained: injects its own <style> block.
// Pages should NOT define .topbar / .topbar-* CSS.
// ═══════════════════════════════════════════════════════════

(function() {
  var path = window.location.pathname.split('/').pop() || '';

  function isActive(href) {
    if (href === path) return true;
    if (href.includes('#')) return path === href.split('#')[0];
    return false;
  }

  function lc(href, extra) {
    var cls = 'an-link';
    if (extra) cls += ' ' + extra;
    if (isActive(href)) cls += ' active';
    return cls;
  }

  function ac(href) { return isActive(href) ? ' class="active"' : ''; }

  // ── Primary links (always visible, progressively collapse) ──
  var PRIMARY = [
    { href: 'feed.html',       label: 'Home'       },
    { href: 'circles.html',    label: 'Circles'    },
    { href: 'map.html',        label: 'Map'        },
    { href: 'projects.html',   label: 'Projects'   },
    { href: 'visualizer.html', label: 'Visualizer', hide: 'an-hide-md' },
    { href: 'gallery.html',    label: 'Gallery',    hide: 'an-hide-sm' },
  ];

  // ── More dropdown links ──
  var MORE = [
    { href: 'visualizer.html',   label: 'AI Visualizer',     group: 'Tools'     },
    { href: 'designer.html',     label: 'Estimator',         group: 'Tools'     },
    { href: 'gallery.html',      label: 'Gallery',           group: 'Community' },
    { href: 'profile.html#media',label: 'Media',             group: 'Community' },
    { href: 'how-it-works.html', label: 'How It Works',      group: 'Learn'     },
    { href: 'use-cases.html',    label: 'Use Cases',         group: 'Learn'     },
    { href: 'about.html',        label: 'About',             group: 'Learn'     },
    { href: 'training.html',     label: 'Training Partners', group: 'Learn'     },
    { href: 'safety.html',       label: 'Safety & Trust',    group: 'Info'      },
    { href: 'terms.html',        label: 'Terms',             group: 'Info'      },
    { href: 'privacy.html',      label: 'Privacy',           group: 'Info'      },
  ];

  // Build primary link HTML
  var primaryHTML = PRIMARY.map(function(p) {
    return '<a href="' + p.href + '" class="' + lc(p.href, p.hide || '') + '">' + p.label + '</a>';
  }).join('');

  // Build grouped More dropdown
  var groups = {};
  MORE.forEach(function(m) {
    if (!groups[m.group]) groups[m.group] = [];
    groups[m.group].push(m);
  });
  var moreDropHTML = Object.keys(groups).map(function(g) {
    var links = groups[g].map(function(m) {
      return '<a href="' + m.href + '"' + ac(m.href) + '>' + m.label + '</a>';
    }).join('');
    return '<div class="an-more-group"><div class="an-more-group-label">' + g + '</div>' + links + '</div>';
  }).join('');

  // ── NAV HTML ──────────────────────────────────────────────
  var navHTML = '\
<style>\
  /* ── APP NAV — BASE ── */\
  #app-nav * { box-sizing: border-box; }\
  #app-nav nav {\
    position: fixed; top: 0; left: 0; right: 0; z-index: 1000;\
    background: linear-gradient(135deg, var(--green, #1F3A2E) 0%, var(--green2, #2d5a27) 100%);\
    font-family: "Inter", system-ui, sans-serif;\
    box-shadow: 0 2px 8px rgba(0,0,0,0.12);\
  }\
  #app-nav .an-inner {\
    display: flex; align-items: center;\
    padding: 0 1.25rem; height: 56px; gap: 0;\
    max-width: 1400px; margin: 0 auto;\
  }\
\
  /* ── LOGO ── */\
  #app-nav .an-logo {\
    display: flex; align-items: center; gap: 0.4em; flex-shrink: 0;\
    font-family: Georgia, "Times New Roman", serif;\
    font-size: 1.1rem; font-weight: 700; color: #F2EFE6;\
    text-decoration: none; letter-spacing: 0.01em;\
    margin-right: 1.25rem;\
  }\
  #app-nav .an-logo img { width: 1.1em; height: 1.1em; opacity: 0.7; }\
  #app-nav .an-logo .brand-the     { font-size: 0.65em; font-weight: 300; color: rgba(242,239,230,0.45); letter-spacing: 0.02em; margin-right: 0.15em; }\
  #app-nav .an-logo .brand-back    { color: #C2A56C; }\
  #app-nav .an-logo .brand-project { font-size: 0.55em; font-weight: 400; color: rgba(242,239,230,0.28); letter-spacing: 0.08em; margin-left: 0.3em; }\
\
  /* ── LINK ROW ── */\
  #app-nav .an-links {\
    display: flex; align-items: center; gap: 0; flex: 1; min-width: 0;\
  }\
  #app-nav .an-link {\
    font-size: 0.84rem; color: rgba(242,239,230,0.6);\
    text-decoration: none; padding: 6px 11px; border-radius: 5px;\
    white-space: nowrap; transition: color 0.15s, background 0.15s;\
    flex-shrink: 0;\
  }\
  #app-nav .an-link:hover  { color: #F2EFE6; background: rgba(255,255,255,0.07); }\
  #app-nav .an-link.active { color: #F2EFE6; background: rgba(255,255,255,0.09); font-weight: 500; }\
\
  /* Progressive collapse */\
  @media (max-width: 960px)  { #app-nav .an-link.an-hide-md { display: none; } }\
  @media (max-width: 720px)  { #app-nav .an-link.an-hide-sm { display: none; } }\
\
  /* ── MORE BUTTON + DROPDOWN ── */\
  #app-nav .an-more { position: relative; flex-shrink: 0; }\
  #app-nav .an-more-btn {\
    display: flex; align-items: center; gap: 5px;\
    font-size: 0.84rem; color: rgba(242,239,230,0.6);\
    background: none; border: none; cursor: pointer;\
    padding: 6px 11px; border-radius: 5px;\
    font-family: "Inter", system-ui, sans-serif;\
    transition: color 0.15s, background 0.15s;\
    white-space: nowrap;\
  }\
  #app-nav .an-more-btn:hover  { color: #F2EFE6; background: rgba(255,255,255,0.07); }\
  #app-nav .an-more-btn.open   { color: #F2EFE6; background: rgba(255,255,255,0.09); }\
  #app-nav .an-more-btn svg    { transition: transform 0.2s; }\
  #app-nav .an-more-btn.open svg { transform: rotate(180deg); }\
\
  #app-nav .an-more-dropdown {\
    position: absolute; top: calc(100% + 8px); left: 0;\
    background: rgba(10, 20, 14, 0.98);\
    backdrop-filter: blur(16px); -webkit-backdrop-filter: blur(16px);\
    border: 1px solid rgba(255,255,255,0.08);\
    border-radius: 10px; box-shadow: 0 16px 48px rgba(0,0,0,0.5);\
    padding: 1rem; min-width: 540px;\
    display: grid; grid-template-columns: repeat(3, 1fr); gap: 0.25rem 1.5rem;\
    opacity: 0; pointer-events: none; transform: translateY(-6px);\
    transition: opacity 0.17s ease, transform 0.17s ease;\
    z-index: 10;\
  }\
  #app-nav .an-more-dropdown.open {\
    opacity: 1; pointer-events: auto; transform: translateY(0);\
  }\
  @media (max-width: 720px) {\
    #app-nav .an-more-dropdown { left: auto; right: 0; min-width: 260px; grid-template-columns: 1fr; }\
  }\
\
  #app-nav .an-more-group-label {\
    font-size: 0.62rem; font-weight: 700; letter-spacing: 0.14em;\
    text-transform: uppercase; color: #C2A56C;\
    padding: 4px 8px 2px; margin-bottom: 2px;\
  }\
  #app-nav .an-more-group a {\
    display: block; font-size: 0.85rem; color: rgba(242,239,230,0.55);\
    text-decoration: none; padding: 5px 8px; border-radius: 5px;\
    transition: color 0.13s, background 0.13s;\
  }\
  #app-nav .an-more-group a:hover  { color: #F2EFE6; background: rgba(255,255,255,0.06); }\
  #app-nav .an-more-group a.active { color: #C2A56C; font-weight: 500; }\
\
  /* ── RIGHT SIDE (messages + avatar) ── */\
  #app-nav .an-right {\
    display: flex; align-items: center; gap: 8px;\
    margin-left: auto; flex-shrink: 0; padding-left: 0.75rem;\
  }\
  #app-nav .an-msg-link {\
    color: rgba(255,255,255,0.7); font-size: 1rem; text-decoration: none;\
    padding: 4px 8px; border-radius: 8px; transition: all 0.2s;\
    display: flex; align-items: center;\
  }\
  #app-nav .an-msg-link:hover { color: white; background: rgba(255,255,255,0.1); }\
  #app-nav .an-avatar {\
    width: 36px; height: 36px; border-radius: 50%;\
    background: linear-gradient(135deg, var(--green, #1F3A2E), var(--sage, #5a7d52));\
    display: flex; align-items: center; justify-content: center;\
    color: white; font-weight: 700; font-size: 0.85rem;\
    cursor: pointer; text-decoration: none;\
  }\
\
  /* ── EARLY ACCESS BANNER ── */\
  #app-nav .an-banner {\
    background: #1F3A2E; color: rgba(255,255,255,0.85);\
    text-align: center; padding: 7px 16px;\
    font-size: 0.75rem; font-family: "Inter", system-ui, sans-serif;\
    letter-spacing: 0.03em; line-height: 1.4;\
    border-top: 1px solid rgba(255,255,255,0.06);\
  }\
\
  /* ── NAV SPACER (pushes content below fixed nav) ── */\
  #app-nav .an-spacer { height: 87px; }\
\
  /* ── BACKDROP ── */\
  #an-backdrop {\
    position: fixed; inset: 0; z-index: 999;\
    opacity: 0; pointer-events: none; transition: opacity 0.17s;\
  }\
  #an-backdrop.open { opacity: 1; pointer-events: auto; }\
\
  /* ── MOBILE ── */\
  @media (max-width: 600px) {\
    #app-nav .an-links { display: none; }\
    #app-nav .an-hamburger { display: flex !important; }\
    #app-nav .an-logo .brand-project { display: none; }\
  }\
  #app-nav .an-hamburger {\
    display: none; flex-direction: column; gap: 4px;\
    cursor: pointer; padding: 6px; border-radius: 6px;\
    transition: background 0.2s; margin-left: 8px;\
  }\
  #app-nav .an-hamburger:hover { background: rgba(255,255,255,0.1); }\
  #app-nav .an-hamburger span {\
    display: block; width: 20px; height: 2px; background: white;\
    border-radius: 2px; transition: all 0.25s;\
  }\
  #app-nav .an-hamburger.open span:nth-child(1) { transform: rotate(45deg) translate(4px,4px); }\
  #app-nav .an-hamburger.open span:nth-child(2) { opacity: 0; }\
  #app-nav .an-hamburger.open span:nth-child(3) { transform: rotate(-45deg) translate(4px,-4px); }\
  #app-nav .an-mobile-menu {\
    display: none; position: fixed; top: 56px; left: 0; right: 0;\
    background: linear-gradient(135deg, var(--green, #1F3A2E) 0%, var(--green2, #2d5a27) 100%);\
    padding: 8px 16px 14px; box-shadow: 0 4px 12px rgba(0,0,0,0.15);\
    z-index: 999; flex-direction: column; gap: 2px;\
  }\
  #app-nav .an-mobile-menu.open { display: flex; }\
  #app-nav .an-mobile-menu a {\
    color: rgba(255,255,255,0.8); text-decoration: none;\
    font-size: 0.92rem; font-weight: 500; padding: 10px 12px;\
    border-radius: 8px; transition: background 0.2s;\
  }\
  #app-nav .an-mobile-menu a:hover,\
  #app-nav .an-mobile-menu a.active { background: rgba(255,255,255,0.12); color: white; }\
</style>\
\
<nav>\
  <div class="an-inner">\
    <a href="index.html" class="an-logo">\
      <img src="assets/img/icons/icon-leaf.svg" alt="">\
      <span><span class="brand-the">the</span> Earth<span class="brand-back">back</span><span class="brand-project"> Project</span></span>\
    </a>\
\
    <div class="an-links">\
      ' + primaryHTML + '\
      <div class="an-more">\
        <button class="an-more-btn" id="an-more-btn" aria-label="More pages" aria-expanded="false">\
          More\
          <svg width="12" height="12" viewBox="0 0 12 12" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><polyline points="2,4 6,8 10,4"/></svg>\
        </button>\
        <div class="an-more-dropdown" id="an-more-dropdown" role="menu">\
          ' + moreDropHTML + '\
        </div>\
      </div>\
    </div>\
\
    <div class="an-right">\
      <a href="messages.html" title="Messages" class="an-msg-link">\
        <img src="assets/img/icons/icon-chat.svg" alt="Messages" style="width:1.2em;height:1.2em;">\
      </a>\
      <a href="profile.html" title="View your profile" class="an-avatar" id="header-avatar">?</a>\
      <div class="an-hamburger" id="an-hamburger">\
        <span></span><span></span><span></span>\
      </div>\
    </div>\
  </div>\
\
  <div class="an-banner">\
    <span style="font-weight:600;color:#C2A56C;margin-right:6px">EARLY ACCESS</span>\
    <span>Claim your username and get in early &mdash; your voice shapes what gets built.</span>\
    <a href="join.html" style="color:#C2A56C;text-decoration:none;font-weight:600;margin-left:8px">Join free &rarr;</a>\
  </div>\
</nav>\
<div class="an-mobile-menu" id="an-mobile-menu">\
  <a href="feed.html"' + (isActive('feed.html') ? ' class="active"' : '') + '>Home</a>\
  <a href="circles.html"' + (isActive('circles.html') ? ' class="active"' : '') + '>Circles</a>\
  <a href="map.html"' + (isActive('map.html') ? ' class="active"' : '') + '>Map</a>\
  <a href="projects.html"' + (isActive('projects.html') ? ' class="active"' : '') + '>Projects</a>\
  <a href="visualizer.html"' + (isActive('visualizer.html') ? ' class="active"' : '') + '>Visualizer</a>\
  <a href="gallery.html"' + (isActive('gallery.html') ? ' class="active"' : '') + '>Gallery</a>\
  <a href="designer.html"' + (isActive('designer.html') ? ' class="active"' : '') + '>Estimator</a>\
  <a href="messages.html"' + (isActive('messages.html') ? ' class="active"' : '') + '>Messages</a>\
  <a href="profile.html"' + (isActive('profile.html') ? ' class="active"' : '') + '>Profile</a>\
</div>\
<div id="an-backdrop"></div>\
<div class="an-spacer"></div>';

  // ── INJECT ────────────────────────────────────────────────
  var target = document.getElementById('app-nav');
  if (target) target.innerHTML = navHTML;

  // ── MORE DROPDOWN ─────────────────────────────────────────
  function openMore() {
    var btn = document.getElementById('an-more-btn');
    var dd  = document.getElementById('an-more-dropdown');
    var bd  = document.getElementById('an-backdrop');
    if (btn) { btn.classList.add('open'); btn.setAttribute('aria-expanded', 'true'); }
    if (dd)  dd.classList.add('open');
    if (bd)  bd.classList.add('open');
  }

  function closeMore() {
    var btn = document.getElementById('an-more-btn');
    var dd  = document.getElementById('an-more-dropdown');
    var bd  = document.getElementById('an-backdrop');
    if (btn) { btn.classList.remove('open'); btn.setAttribute('aria-expanded', 'false'); }
    if (dd)  dd.classList.remove('open');
    if (bd)  bd.classList.remove('open');
  }

  // ── HAMBURGER TOGGLE ──
  function openMobile() {
    var btn = document.getElementById('an-hamburger');
    var menu = document.getElementById('an-mobile-menu');
    if (btn) btn.classList.add('open');
    if (menu) menu.classList.add('open');
  }

  function closeMobile() {
    var btn = document.getElementById('an-hamburger');
    var menu = document.getElementById('an-mobile-menu');
    if (btn) btn.classList.remove('open');
    if (menu) menu.classList.remove('open');
  }

  document.addEventListener('click', function(e) {
    // More dropdown
    if (e.target.closest('#an-more-btn')) {
      var dd = document.getElementById('an-more-dropdown');
      dd && dd.classList.contains('open') ? closeMore() : openMore();
      return;
    }
    if (e.target.closest('#an-backdrop'))        { closeMore(); return; }
    if (e.target.closest('#an-more-dropdown a')) { closeMore(); return; }

    // Hamburger
    if (e.target.closest('#an-hamburger')) {
      var menu = document.getElementById('an-mobile-menu');
      menu && menu.classList.contains('open') ? closeMobile() : openMobile();
      return;
    }
  });

  document.addEventListener('keydown', function(e) {
    if (e.key === 'Escape') { closeMore(); closeMobile(); }
  });

})();
