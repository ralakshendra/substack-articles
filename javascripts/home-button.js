function addHomeButton() {
  const content = document.querySelector('.md-content__inner');
  if (!content || document.querySelector('.wwai-home-button') || document.querySelector('.wwai-home')) return;

  const button = document.createElement('a');
  button.className = 'wwai-home-button';
  button.href = '/substack-articles/';
  button.innerHTML = '<span>←</span> Back to Home';

  content.insertBefore(button, content.firstChild);
}

if (typeof document$ !== 'undefined') {
  document$.subscribe(addHomeButton);
} else {
  document.addEventListener('DOMContentLoaded', addHomeButton);
}
