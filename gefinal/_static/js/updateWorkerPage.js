        function updateWorkerPage(worker_information) {
            let {wait, invalid, show_private} = worker_information;
            if (js_vars.is_employer==false) {
                document.getElementById("trading_mask").style.display = "none";                                         // Hide trading mask
                if (wait) {                                                                                             // Unless wait is true, show accept mask
                    document.getElementById("worker_wait").style.display = "block";
                    document.getElementById("accept_mask").style.display = "none";
                } else {
                    document.getElementById("worker_wait").style.display = "none";
                    document.getElementById("accept_mask").style.display = "block";
                }
                if (show_private) {                                                                                     // Show private offers if show_private is true
                    document.getElementById("private_offer").style.display = "block";
                } else {
                    document.getElementById("private_offer").style.display = "none";
                }
                if (invalid) {                                                                                          // If invalid is true, show alert
                    alert("The job id you have entered is not valid!");
                }
            }
        }
