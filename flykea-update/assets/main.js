(function(){
  var hdr=document.getElementById('hdr');
  function onScroll(){if(hdr)hdr.classList.toggle('scrolled',window.scrollY>40);}
  onScroll();window.addEventListener('scroll',onScroll,{passive:true});
  var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){e.target.classList.add('in');io.unobserve(e.target);}})},{threshold:.12});
  document.querySelectorAll('.reveal').forEach(function(el){io.observe(el);});
  function fmt(n){return n.toLocaleString('en-US');}
  function animate(el){var t;if(el.dataset.base){var per=+el.dataset.per||0,st=el.dataset.start?new Date(el.dataset.start).getTime():Date.now();var dd=Math.max(0,Math.floor((Date.now()-st)/864e5));t=(+el.dataset.base)+dd*per;}else{t=+el.dataset.target;}var sfx=el.dataset.suffix||'',d=1600,t0=performance.now();function tick(now){var p=Math.min((now-t0)/d,1),e=1-Math.pow(1-p,3);el.innerHTML=fmt(Math.round(t*e))+(sfx?'<span>'+sfx+'</span>':'');if(p<1)requestAnimationFrame(tick);}requestAnimationFrame(tick);}
  var sIO=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){e.target.querySelectorAll('.num').forEach(animate);sIO.unobserve(e.target);}})},{threshold:.4});
  document.querySelectorAll('.stats-grid').forEach(function(el){sIO.observe(el);});
  var b=document.querySelector('.burger'),m=document.querySelector('.mobile-menu');
  if(b&&m){b.addEventListener('click',function(){var open=m.classList.toggle('open');b.setAttribute('aria-expanded',open?'true':'false');b.setAttribute('aria-label',open?'Close menu':'Open menu');});}
})();

/* ---- FormSubmit progressive enhancement ----
   Contact form (no file): submitted via AJAX -> inline success, no page reload.
   Careers form (CV upload): native multipart POST -> redirected to /thank-you.html
   (FormSubmit's AJAX endpoint does not accept file attachments). */
(function(){
  function setStatus(el,kind,msg){ if(!el)return; el.hidden=!msg; el.textContent=msg||''; el.className='form-status'+(kind?(' '+kind):''); }
  document.querySelectorAll('form[data-formsubmit]').forEach(function(form){
    var btn=form.querySelector('button[type="submit"]');
    var fileInput=form.querySelector('input[type="file"]');
    var status=form.querySelector('.form-status');
    var nextInput=form.querySelector('input[name="_next"]');
    if(nextInput){ nextInput.value=location.origin+'/thank-you.html'; }

    form.addEventListener('submit',function(e){
      // CV present -> let the browser do a normal multipart POST (redirects via _next)
      if(fileInput && fileInput.files && fileInput.files.length){
        if(!form.checkValidity()){ return; }
        if(btn){ btn.disabled=true; btn.dataset.orig=btn.innerHTML; btn.textContent='Sending…'; }
        return; // native submission proceeds
      }
      // Otherwise AJAX submit for instant inline feedback
      e.preventDefault();
      if(!form.checkValidity()){ form.reportValidity(); return; }
      var orig=btn?btn.innerHTML:'';
      if(btn){ btn.disabled=true; btn.textContent='Sending…'; }
      setStatus(status,'','');
      var endpoint=form.getAttribute('action').replace('formsubmit.co/','formsubmit.co/ajax/');
      fetch(endpoint,{method:'POST',headers:{'Accept':'application/json'},body:new FormData(form)})
        .then(function(r){return r.json().catch(function(){return {};});})
        .then(function(d){
          if(d && (d.success===true || d.success==='true')){
            form.reset();
            setStatus(status,'ok','Thank you — your message has been sent. We’ll be in touch shortly.');
          }else{
            setStatus(status,'err',(d&&d.message)||'Something went wrong. Please email reservations@flykea.com.');
          }
        })
        .catch(function(){ setStatus(status,'err','Network error — please email reservations@flykea.com directly.'); })
        .finally(function(){ if(btn){ btn.disabled=false; btn.innerHTML=orig; } });
    });
  });
})();

