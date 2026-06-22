(function(){
  var hdr=document.getElementById('hdr');
  function onScroll(){if(hdr)hdr.classList.toggle('scrolled',window.scrollY>40);}
  onScroll();window.addEventListener('scroll',onScroll,{passive:true});
  var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){e.target.classList.add('in');io.unobserve(e.target);}})},{threshold:.12});
  document.querySelectorAll('.reveal').forEach(function(el){io.observe(el);});
  function fmt(n){return n.toLocaleString('en-US');}
  function animate(el){var t=+el.dataset.target,sfx=el.dataset.suffix||'',d=1600,t0=performance.now();function tick(now){var p=Math.min((now-t0)/d,1),e=1-Math.pow(1-p,3);el.innerHTML=fmt(Math.round(t*e))+(sfx?'<span>'+sfx+'</span>':'');if(p<1)requestAnimationFrame(tick);}requestAnimationFrame(tick);}
  var sIO=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){e.target.querySelectorAll('.num').forEach(animate);sIO.unobserve(e.target);}})},{threshold:.4});
  document.querySelectorAll('.stats-grid').forEach(function(el){sIO.observe(el);});
  var b=document.querySelector('.burger'),m=document.querySelector('.mobile-menu');
  if(b&&m){b.addEventListener('click',function(){m.classList.toggle('open');});}
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
