const button = document.querySelector('.nav-toggle');
const nav = document.querySelector('.nav-links');

if (button && nav) {
  button.addEventListener('click', () => {
    const isOpen = button.getAttribute('aria-expanded') === 'true';
    button.setAttribute('aria-expanded', String(!isOpen));
    nav.classList.toggle('is-open');
  });
}
