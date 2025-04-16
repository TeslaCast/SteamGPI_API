// content.js

const match = window.location.href.match(/\/app\/(\d+)/);
if (match) {
  const appid = match[1];
  chrome.runtime.sendMessage({ appid });
}
