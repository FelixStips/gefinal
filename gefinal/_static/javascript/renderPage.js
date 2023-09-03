        function renderPage(page_information) {
            let {is_finished} = page_information;

            // Submit page if done
            if (is_finished) {
                document.getElementById("to_next_page").click();
            } else {
                document.getElementById('info_box').style.display = 'block';
                document.getElementById('offers_table').style.display = 'block';
            }
        }