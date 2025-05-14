(function(){const r=document.createElement("link").relList;if(r&&r.supports&&r.supports("modulepreload"))return;for(const e of document.querySelectorAll('link[rel="modulepreload"]'))c(e);new MutationObserver(e=>{for(const t of e)if(t.type==="childList")for(const o of t.addedNodes)o.tagName==="LINK"&&o.rel==="modulepreload"&&c(o)}).observe(document,{childList:!0,subtree:!0});function i(e){const t={};return e.integrity&&(t.integrity=e.integrity),e.referrerPolicy&&(t.referrerPolicy=e.referrerPolicy),e.crossOrigin==="use-credentials"?t.credentials="include":e.crossOrigin==="anonymous"?t.credentials="omit":t.credentials="same-origin",t}function c(e){if(e.ep)return;e.ep=!0;const t=i(e);fetch(e.href,t)}})();async function s(){return new Promise(n=>{chrome.runtime.sendMessage({type:"getAppId"},r=>{n((r==null?void 0:r.appid)||null)})})}async function a(n){const r=`http://localhost:8000/game/${n}`;try{const i=await fetch(r);if(!i.ok)throw new Error("Ошибка при получении данных");return await i.json()}catch(i){return document.getElementById("table-container").innerHTML=`<div class="loading">⚠️ ${i.message}</div>`,null}}function l(n){var e;if(!Array.isArray(n)||n.length===0){document.getElementById("table-container").innerHTML='<div class="loading">❌ Нет данных для отображения</div>';return}const r=(t,o)=>{if(t==null)return"N/A";const d=parseFloat(t);return isNaN(d)?"N/A":o==="USD"||o==="EUR"?`${o} ${d.toFixed(2)}`:`${d.toFixed(2)} ${o}`},i=((e=n[0])==null?void 0:e.name)||"Неизвестная игра";document.getElementById("game-title").textContent=i;const c=n.map(t=>`
    <tr>
      <td>${t.region}</td>
      <td class="price">${r(t.initial_price,t.currency)}</td>
      <td class="price">${r(t.final_price,t.currency)}</td>
      <td class="discount">${t.discount_percent?t.discount_percent+"%":"0%"}</td>
    </tr>
  `).join("");document.getElementById("table-container").innerHTML=`
    <div class="table-wrapper">
      <table>
        <thead>
          <tr>
            <th>Регион</th>
            <th>Обычная цена</th>
            <th>Цена со скидкой</th>
            <th>Скидка</th>
          </tr>
        </thead>
        <tbody>
          ${c}
        </tbody>
      </table>
    </div>
  `}(async()=>{const n=await s();if(!n){document.getElementById("table-container").innerHTML='<div class="loading">❌ Откройте страницу игры в Steam</div>';return}const r=await a(n);r&&l(r)})();
