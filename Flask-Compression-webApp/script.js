document.getElementById("start-button").addEventListener("click", () => {
    document.getElementById("welcome-screen").classList.add("hidden");
    document.getElementById("selection-screen").classList.remove("hidden");
  });
  
  document.getElementById("process-button").addEventListener("click", () => {
    const fileInput = document.getElementById("file-input");
    const operation = document.querySelector('input[name="operation"]:checked');
  
    if (!operation || !fileInput.files.length) {
      alert("Please select an operation and upload a file!");
      return;
    }
  
    const formData = new FormData();
    formData.append("operation", operation.value);
    formData.append("file", fileInput.files[0]);
  
    document.getElementById("progress-bar").classList.remove("hidden");
  
    fetch("/process", {
      method: "POST",
      body: formData,
    })
      .then(response => response.json())
      .then(data => {
        document.getElementById("progress-bar").classList.add("hidden");
        document.getElementById("result-screen").classList.remove("hidden");
  
        document.getElementById("operation").textContent = data.operation;
        document.getElementById("original").textContent = data.original;
        document.getElementById("output").textContent = data.output;
      })
      .catch(err => {
        alert("Error processing the file!");
        console.error(err);
      });
  });
  