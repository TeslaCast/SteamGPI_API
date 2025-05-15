// content.js
// Этот скрипт работает на странице Steam и отвечает за извлечение appid из URL и передачу его в background.js

// Функция для извлечения appid из текущего URL и отправки сообщения в background.js
function sendAppIdFromUrl() {
  const match = window.location.href.match(/store\.steampowered\.com\/app\/(\d+)/);
  console.log("URL is: ", match);
  if (match) {
    const appid = match[1];
    console.log("Content script: found appid", appid);
    chrome.runtime.sendMessage({ type: "setAppId", appid });
  } else {
    console.log("Content script: no appid found in URL");
    chrome.runtime.sendMessage({ type: "clearAppId" });
  }
}

// Выполняем при загрузке страницы
sendAppIdFromUrl();
