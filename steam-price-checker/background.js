// background.js

let lastAppId = null;

chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  if (message.appid) {
    lastAppId = message.appid;
  }
});

chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  if (message.type === "getAppId") {
    sendResponse({ appid: lastAppId });
  }
});
