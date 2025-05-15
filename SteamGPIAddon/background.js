// background.js
// Этот скрипт работает в фоне расширения и отвечает за хранение и передачу appid между компонентами расширения.

// Переменная для хранения текущего appid, изначально null
let lastAppId = null;

// Обработчик сообщений, получаемых от других частей расширения (content.js, popup.js)
chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  // Логируем полученное сообщение для отладки
  console.log("Background received message:", message);
  
  // Если сообщение типа "setAppId", значит нужно сохранить appid
  if (message.type === "setAppId") {
    // Сохраняем appid из сообщения в переменную lastAppId
    lastAppId = message.appid;
    // Логируем сохраненный appid
    console.log("Background set lastAppId:", lastAppId);
  }
  
  // Если сообщение типа "getAppId", значит кто-то запрашивает текущий appid
  if (message.type === "getAppId") {
    // Логируем текущий appid перед отправкой
    console.log("Background get lastAppId:", lastAppId);
    // Отправляем текущий appid в ответ
    sendResponse({ appid: lastAppId });
  }

  // Если сообщение типа "clearAppId", значит нужно очистить сохраненный appid
  if (message.type === "clearAppId") {
    // Обнуляем переменную lastAppId
    lastAppId = null;
    // Логируем очистку appid
    console.log("Background cleared lastAppId");
  }
  // Возвращаем true, чтобы указать, что sendResponse будет вызван асинхронно
  return true;
});
