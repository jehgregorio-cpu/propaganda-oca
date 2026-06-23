// ==========================================
// PROPAGANDA OCA — SCRIPTS
// ==========================================

// Nav scroll state
const nav = document.querySelector('.nav');
const onScroll = () => nav.classList.toggle('scrolled', window.scrollY > 40);
window.addEventListener('scroll', onScroll, { passive: true });
onScroll();

// Custom cursor
const cursor = document.getElementById('cursor');
if (cursor && window.matchMedia('(pointer: fine)').matches && !window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
  document.addEventListener('mousemove', e => {
    cursor.style.left = e.clientX + 'px';
    cursor.style.top  = e.clientY + 'px';
  });
  document.querySelectorAll('a, button, .servico-item').forEach(el => {
    el.addEventListener('mouseenter', () => cursor.classList.add('expanded'));
    el.addEventListener('mouseleave', () => cursor.classList.remove('expanded'));
  });
}

// Nav menu toggle
const toggle = document.getElementById('nav-toggle');
const menu   = document.getElementById('nav-menu');
const closeMenu = document.getElementById('nav-close');
const setMenuOpen = isOpen => {
  toggle?.classList.toggle('open', isOpen);
  menu?.classList.toggle('open', isOpen);
  document.body.classList.toggle('menu-open', isOpen);
  toggle?.setAttribute('aria-expanded', String(isOpen));
  toggle?.setAttribute('aria-label', isOpen ? 'Fechar menu' : 'Abrir menu');
  menu?.setAttribute('aria-hidden', String(!isOpen));
};

toggle?.addEventListener('click', () => {
  setMenuOpen(!menu.classList.contains('open'));
});
closeMenu?.addEventListener('click', () => {
  setMenuOpen(false);
  toggle?.focus();
});
menu?.querySelectorAll('a').forEach(a => {
  a.addEventListener('click', () => setMenuOpen(false));
});
document.addEventListener('keydown', e => {
  if (e.key === 'Escape' && menu?.classList.contains('open')) {
    setMenuOpen(false);
    toggle?.focus();
  }
});

// Accordion serviços
document.querySelectorAll('.servico-item').forEach(item => {
  const header = item.querySelector('.servico-top');
  const body = item.querySelector('.servico-body');
  if (!header || !body) return;

  header.setAttribute('role', 'button');
  header.setAttribute('tabindex', '0');
  header.setAttribute('aria-expanded', 'false');

  const toggleService = () => {
    const isOpen = item.classList.contains('open');
    document.querySelectorAll('.servico-item').forEach(i => {
      i.classList.remove('open');
      i.querySelector('.servico-top')?.setAttribute('aria-expanded', 'false');
    });
    if (!isOpen) {
      item.classList.add('open');
      header.setAttribute('aria-expanded', 'true');
    }
  };

  header.addEventListener('click', toggleService);
  header.addEventListener('keydown', e => {
    if (e.key === 'Enter' || e.key === ' ') {
      e.preventDefault();
      toggleService();
    }
  });
});
// Abre o primeiro por padrão
const firstService = document.querySelector('.servico-item');
firstService?.classList.add('open');
firstService?.querySelector('.servico-top')?.setAttribute('aria-expanded', 'true');

// Reveal on scroll
const observer = new IntersectionObserver(entries => {
  entries.forEach(e => { if (e.isIntersecting) { e.target.classList.add('in'); observer.unobserve(e.target); } });
}, { threshold: 0.1 });

document.querySelectorAll(
  '.mstat, .servico-item, .depo, .sobre-card, .proc-step'
).forEach((el, i) => {
  el.classList.add('reveal');
  el.style.transitionDelay = `${(i % 4) * 80}ms`;
  observer.observe(el);
});

// Form submit
const form = document.getElementById('form');
form?.addEventListener('submit', async e => {
  e.preventDefault();
  const btn = form.querySelector('.btn-submit');
  btn.textContent = 'Enviando...';
  btn.style.opacity = '.6';
  btn.disabled = true;
  try {
    const res = await fetch('https://formspree.io/f/mjgdeqnd', {
      method: 'POST',
      body: new FormData(form),
      headers: { 'Accept': 'application/json' }
    });
    if (res.ok) {
      form.innerHTML = `
        <div style="padding:60px 20px;text-align:center;">
          <div style="font-size:2.5rem;margin-bottom:24px">✓</div>
          <h3 style="font-family:'Bebas Neue',sans-serif;font-size:2.5rem;letter-spacing:.05em;margin-bottom:12px;color:#0A0A0A">MENSAGEM ENVIADA!</h3>
          <p style="font-family:'DM Mono',monospace;font-size:.8rem;letter-spacing:.08em;color:#888">Um especialista entra em contato em até 24h.</p>
        </div>
      `;
    } else {
      btn.textContent = 'Enviar e receber diagnóstico gratuito →';
      btn.style.opacity = '1';
      btn.disabled = false;
      alert('Erro ao enviar. Tente novamente ou entre em contato pelo WhatsApp.');
    }
  } catch {
    btn.textContent = 'Enviar e receber diagnóstico gratuito →';
    btn.style.opacity = '1';
    btn.disabled = false;
    alert('Erro ao enviar. Verifique sua conexão e tente novamente.');
  }
});
