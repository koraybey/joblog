chrome.runtime.onInstalled.addListener(() => {
  chrome.action.disable();

  // Clear all rules to ensure only our expected rules are set
  chrome.declarativeContent.onPageChanged.removeRules(undefined, () => {
  let mainRule = {
    conditions: chrome.runtime.getManifest().host_permissions.map(h => {
      const [, sub, host] = h.match(/:\/\/(\*\.)?([^/]+)/);
      return new chrome.declarativeContent.PageStateMatcher({
        pageUrl: sub ? {hostSuffix: '.' + host} : {hostEquals: host},
      });
    }),
    actions: [new chrome.declarativeContent.ShowAction()],
  };

  // Finally, apply our new array of rules
  let rules = [mainRule];
  chrome.declarativeContent.onPageChanged.addRules(rules);
  });
});


chrome.action.onClicked.addListener((tab) => {
  chrome.scripting.executeScript({
    target: { tabId: tab.id },
    function: createVacancy,
  });
});

const createVacancy = () => {
  const url = location.href
  const html = document.querySelector("html").innerHTML;  
  fetch("http://127.0.0.1:5000/createVacancy", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ html, url }),
  })
    .then((response) => response.json())
    .then((data) => console.log("Success:", data))
    .catch((error) => console.error("Error:", error));
}

