(() => {
  const root = document.documentElement;
  const themeToggle = document.querySelector('[data-theme-toggle]');
  const header = document.querySelector('[data-header]');
  const year = document.querySelector('[data-year]');

  const updateThemeButton = () => {
    if (!themeToggle) return;
    const isLight = root.dataset.theme === 'light';
    themeToggle.setAttribute('aria-pressed', String(isLight));
    themeToggle.setAttribute(
      'aria-label',
      isLight ? 'Switch to dark theme' : 'Switch to light theme'
    );
  };

  if (themeToggle) {
    updateThemeButton();
    themeToggle.addEventListener('click', () => {
      const nextTheme = root.dataset.theme === 'light' ? 'dark' : 'light';
      root.dataset.theme = nextTheme;
      try {
        localStorage.setItem('theme', nextTheme);
      } catch (_) {}
      updateThemeButton();
    });
  }

  if (header) {
    const updateHeader = () => {
      header.classList.toggle('is-scrolled', window.scrollY > 12);
    };
    updateHeader();
    window.addEventListener('scroll', updateHeader, { passive: true });
  }

  if (year) {
    year.textContent = String(new Date().getFullYear());
  }
})();
