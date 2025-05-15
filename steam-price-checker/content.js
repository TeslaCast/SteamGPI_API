// content.js
// Этот скрипт работает на странице Steam и отвечает за извлечение appid из URL и передачу его в background.js

// Пытаемся найти appid в URL страницы Steam с помощью регулярного выражения
const match = window.location.href.match(/store\.steampowered\.com\/app\/(\d+)/);

if (match) {
  // Если appid найден, отправляем сообщение background.js с типом "setAppId" и самим appid
  const appid = match[1];
  chrome.runtime.sendMessage({ type: "setAppId", appid });
} else {
  // Если appid не найден (например, главная страница Steam), отправляем сообщение для очистки appid
  chrome.runtime.sendMessage({ type: "clearAppId" });
}
