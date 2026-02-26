/**
 * Early Access Banner — centralised, one place to edit.
 *
 * Config lives right here. Change the text, swap the CTA,
 * or set  enabled = false  to kill it across every page.
 */

(function () {
  /* ── CONFIG ─────────────────────────────────────────── */

  const BANNER = {
    enabled: true,

    label: 'Early Access',
    message: 'Claim your username and get in early — your voice shapes what gets built.',
    cta: {
      text: 'Join free →',
      href: 'join.html'
    },

    /* set to null to hide the dismiss ✕ */
    dismissKey: 'eb_banner_dismissed'
  };

  /* ── RENDER ─────────────────────────────────────────── */

  if (!BANNER.enabled) return;

  /* respect dismiss */
  if (BANNER.dismissKey) {
    try { if (sessionStorage.getItem(BANNER.dismissKey)) return; } catch (e) { /* private mode */ }
  }

  var aside = document.createElement('aside');
  aside.id = 'eb-early-access';
  aside.style.cssText =
    'position:fixed;bottom:0;left:0;right:0;' +
    'background:linear-gradient(135deg,#1F3A2E,#2d5a27);' +
    'color:rgba(255,255,255,0.9);text-align:center;' +
    'padding:10px 20px;font-size:0.78rem;' +
    "font-family:'Inter',system-ui,sans-serif;" +
    'z-index:9999;box-shadow:0 -2px 12px rgba(0,0,0,0.15);' +
    'display:flex;align-items:center;justify-content:center;' +
    'gap:8px;flex-wrap:wrap';

  var html =
    '<span style="font-weight:600">' +
      '<img src="assets/img/icons/icon-leaf.svg" alt="" ' +
        'style="width:0.9em;height:0.9em;vertical-align:-0.1em;margin-right:3px;"> ' +
      BANNER.label +
    '</span>' +
    '<span style="opacity:0.7">—</span>' +
    '<span>' + BANNER.message + '</span>';

  if (BANNER.cta) {
    html +=
      '<a href="' + BANNER.cta.href + '" ' +
        'style="color:#C2A56C;text-decoration:none;font-weight:600;margin-left:4px">' +
        BANNER.cta.text +
      '</a>';
  }

  if (BANNER.dismissKey) {
    html +=
      '<button onclick="try{sessionStorage.setItem(\'' + BANNER.dismissKey + '\',\'1\')}catch(e){};' +
        'this.parentElement.remove()" ' +
        'style="background:none;border:none;color:rgba(255,255,255,0.5);' +
        'cursor:pointer;font-size:1rem;margin-left:8px;padding:0 4px" ' +
        'aria-label="Dismiss">✕</button>';
  }

  aside.innerHTML = html;
  document.body.appendChild(aside);
})();
