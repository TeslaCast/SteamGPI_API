import { auth } from "../firebase";
import {
  signInAnonymously,
  onAuthStateChanged
} from "firebase/auth";

// Получение appid от background.js
async function getAppId() {
  return new Promise((resolve) => {
    chrome.runtime.sendMessage({ type: "getAppId" }, (response) => {
      resolve(response?.appid || null);
    });
  });
}

// Получение данных с сервера
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

// Рендер таблицы
function renderTable(gameData) {
  if (!Array.isArray(gameData) || gameData.length === 0) {
    document.getElementById("table-container").innerHTML = 
      '<div class="loading">❌ Нет данных для отображения</div>';
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

// Авторизация и инициализация данных
function showAuthUI() {
  document.getElementById("auth-container").innerHTML = `
    <button id="login-btn">🔐 Войти</button>
  `;
  document.getElementById("login-btn").addEventListener("click", async () => {
    try {
      await signInAnonymously(auth);
    } catch (err) {
      alert("Ошибка входа: " + err.message);
    }
  });
}

async function main() {
  onAuthStateChanged(auth, async (user) => {
    if (!user) {
      showAuthUI();
      return;
    }

    const appid = await getAppId();
    if (!appid) {
      document.getElementById("table-container").innerHTML =
        `<div class="loading">❌ Откройте страницу игры в Steam</div>`;
      return;
    }

    const data = await fetchData(appid);
    if (data) renderTable(data);
  });
}

main();
