// ═══════════════════════════════════════════════════════════
// Earthback — Shared App Navigation Component
// Include this on all authenticated/app pages
// (feed, circles, profile, projects, messages, etc.)
// ═══════════════════════════════════════════════════════════

(function() {
  const path = window.location.pathname.split('/').pop() || '';

  function isActive(href) {
    if (href === path) return true;
    // Handle hash-based active states
    if (href.includes('#')) return path === href.split('#')[0];
    return false;
  }

  function ac(href) { return isActive(href) ? ' active' : ''; }

  const navHTML = `
<nav class="topbar">
  <a class="topbar-brand" href="index.html">
    <span class="topbar-brand-mark">🌿</span>
    <span class="topbar-brand-name"><span class="topbar-the">the</span> Earthback <span class="brand-sub">Project</span></span>
  </a>
  <div class="topbar-nav">
    <a href="feed.html" class="topbar-nav-link${ac('feed.html')}">Home</a>
    <a href="projects.html" class="topbar-nav-link${ac('projects.html')}">Projects</a>
    <a href="visualizer.html" class="topbar-nav-link${ac('visualizer.html')}">Visualizer</a>
    <a href="profile.html#media" class="topbar-nav-link${ac('profile.html')}">Media</a>
    <a href="circles.html" class="topbar-nav-link${ac('circles.html')}">Circles</a>
  </div>
  <div class="topbar-right">
    <a href="messages.html" title="Messages" style="color:rgba(255,255,255,0.7);font-size:1rem;text-decoration:none;padding:4px 8px;border-radius:8px;transition:all 0.2s" onmouseover="this.style.color='white';this.style.background='rgba(255,255,255,0.1)'" onmouseout="this.style.color='rgba(255,255,255,0.7)';this.style.background='none'">💬</a>
    <a href="profile.html" title="View your profile" style="width:36px;height:36px;border-radius:50%;background:linear-gradient(135deg,var(--green),var(--sage));display:flex;align-items:center;justify-content:center;color:white;font-weight:700;font-size:0.85rem;cursor:pointer;text-decoration:none;" id="header-avatar">?</a>
    <div class="topbar-hamburger" id="app-hamburger">
      <span></span><span></span><span></span>
    </div>
  </div>
</nav>
<div class="topbar-mobile-menu" id="app-mobile-menu">
  <a href="feed.html"${ac('feed.html') ? ' class="active"' : ''}>Home</a>
  <a href="projects.html"${ac('projects.html') ? ' class="active"' : ''}>Projects</a>
  <a href="visualizer.html"${ac('visualizer.html') ? ' class="active"' : ''}>Visualizer</a>
  <a href="profile.html#media"${ac('profile.html') ? ' class="active"' : ''}>Media</a>
  <a href="circles.html"${ac('circles.html') ? ' class="active"' : ''}>Circles</a>
  <a href="messages.html">Messages</a>
</div>`;

  const target = document.getElementById('app-nav');
  if (target) {
    target.innerHTML = navHTML;
  }

  // ── HAMBURGER TOGGLE ──
  document.addEventListener('click', function(e) {
    var btn = e.target.closest('#app-hamburger');
    if (btn) {
      btn.classList.toggle('open');
      document.getElementById('app-mobile-menu').classList.toggle('open');
    }
  });
})();
