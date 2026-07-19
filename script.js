// ============================================
// script.js — small interactive touches
// ============================================

// 1. Keep the footer year current automatically.
document.getElementById('year').textContent = new Date().getFullYear();

// 2. Gently fade sections in as they scroll into view.
//    If the browser doesn't support this, sections just stay visible.
const sections = document.querySelectorAll('.section');

if ('IntersectionObserver' in window) {
  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add('visible');
          observer.unobserve(entry.target);
        }
      });
    },
    { threshold: 0.1 }
  );

  sections.forEach((section) => {
    section.classList.add('fade-in');
    observer.observe(section);
  });
}

// The styles for the fade effect are added here so the site still
// looks complete even if JavaScript is turned off.
const fadeStyles = document.createElement('style');
fadeStyles.textContent = `
  .fade-in {
    opacity: 0;
    transform: translateY(14px);
    transition: opacity 0.6s ease, transform 0.6s ease;
  }
  .fade-in.visible {
    opacity: 1;
    transform: translateY(0);
  }
`;
document.head.appendChild(fadeStyles);
