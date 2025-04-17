// content.js
const match = window.location.href.match(/store\.steampowered\.com\/app\/(\d+)/);
if (match) {
  const appid = match[1];
  chrome.runtime.sendMessage({ type: "setAppId", appid });
}