/* ---- accessible carousels + lightbox (vanilla, no deps) ---- */
(function(){
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  function setupCarousel(car){
    var track=car.querySelector('.carousel-track');
    var slides=[].slice.call(car.querySelectorAll('.slide'));
    var prev=car.querySelector('.cprev'), next=car.querySelector('.cnext');
    var dots=[].slice.call(car.querySelectorAll('.cdot'));
    if(!track||slides.length<2) return;
    var idx=0;
    function go(i){ idx=Math.max(0,Math.min(slides.length-1,i));
      slides[idx].scrollIntoView({behavior:reduce?'auto':'smooth',inline:'start',block:'nearest'}); }
    if(prev) prev.addEventListener('click',function(){go(idx-1);});
    if(next) next.addEventListener('click',function(){go(idx+1);});
    dots.forEach(function(d){ d.addEventListener('click',function(){go(+d.dataset.i);}); });
    track.addEventListener('keydown',function(e){
      if(e.key==='ArrowRight'){e.preventDefault();go(idx+1);}
      else if(e.key==='ArrowLeft'){e.preventDefault();go(idx-1);}
      else if(e.key==='Home'){e.preventDefault();go(0);}
      else if(e.key==='End'){e.preventDefault();go(slides.length-1);}
    });
    var io=new IntersectionObserver(function(es){es.forEach(function(en){
      if(en.isIntersecting){ var i=slides.indexOf(en.target); if(i<0)return; idx=i;
        dots.forEach(function(d,j){ if(j===i)d.setAttribute('aria-current','true'); else d.removeAttribute('aria-current'); });
        if(prev) prev.disabled=(i===0);
        if(next) next.disabled=(i===slides.length-1);
      }});},{root:track,threshold:0.6});
    slides.forEach(function(s){io.observe(s);});
    if(prev) prev.disabled=true;
    if(car.hasAttribute('data-autoplay') && !reduce){
      var timer=null;
      function tick(){ go(idx>=slides.length-1?0:idx+1); }
      function start(){ if(!timer) timer=setInterval(tick,5000); }
      function stop(){ if(timer){clearInterval(timer);timer=null;} }
      car.addEventListener('mouseenter',stop); car.addEventListener('mouseleave',start);
      car.addEventListener('focusin',stop); car.addEventListener('focusout',start);
      start();
    }
  }
  [].forEach.call(document.querySelectorAll('.carousel'),setupCarousel);

  /* lightbox */
  var lb=document.getElementById('lightbox');
  if(!lb) return;
  var lbImg=lb.querySelector('.lb-img'), lbCap=lb.querySelector('.lb-cap');
  var btnClose=lb.querySelector('.lb-close'), btnPrev=lb.querySelector('.lb-prev'), btnNext=lb.querySelector('.lb-next');
  var group=[], gi=0, lastFocus=null;
  function show(i){ gi=(i+group.length)%group.length; var it=group[gi];
    lbImg.src=it.full; lbImg.alt=it.alt; lbCap.textContent=it.alt+'  ('+(gi+1)+' / '+group.length+')'; }
  function open(btns,start){ group=btns.map(function(b){return {full:b.dataset.full,alt:b.dataset.alt||''};});
    lastFocus=document.activeElement; lb.hidden=false; document.documentElement.style.overflow='hidden';
    show(start); btnClose.focus(); }
  function close(){ lb.hidden=true; document.documentElement.style.overflow=''; if(lastFocus)lastFocus.focus(); }
  [].forEach.call(document.querySelectorAll('.carousel'),function(car){
    var btns=[].slice.call(car.querySelectorAll('.slide-btn'));
    btns.forEach(function(b,i){ b.addEventListener('click',function(){ open(btns,i); }); });
  });
  btnClose.addEventListener('click',close);
  btnPrev.addEventListener('click',function(){show(gi-1);});
  btnNext.addEventListener('click',function(){show(gi+1);});
  lb.addEventListener('click',function(e){ if(e.target===lb) close(); });
  document.addEventListener('keydown',function(e){
    if(lb.hidden) return;
    if(e.key==='Escape') close();
    else if(e.key==='ArrowRight') show(gi+1);
    else if(e.key==='ArrowLeft') show(gi-1);
    else if(e.key==='Tab'){ var f=lb.querySelectorAll('button'); var first=f[0],last=f[f.length-1];
      if(e.shiftKey&&document.activeElement===first){e.preventDefault();last.focus();}
      else if(!e.shiftKey&&document.activeElement===last){e.preventDefault();first.focus();} }
  });
})();
