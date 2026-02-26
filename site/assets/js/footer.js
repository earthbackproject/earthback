// ═══════════════════════════════════════════════════════════
// Earthback — Shared Footer Component
// Include on all pages. Inject into <div id="site-footer">
// ═══════════════════════════════════════════════════════════

(function() {
  const footerHTML = `
<footer style="background:#171c19; padding:4.5rem 2rem 2.25rem; font-family:'Inter',system-ui,sans-serif;">
  <div style="max-width:1200px; margin:0 auto;">
    <div style="display:grid; grid-template-columns:2fr 1fr 1fr 1fr; gap:4rem; padding-bottom:3rem; border-bottom:1px solid rgba(242,239,230,0.07); margin-bottom:2rem;">
      <div>
        <div style="font-family:Georgia,'Times New Roman',serif; font-size:1.5rem; font-weight:700; color:#F2EFE6; margin-bottom:0.75rem; display:flex; align-items:center; gap:0.4em;">
          <img src="assets/img/icons/icon-leaf.svg" alt="" style="width:1.1em;height:1.1em;opacity:0.6;">
          <span><span style="font-size:0.65em; font-weight:300; color:rgba(242,239,230,0.5); letter-spacing:0.02em; margin-right:0.2em;">the</span>Earth<span style="color:#C2A56C;">back</span><span style="font-size:0.55em; font-weight:400; color:rgba(242,239,230,0.35); letter-spacing:0.08em; margin-left:0.3em;">Project</span></span>
        </div>
        <p style="font-size:0.84rem; color:rgba(242,239,230,0.4); line-height:1.75; max-width:30ch; margin:0;">
          A community for people building a better world — natural materials, renewable energy, food systems, and mutual aid.
        </p>
      </div>
      <div>
        <h4 style="font-size:0.7rem; font-weight:700; letter-spacing:0.14em; text-transform:uppercase; color:#C2A56C; margin:0 0 1rem;">Platform</h4>
        <ul style="list-style:none; padding:0; margin:0; display:flex; flex-direction:column; gap:0.6rem;">
          <li><a href="feed.html" style="font-size:0.84rem; color:rgba(242,239,230,0.45); text-decoration:none;">The Feed</a></li>
          <li><a href="circles.html" style="font-size:0.84rem; color:rgba(242,239,230,0.45); text-decoration:none;">Circles</a></li>
          <li><a href="visualizer.html" style="font-size:0.84rem; color:rgba(242,239,230,0.45); text-decoration:none;">Visualizer</a></li>
          <li><a href="gallery.html" style="font-size:0.84rem; color:rgba(242,239,230,0.45); text-decoration:none;">Gallery</a></li>
          <li><a href="designer.html" style="font-size:0.84rem; color:rgba(242,239,230,0.45); text-decoration:none;">Estimator</a></li>
        </ul>
      </div>
      <div>
        <h4 style="font-size:0.7rem; font-weight:700; letter-spacing:0.14em; text-transform:uppercase; color:#C2A56C; margin:0 0 1rem;">Learn</h4>
        <ul style="list-style:none; padding:0; margin:0; display:flex; flex-direction:column; gap:0.6rem;">
          <li><a href="how-it-works.html" style="font-size:0.84rem; color:rgba(242,239,230,0.45); text-decoration:none;">How It Works</a></li>
          <li><a href="use-cases.html" style="font-size:0.84rem; color:rgba(242,239,230,0.45); text-decoration:none;">Use Cases</a></li>
          <li><a href="about.html" style="font-size:0.84rem; color:rgba(242,239,230,0.45); text-decoration:none;">About</a></li>
          <li><a href="training.html" style="font-size:0.84rem; color:rgba(242,239,230,0.45); text-decoration:none;">Training Partners</a></li>
        </ul>
      </div>
      <div>
        <h4 style="font-size:0.7rem; font-weight:700; letter-spacing:0.14em; text-transform:uppercase; color:#C2A56C; margin:0 0 1rem;">Legal</h4>
        <ul style="list-style:none; padding:0; margin:0; display:flex; flex-direction:column; gap:0.6rem;">
          <li><a href="safety.html" style="font-size:0.84rem; color:rgba(242,239,230,0.45); text-decoration:none;">Safety &amp; Trust</a></li>
          <li><a href="terms.html" style="font-size:0.84rem; color:rgba(242,239,230,0.45); text-decoration:none;">Terms</a></li>
          <li><a href="privacy.html" style="font-size:0.84rem; color:rgba(242,239,230,0.45); text-decoration:none;">Privacy</a></li>
          <li><a href="sitemap.html" style="font-size:0.84rem; color:rgba(242,239,230,0.45); text-decoration:none;">Site Map</a></li>
        </ul>
      </div>
    </div>
    <div style="display:flex; justify-content:space-between; align-items:center; font-size:0.74rem; color:rgba(242,239,230,0.22);">
      <span>&copy; 2026 Earthback. Built by the community, for the community.</span>
      <span style="font-family:Georgia,'Times New Roman',serif; font-style:italic;">The work that matters.</span>
    </div>
  </div>
</footer>
<style>
  #site-footer footer a:hover { color: #C2A56C !important; }
  @media (max-width: 768px) {
    #site-footer footer > div > div:first-child {
      grid-template-columns: 1fr !important;
      gap: 2rem !important;
    }
    #site-footer footer > div > div:last-child {
      flex-direction: column !important;
      gap: 0.5rem !important;
      text-align: center !important;
    }
  }
</style>`;

  const target = document.getElementById('site-footer');
  if (target) {
    target.innerHTML = footerHTML;
  }
})();
