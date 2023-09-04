

        function updateTable(offers) {
            let open_offers_body = document.getElementById("open_offers_body");
            let accepted_offers_body = document.getElementById("accepted_offers_body");

            // Clear table
            open_offers_body.innerHTML = "";
            accepted_offers_body.innerHTML = "";

            // Loop over public offers
            var publicOffers = offers.filter(offer => offer.private === false);
            for (let i = 0; i < publicOffers.length; i++) {
                // Retrieve information
                let {job_id, wage_points, wage_tokens, effort, status, employer_id, job_number} = publicOffers[i];
                let wage_displayed = js_vars.currency_is_points ? wage_points : wage_tokens;
                if (effort === 1) {
                    var effort_displayed = js_vars.name_high_effort;
                } else if (effort === 0) {
                    var effort_displayed = js_vars.name_low_effort;
                } else {
                    var effort_displayed = "";
                    console.log("effort_displayed is wrong");
                }

                // Update open offers table
                if (status === "open") {
                    open_offers_body.innerHTML += `<tr id="open_row_${job_id}">
                                                        <td id="open_col_job_id_${job_id}"> ${job_id} </td>
                                                        <td id="open_col_wage_${job_id}"> ${wage_displayed} </td>
                                                        <td id="open_col_effort_${job_id}"> ${effort_displayed} </td>
                                                        <td id="open_col_status_${job_id}" style="color: #008000;"> ${status} </td>
                                                        <td id="open_col_employer_id_${job_id}" style="display: none"> ${employer_id} </td>
                                                        <td id="open_col_job_number_${job_id}" style="display: none"> ${job_number} </td>
                                                    </tr>`;
                // Updated accepted offers table
                } else if (status === "accepted") {
                    accepted_offers_body.innerHTML += `<tr id="accepted_row_${job_id}">
                                                        <td id="accepted_col_job_id_${job_id}"> ${job_id} </td>
                                                        <td id="accepted_col_wage_${job_id}"> ${wage_displayed} </td>
                                                        <td id="accepted_col_effort_${job_id}"> ${effort_displayed} </td>
                                                        <td id="accepted_col_status_${job_id}" style="color: #0000CD;"> ${status} </td>
                                                    </tr>`;
                }
            }
        }