(() => {
  'use strict';

  const toggle = document.querySelector('.menu-toggle');
  const navigation = document.querySelector('.site-nav');
  if (toggle && navigation) {
    const closeMenu = (restoreFocus = false) => {
      toggle.setAttribute('aria-expanded', 'false');
      toggle.setAttribute('aria-label', 'Open navigation');
      navigation.classList.remove('open');
      if (restoreFocus) toggle.focus();
    };
    toggle.addEventListener('click', () => {
      const open = toggle.getAttribute('aria-expanded') !== 'true';
      toggle.setAttribute('aria-expanded', String(open));
      toggle.setAttribute('aria-label', open ? 'Close navigation' : 'Open navigation');
      navigation.classList.toggle('open', open);
    });
    navigation.querySelectorAll('a').forEach(link => {
      link.addEventListener('click', () => closeMenu());
    });
    document.addEventListener('keydown', event => {
      if (event.key === 'Escape' && toggle.getAttribute('aria-expanded') === 'true') {
        closeMenu(true);
      }
    });
    const desktop = window.matchMedia('(min-width: 761px)');
    desktop.addEventListener('change', event => {
      if (event.matches) closeMenu();
    });
  }

  const filters = document.querySelector('.note-filters');
  const notes = Array.from(document.querySelectorAll('.note-row[data-topic]'));
  const count = document.getElementById('note-count');
  if (filters && notes.length) {
    filters.hidden = false;
    filters.querySelectorAll('button').forEach(button => {
      button.addEventListener('click', () => {
        const selected = button.dataset.filter;
        filters.querySelectorAll('button').forEach(option => {
          option.setAttribute('aria-pressed', String(option === button));
        });
        let visible = 0;
        notes.forEach(note => {
          const show = selected === 'all' || note.dataset.topic === selected;
          note.hidden = !show;
          if (show) visible += 1;
        });
        if (count) count.textContent = `${visible} ${visible === 1 ? 'note' : 'notes'}`;
      });
    });
  }

  if ('IntersectionObserver' in window) {
    const sectionLinks = Array.from(document.querySelectorAll('.site-nav a[href^="#"]'));
    const activeSection = new IntersectionObserver(entries => {
      entries.forEach(entry => {
        if (!entry.isIntersecting) return;
        sectionLinks.forEach(link => {
          if (link.hash === `#${entry.target.id}`) link.setAttribute('aria-current', 'location');
          else link.removeAttribute('aria-current');
        });
      });
    }, { rootMargin: '-15% 0px -65% 0px' });
    document.querySelectorAll('.home-page .hero, .home-page main > section[id]').forEach(section => activeSection.observe(section));
  }
})();
