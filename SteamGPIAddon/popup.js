// popup.js (Firefox-совместимый, с кешем на 1 минуту)

async function getAppId() {
  try {
    const response = await browser.runtime.sendMessage({ type: "getAppId" });
    return response?.appid || null;
  } catch (err) {
    console.error("Ошибка получения appid:", err);
    return null;
  }
}

async function fetchFromAPI(appid) {
  const url = `http://localhost:8000/game/${appid}`;
  const res = await fetch(url);
  if (!res.ok) throw new Error("Ошибка при получении данных");
  return await res.json();
}

function formatPrice(price, currency, is_free) {
  if (price !== 0) {
    const num = parseFloat(price);
    if (isNaN(num)) return 'Недоступно';
    if (currency === 'USD' || currency === 'EUR') {
      return `${currency} ${num.toFixed(2)}`;
    }
    return `${num.toFixed(2)} ${currency}`;
  } else {
    return is_free === true ? 'Бесплатно' : 'Недоступно';
  }
}

function renderMainPage() {
  document.getElementById("game-title").textContent = "";
  document.getElementById("table-container").innerHTML = `
    <div class="main-instruction">
      <h2>Добро пожаловать в Steam Price Checker</h2>
      <p>Откройте страницу игры в Steam, чтобы увидеть цены и скидки.</p>
    </div>
  `;
}

function renderTable(gameData) {
  if (!Array.isArray(gameData) || gameData.length === 0) {
    document.getElementById("table-container").innerHTML = 
      '<div class="loading">❌ Нет данных для отображения</div>';
    return;
  }

  const gameName = gameData[0]?.name || "Неизвестная игра";
  document.getElementById("game-title").textContent = gameName;

  const rows = gameData.map(region => `
    <tr>
      <td>${region.region}</td>
      <td class="price">${formatPrice(region.initial_price, region.currency, region.is_free)}</td>
      <td class="price">${formatPrice(region.final_price, region.currency, region.is_free)}</td>
      <td class="discount">${region.discount_percent ? region.discount_percent + '%' : '0%'}</td>
    </tr>
  `).join("");

  document.getElementById("table-container").innerHTML = `
    <div class="table-wrapper">
      <table>
        <thead>
          <tr>
            <th>Регион</th>
            <th>Цена</th>
            <th>Цена со скидкой</th>
            <th>Скидка</th>
          </tr>
        </thead>
        <tbody>
          ${rows}
        </tbody>
      </table>
    </div>
  `;
}

async function loadAndRender(appid) {
  const cacheKey = `game_${appid}`;
  const cache = await browser.storage.local.get(cacheKey);
  const now = Date.now();

  if (cache[cacheKey] && now - cache[cacheKey].timestamp < 1_000) {
    // Используем кэш
    renderTable(cache[cacheKey].data);
  } else {
    // Получаем с сервера
    try {
      const data = await fetchFromAPI(appid);
      await browser.storage.local.set({ 
        [cacheKey]: { data, timestamp: now }
      });
      renderTable(data);
    } catch (err) {
      document.getElementById("table-container").innerHTML = 
        `<div class="loading">⚠️ ${err.message}</div>`;
    }
  }
}

// Основной блок
(async () => {
  const appid = await getAppId();
  if (!appid) {
    renderMainPage();
    return;
  }
  await loadAndRender(appid);
})();
