// popup.js
// Этот скрипт отвечает за логику всплывающего окна расширения: получение appid, запрос данных и отображение таблицы с ценами.

// Кешируем appid, чтобы не запрашивать его повторно у background.js
let cachedAppId = null;

// Функция для получения appid из background.js или из кеша
async function getAppId() {
  if (cachedAppId !== null) {
    console.log("Popup: returning cached appid", cachedAppId);
    return cachedAppId;
  }
  console.log("Popup: calling getAppId");
  return new Promise((resolve) => {
    chrome.runtime.sendMessage({ type: "getAppId" }, (response) => {
      console.log("Popup: received appid", response?.appid);
      cachedAppId = response?.appid || null;
      resolve(cachedAppId);
    });
  });
}

// Функция для запроса данных игры по appid из api_gateway
async function fetchData(appid) {
  const url = `http://localhost:8000/game/${appid}`;
  try {
    const res = await fetch(url);
    if (!res.ok) throw new Error("Ошибка при получении данных");
    // После успешного запроса очищаем appid и кеш
    chrome.runtime.sendMessage({ type: "clearAppId" });
    cachedAppId = null;
    return await res.json();
  } catch (err) {
    document.getElementById("table-container").innerHTML = 
      `<div class="loading">⚠️ ${err.message}</div>`;
    return null;
  }
}

// Функция для отображения таблицы с данными игры
function renderTable(gameData) {
  if (!Array.isArray(gameData) || gameData.length === 0) {
    document.getElementById("table-container").innerHTML = 
      '<div class="loading">❌ Нет данных для отображения</div>';
    (async () => {
      const appid = await getAppId();
      fetchData(appid);
    })();
    return;
  }

  const formatPrice = (price, currency) => {
    if (price === null || price === undefined) return 'N/A';
    const num = parseFloat(price);
    if (isNaN(num)) return 'N/A';
    
    if (currency === 'USD' || currency === 'EUR') {
      return `${currency} ${num.toFixed(2)}`;
    }
    return `${num.toFixed(2)} ${currency}`;
  };

  const gameName = gameData[0]?.name || "Неизвестная игра";
  document.getElementById("game-title").textContent = gameName;

  const rows = gameData.map(region => `
    <tr>
      <td>${region.region}</td>
      <td class="price">${formatPrice(region.initial_price, region.currency)}</td>
      <td class="price">${formatPrice(region.final_price, region.currency)}</td>
      <td class="discount">${region.discount_percent ? region.discount_percent + '%' : '0%'}</td>
    </tr>
  `).join("");

  document.getElementById("table-container").innerHTML = `
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
          ${rows}
        </tbody>
      </table>
    </div>
  `;
}

// Функция для отображения главной страницы расширения с инструкциями
function renderMainPage() {
  document.getElementById("game-title").textContent = "";
  document.getElementById("table-container").innerHTML = `
    <div class="main-instruction">
      <h2>Добро пожаловать в Steam Price Checker</h2>
      <p>Откройте страницу игры в Steam, чтобы увидеть цены и скидки.</p>
      <p>Если вы не на странице игры, пожалуйста, перейдите на страницу игры в Steam и обновите расширение.</p>
    </div>
  `;
}

// Основной асинхронный блок, который запускается при открытии popup
(async () => {
  const appid = await getAppId();
  if (!appid) {
    renderMainPage();
    return;
  }
  
  const data = await fetchData(appid);
  if (data) renderTable(data);
})();
