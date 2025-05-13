// background.js
let lastAppId = null;

chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  if (message.type === "setAppId") {
    lastAppId = message.appid;
  }
  
  if (message.type === "getAppId") {
    sendResponse({ appid: lastAppId });
  }
  return true; // Важно для асинхронного sendResponse
});