// popup.js

async function getPrices(appid) {
    const res = await fetch(`http://localhost:8000/game/${appid}`);
    const data = await res.json();
  
    const container = document.getElementById("prices");
    container.innerHTML = "";
  
    data.forEach(regionInfo => {
      const block = document.createElement("div");
      block.className = "region-block";
      block.innerHTML = `
        <strong>${regionInfo.region}</strong>: ${regionInfo.final_price ?? "N/A"} ${regionInfo.currency ?? ""}
      `;
      container.appendChild(block);
    });
  }
  
  chrome.runtime.sendMessage({ type: "getAppId" }, (response) => {
    if (response?.appid) {
      getPrices(response.appid);
    } else {
      document.getElementById("prices").innerText = "AppID не найден на странице.";
    }
  });
  