(function(){
  'use strict';
  const button=document.querySelector('.menu-toggle');
  const nav=document.querySelector('.site-nav');
  if(!button||!nav)return;
  function closeMenu(){button.setAttribute('aria-expanded','false');button.setAttribute('aria-label','Open navigation');nav.classList.remove('open')}
  button.addEventListener('click',function(){const open=button.getAttribute('aria-expanded')!=='true';button.setAttribute('aria-expanded',String(open));button.setAttribute('aria-label',open?'Close navigation':'Open navigation');nav.classList.toggle('open',open)});
  nav.querySelectorAll('a').forEach(function(link){link.addEventListener('click',closeMenu)});
  document.addEventListener('keydown',function(event){if(event.key==='Escape')closeMenu()});
})();
