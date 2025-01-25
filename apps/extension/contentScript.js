const createToast = (message, isError = false) => {
    // Create wrapper for fade-in effect
    const toast = document.createElement('div');
    toast.style.cssText = `
      position: fixed;
      top: 20px;
      right: 20px;
      padding: 16px 24px;
      background-color: ${isError ? '#f44336' : '#4CAF50'};
      color: white;
      border-radius: 4px;
      z-index: 10000;
      box-shadow: 0 2px 5px rgba(0,0,0,0.2);
      font-family: system-ui;
      opacity: 0;
      transform: translateX(100%);
      transition: all 0.3s ease;
    `;
    toast.textContent = message;
  
    // Create progress bar
    const progressBar = document.createElement('div');
    progressBar.style.cssText = `
      position: absolute;
      bottom: 0;
      left: 0;
      height: 3px;
      width: 100%;
      background-color: rgba(255, 255, 255, 0.7);
      transform-origin: left;
      transform: scaleX(1);
      transition: transform 3s linear;
    `;
    toast.appendChild(progressBar);
  
    document.body.appendChild(toast);
  
    // Trigger fade-in
    requestAnimationFrame(() => {
      toast.style.opacity = '1';
      toast.style.transform = 'translateX(0)';
      // Start progress bar animation
      requestAnimationFrame(() => {
        progressBar.style.transform = 'scaleX(0)';
      });
    });
    
    // Fade out after 3 seconds
    setTimeout(() => {
      toast.style.opacity = '0';
      toast.style.transform = 'translateX(100%)';
      setTimeout(() => toast.remove(), 300); // Remove after fade animation
    }, 3000);
  };
  
  function handleVacancy() {
    const url = location.href;
    const html = document.querySelector("html").innerHTML;  
    fetch("http://127.0.0.1:5000/createVacancy", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ html, url }),
    })
      .then((response) => response.json())
      .then((data) => {
        console.log("Success:", data);
        createToast('Vacancy created successfully!');
      })
      .catch((error) => {
        console.error("Error:", error);
        createToast(error.message || 'Failed to create vacancy', true);
      });
  }
  
  // Listen for messages from the background script
  chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
    if (request.action === 'createVacancy') {
      handleVacancy();
    }
  });