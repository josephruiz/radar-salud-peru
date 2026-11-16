"use strict";
/* Editorial preview: deterministic selection, NOT medical or legal verification. */
(function(){
 const $=id=>document.getElementById(id);
 const priority=["saludconlupa.com","salud con lupa","la encerrona","hildebrandt","la lupa","infobae","brutalidad politica","medscape"];
 const lower=s=>String(s||"").normalize("NFD").replace(/[\u0300-\u036f]/g,"").toLowerCase();
 const health=["dengue","hospital","salud","enfermer","medic","vacun","epidemi","pacient","essalud","cirugia","agua","senamhi","lluvia","nino","norma","farmac","emergencia"];
 const risk=["dengue","epidemi","lluvia","nino","inundacion","hospital","emergencia","vacun","agua","medicament"];
 function score(x){const t=lower(x.title),src=lower(x.source);return health.reduce((n,w)=>n+(t.includes(w)?2:0),0)+risk.reduce((n,w)=>n+(t.includes(w)?3:0),0)+(priority.some(w=>src.includes(lower(w)))?3:0)+(x.region?2:0);}
 function note(target,text){const el=document.createElement("div");el.className="coffee-empty";el.textContent=text;target.replaceChildren(el);}
 function show(target,items,max){target.replaceChildren();if(!items.length){note(target,"No hay suficientes registros contrastados para esta sección. Se ampliarán las fuentes; no se completará con titulares ficticios.");return;}
 for(const x of items.slice(0,max)){const el=document.createElement("article");el.className="coffee-story";const a=document.createElement("a");try{const u=new URL(x.url);if(!["https:","http:"].includes(u.protocol))throw Error();a.href=u.href;a.target="_blank";a.rel="noopener noreferrer";}catch{continue;}a.textContent=x.title||"Sin título";el.append(a);const m=document.createElement("small");m.textContent=[x.source,x.region,x.published_at?.slice(0,10),"Pendiente de revisión"].filter(Boolean).join(" · ");el.append(m);target.append(el);}}
 async function load(){const date=$("date")?.value||new Intl.DateTimeFormat("en-CA",{timeZone:"America/Lima",year:"numeric",month:"2-digit",day:"2-digit"}).format(new Date());if(!/^\d{4}-\d{2}-\d{2}$/.test(date))return;const path=date.replaceAll("-","/");let items=[];try{const r=await fetch("data/"+path+"/edition.json",{cache:"no-store"});if(r.ok){const d=await r.json();items=Array.isArray(d.items)?d.items:[];}}catch{}
 const sorted=items.filter(x=>x.url&&x.title).sort((a,b)=>score(b)-score(a));show($("coffee-peru"),sorted.filter(x=>x.category!=="internacional"),6);
 // No geographic inference from a foreign-sounding title. International requires explicit tagging.
 show($("coffee-world"),sorted.filter(x=>x.category==="internacional"),3);
 try{const r=await fetch("data/"+path+"/el-peruano.json",{cache:"no-store"});const d=r.ok?await r.json():null;show($("coffee-laws"),(d?.items||[]).filter(x=>x.review_status==="verified"),3);}catch{note($("coffee-laws"),"Normas oficiales aún no verificadas. No se atribuyen cambios legales ni impactos profesionales sin revisar el texto original.");}
 }
 document.addEventListener("DOMContentLoaded",()=>{$("date")?.addEventListener("change",load);load();});
})();
