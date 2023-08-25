  // script.js

  document.addEventListener("DOMContentLoaded", function () {
    const body = document.body;
    const toggleIcon = document.querySelector(".toggle-icon");
  
    // Check if the user's color preference is stored in localStorage
    const currentColorMode = localStorage.getItem("colorMode");
  
    // Apply the stored color mode if available
    if (currentColorMode === "dark-mode") {
      enableDarkMode();
    } else {
      enableLightMode(); // Default to light mode if no preference is found
    }
  
    // Toggle the color mode when the user clicks the toggle icon
    toggleIcon.addEventListener("click", function () {
      if (body.classList.contains("dark-mode")) {
        enableLightMode();
      } else {
        enableDarkMode();
      }
    });
  
    // Function to enable dark mode
    function enableDarkMode() {
      body.classList.add("dark-mode");
      localStorage.setItem("colorMode", "dark-mode"); // Store the user's preference
    }
  
    // Function to enable light mode
    function enableLightMode() {
      body.classList.remove("dark-mode");
      localStorage.setItem("colorMode", "light-mode"); // Store the user's preference
    }
  });