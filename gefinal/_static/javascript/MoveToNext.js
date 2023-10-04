

    function MoveToNext(btn) {
        let currentTab = btn.parentElement.parentElement;
        let nextTab = currentTab.nextElementSibling;
        currentTab.style.display = "none";
        nextTab.style.display = "block";
        window.scrollTo(0, 0); // Scroll to the top of the page
    }
