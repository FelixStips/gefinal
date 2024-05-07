    function MoveToPrevious(btn) {
        let currentTab = btn.parentElement.parentElement;
        let previousTab = currentTab.previousElementSibling;
        currentTab.style.display = "none";
        previousTab.style.display = "block";
        window.scrollTo(0, 0); // Scroll to the top of the page
    }