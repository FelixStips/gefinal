
        function updateEmployerPage(employer_information) {
            let {done, num_workers_employed, offer1, offer2, offer3, offer4} = employer_information;
            if (js_vars.is_employer==true) {

                // Update overall page view
                document.getElementById("trading_mask").style.display = "block";
                document.getElementById("worker_wait").style.display = "none";
                document.getElementById("private_offer").style.display = "none";
                document.getElementById("accept_mask").style.display = "none";

                // Is the employer done?
                if (done) {
                    document.getElementById("employer_done").style.display = "block";
                    document.getElementById("no_more_offers").style.display = "none";
                    document.getElementById("employer_max_workers").style.display = "none";
                } else if (num_workers_employed===2) {
                    document.getElementById("employer_max_workers").style.display = "block";
                    document.getElementById("employer_done").style.display = "none";
                    document.getElementById("no_more_offers").style.display = "none";
                } else {
                    document.getElementById("employer_max_workers").style.display = "none";
                    document.getElementById("employer_done").style.display = "none";
                    document.getElementById("no_more_offers").style.display = "block";
                }


                // Update public offer mask
                const public_offers_status = [offer1, offer2];
                for (let i = 0; i < public_offers_status.length; i++) {
                    let offer_status = public_offers_status[i];
                    let counter = i + 1;
                    if (offer_status === "empty" || offer_status === "cancelled")  {
                        // Empty or cancelled: show the offer mask if employer is not done or has not reached the limit of 2 workers
                        document.getElementById(`employer_wait_${counter}`).style.display = "none";
                        document.getElementById(`employer_accepted_${counter}`).style.display = "none";
                        if (num_workers_employed===2 || done==true) {
                            document.getElementById(`offer_mask_${counter}`).style.display = "none";
                        } else {
                            document.getElementById(`offer_mask_${counter}`).style.display = "block";
                        }
                    } else if (offer_status === "open") {
                        document.getElementById(`offer_mask_${counter}`).style.display = "none";
                        document.getElementById(`employer_wait_${counter}`).style.display = "block";
                        document.getElementById(`employer_accepted_${counter}`).style.display = "none";
                    } else if (offer_status === "accepted") {
                        document.getElementById(`offer_mask_${counter}`).style.display = "none";
                        document.getElementById(`employer_wait_${counter}`).style.display = "none";
                        document.getElementById(`employer_accepted_${counter}`).style.display = "block";
                    }
                }

                // Update private offer mask
                const private_offers_status = [offer3, offer4];
                for (let i = 0; i < private_offers_status.length; i++) {
                    let offer_status = private_offers_status[i];
                    let counter = i + 3;
                    if (offer_status === "empty" || offer_status === "cancelled")  {
                        document.getElementById(`employer_wait_${counter}`).style.display = "none";
                        document.getElementById(`employer_accepted_${counter}`).style.display = "none";
                    } else if (offer_status === "open") {
                        document.getElementById(`employer_wait_${counter}`).style.display = "block";
                        document.getElementById(`employer_accepted_${counter}`).style.display = "none";
                    } else if (offer_status === "accepted") {
                        document.getElementById(`employer_wait_${counter}`).style.display = "none";
                        document.getElementById(`employer_accepted_${counter}`).style.display = "block";
                    }
                }
            }
        }
