let e=null;chrome.runtime.onMessage.addListener((p,d,t)=>(p.type==="setAppId"&&(e=p.appid),p.type==="getAppId"&&t({appid:e}),!0));
