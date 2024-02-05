chrome.action.onClicked.addListener((tab) => {
  chrome.scripting.executeScript({
    target: { tabId: tab.id },
    function: function () {
      const body = document.querySelector("body").innerHTML;
      fetch("https://h29opgs89s45oj-5000.proxy.runpod.net/createVacancy", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ html: body }),
      })
        .then((response) => response.json())
        .then((data) => console.log("Success:", data))
        .catch((error) => console.error("Error:", error));
    },
  });
});
