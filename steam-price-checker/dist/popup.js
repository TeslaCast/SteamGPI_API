import{o as s,a as c,s as l}from"./firebase.js";async function u(){return new Promise(t=>{chrome.runtime.sendMessage({type:"getAppId"},n=>{t((n==null?void 0:n.appid)||null)})})}async function m(t){const n=`http://localhost:8000/game/${t}`;try{const a=await fetch(n);if(!a.ok)throw new Error("Ошибка при получении данных");return await a.json()}catch(a){return document.getElementById("table-container").innerHTML=`<div class="loading">⚠️ ${a.message}</div>`,null}}function h(t){var d;if(!Array.isArray(t)||t.length===0){document.getElementById("table-container").innerHTML='<div class="loading">❌ Нет данных для отображения</div>';return}const n=(e,i)=>{if(e==null)return"N/A";const r=parseFloat(e);return isNaN(r)?"N/A":i==="USD"||i==="EUR"?`${i} ${r.toFixed(2)}`:`${r.toFixed(2)} ${i}`},a=((d=t[0])==null?void 0:d.name)||"Неизвестная игра";document.getElementById("game-title").textContent=a;const o=t.map(e=>`
    <tr>
      <td>${e.region}</td>
      <td class="price">${n(e.initial_price,e.currency)}</td>
      <td class="price">${n(e.final_price,e.currency)}</td>
      <td class="discount">${e.discount_percent?e.discount_percent+"%":"0%"}</td>
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
          ${o}
        </tbody>
      </table>
    </div>
  `}function y(){document.getElementById("auth-container").innerHTML=`
    <button id="login-btn">🔐 Войти</button>
  `,document.getElementById("login-btn").addEventListener("click",async()=>{try{await l(c)}catch(t){alert("Ошибка входа: "+t.message)}})}async function f(){s(c,async t=>{if(!t){y();return}const n=await u();if(!n){document.getElementById("table-container").innerHTML='<div class="loading">❌ Откройте страницу игры в Steam</div>';return}const a=await m(n);a&&h(a)})}f();
