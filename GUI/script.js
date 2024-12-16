// JavaScript Code
document.getElementById("start-button").addEventListener("click", () => {
    document.getElementById("welcome-screen").classList.add("hidden");
    document.getElementById("selection-screen").classList.remove("hidden");
  });
  
  document.getElementById("compress-button").addEventListener("click", () => {
    const technique = document.querySelector('input[name="technique"]:checked');
    const fileInput = document.getElementById("file-input");
  
    if (!technique || !fileInput.files.length) {
      alert("Please select a compression technique and a file!");
      return;
    }
  
    document.getElementById("progress-bar").classList.remove("hidden");
  
    // Simulate compression process
    setTimeout(() => {
      document.getElementById("selection-screen").classList.add("hidden");
      document.getElementById("result-screen").classList.remove("hidden");
  
      // Mock data for demonstration
      document.getElementById(
        "compression-ratio"
      ).textContent = `Compression Ratio: ${(Math.random() * 0.5 + 0.5).toFixed(
        2
      )}`;
      document.getElementById(
        "compressed-length"
      ).textContent = `Length After Compression: ${
        Math.floor(Math.random() * 100) + 50
      } KB`;
    }, 3000); // Simulate 3-second delay
  });
  