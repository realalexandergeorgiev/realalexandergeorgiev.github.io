// Mobile nav toggle + carousels + clipboard helpers
document.addEventListener('DOMContentLoaded', () => {
  // Clipboard: copy a template before/while firing mailto (some clients ignore body=)
  const copyText = async (text) => {
    try {
      if (navigator.clipboard && window.isSecureContext) {
        await navigator.clipboard.writeText(text);
        return true;
      }
    } catch (_) {}
    // Fallback for older browsers / non-secure contexts
    try {
      const ta = document.createElement('textarea');
      ta.value = text;
      ta.style.position = 'fixed';
      ta.style.opacity = '0';
      document.body.appendChild(ta);
      ta.focus();
      ta.select();
      const ok = document.execCommand('copy');
      ta.remove();
      return ok;
    } catch (_) { return false; }
  };

  // Links/buttons with data-copy-template: copy that text on click (mailto still fires)
  document.querySelectorAll('[data-copy-template]').forEach(el => {
    el.addEventListener('click', async () => {
      const text = el.getAttribute('data-copy-template').replace(/&#10;/g, '\n');
      const label = el.getAttribute('data-copy-label') ||
        "Template copied to clipboard — paste it into your email if it didn't auto-fill.";
      const ok = await copyText(text);
      const feedback = el.parentElement.querySelector('.women-cta__copy-feedback');
      if (feedback) {
        feedback.textContent = ok ? label : "Couldn't copy automatically — see the template below.";
        feedback.hidden = false;
        feedback.style.opacity = '1';
        setTimeout(() => { feedback.style.opacity = '0'; }, 6000);
      }
    });
  });

  // Buttons with data-copy-from="#selector": copy that element's text
  document.querySelectorAll('[data-copy-from]').forEach(btn => {
    btn.addEventListener('click', async () => {
      const src = document.querySelector(btn.getAttribute('data-copy-from'));
      if (!src) return;
      const ok = await copyText(src.textContent);
      const original = btn.innerHTML;
      btn.innerHTML = ok
        ? '<i class="fas fa-check"></i> Copied!'
        : '<i class="fas fa-triangle-exclamation"></i> Copy failed';
      setTimeout(() => { btn.innerHTML = original; }, 2500);
    });
  });

  // Speaker carousel arrows
  document.querySelectorAll('.speakers').forEach(carousel => {
    const track = carousel.querySelector('.speakers__track');
    const prev = carousel.querySelector('.speakers__nav--prev');
    const next = carousel.querySelector('.speakers__nav--next');
    if (!track) return;

    const scrollBy = () => {
      const card = track.querySelector('.speaker-card');
      const gap = parseInt(getComputedStyle(track).columnGap || getComputedStyle(track).gap || '16', 10);
      return (card ? card.getBoundingClientRect().width : 320) + gap;
    };

    const updateState = () => {
      const max = track.scrollWidth - track.clientWidth - 2;
      if (prev) prev.toggleAttribute('disabled', track.scrollLeft <= 2);
      if (next) next.toggleAttribute('disabled', track.scrollLeft >= max);
    };

    prev?.addEventListener('click', () => track.scrollBy({ left: -scrollBy(), behavior: 'smooth' }));
    next?.addEventListener('click', () => track.scrollBy({ left: scrollBy(), behavior: 'smooth' }));
    track.addEventListener('scroll', updateState, { passive: true });
    updateState();
  });

  const toggle = document.querySelector('.nav__toggle');
  const panel = document.getElementById('nav-panel');
  if (toggle && panel) {
    toggle.addEventListener('click', () => {
      const open = panel.classList.toggle('is-open');
      toggle.setAttribute('aria-expanded', String(open));
    });
  }

  // Animate stat counters when visible
  const stats = document.querySelectorAll('[data-count-to]');
  if ('IntersectionObserver' in window && stats.length) {
    const io = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (!entry.isIntersecting) return;
        const el = entry.target;
        const target = parseInt(el.dataset.countTo, 10);
        const dur = 1200;
        const start = performance.now();
        const step = (t) => {
          const p = Math.min(1, (t - start) / dur);
          el.textContent = Math.round(target * (1 - Math.pow(1 - p, 3)));
          if (p < 1) requestAnimationFrame(step);
        };
        requestAnimationFrame(step);
        io.unobserve(el);
      });
    }, { threshold: 0.3 });
    stats.forEach(s => io.observe(s));
  }
});
