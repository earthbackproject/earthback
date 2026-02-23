// ═══════════════════════════════════════════════════════════
// Earthback — Shared Footer Component
// Include on all pages. Inject into <div id="site-footer">
// ═══════════════════════════════════════════════════════════

(function() {
  const footerHTML = `
<footer>
  <a href="index.html" class="footer-logo"><span class="brand-the">the</span> Earth<span class="brand-back">back</span><span class="brand-project"> Project</span></a>
  <ul class="footer-links">
    <li><a href="feed.html">The Feed</a></li>
    <li><a href="circles.html">Circles</a></li>
    <li><a href="visualizer.html">Visualizer</a></li>
    <li><a href="how-it-works.html">How It Works</a></li>
    <li><a href="about.html">About</a></li>
    <li><a href="safety.html">Safety &amp; Trust</a></li>
    <li><a href="terms.html">Terms</a></li>
    <li><a href="privacy.html">Privacy</a></li>
  </ul>
  <div class="footer-copy">&copy; 2026 Earthback. Built by the community, for the community.</div>
</footer>`;

  const target = document.getElementById('site-footer');
  if (target) {
    target.innerHTML = footerHTML;
  }
})();
