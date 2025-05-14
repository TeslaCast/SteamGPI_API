const e=window.location.href.match(/store\.steampowered\.com\/app\/(\d+)/);if(e){const t=e[1];chrome.runtime.sendMessage({type:"setAppId",appid:t})}
