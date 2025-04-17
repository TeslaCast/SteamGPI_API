async function getAppId() {
  return new Promise((resolve) => {
    chrome.runtime.sendMessage({ type: "getAppId" }, (response) => {
      resolve(response?.appid || null);
    });
  });
}

async function fetchData(appid) {
  const url = `http://localhost:8000/game/${appid}`;
  try {
    const res = await fetch(url);
    if (!res.ok) throw new Error("Ошибка при получении данных");
    return await res.json();
  } catch (err) {
    document.getElementById("table-container").innerHTML = 
      `<div class="loading">⚠️ ${err.message}</div>`;
    return null;
  }
}

function renderTable(gameData) {
  if (!Array.isArray(gameData)) {
    document.getElementById("table-container").innerHTML = 
      '<div class="loading">❌ Нет данных для отображения</div>';
    return;
  }

  const gameName = gameData[0]?.name || "Неизвестная игра";
  document.getElementById("game-title").textContent = gameName;

  const rows = gameData.map(region => `
    <div class="row">
      <div class="cell region" title="${region.region}">
        ${region.region}
      </div>
      <div class="cell price" title="${region.initial_price ?? 'N/A'} ${region.currency}">
        ${region.initial_price ?? 'N/A'} ${region.currency}
      </div>
      <div class="cell price" title="${region.final_price ?? 'N/A'} ${region.currency}">
        ${region.final_price ?? 'N/A'} ${region.currency}
      </div>
      <div class="cell discount">
        ${region.discount_percent ? region.discount_percent + '%' : '-'}
      </div>
    </div>
  `).join("");

  document.getElementById("table-container").innerHTML = `
    <div class="table">
      <div class="cell header">Регион</div>
      <div class="cell header">Обычная цена</div>
      <div class="cell header">Цена со скидкой</div>
      <div class="cell header">Скидка</div>
      ${rows}
    </div>
  `;
}

(async () => {
  const appid = await getAppId();
  if (!appid) {
    document.getElementById("table-container").innerHTML = 
      `<div class="loading">❌ Откройте страницу игры в Steam</div>`;
    return;
  }
  
  const data = await fetchData(appid);
  if (data) renderTable(data);
})();