        function updateEmployerOffers(offers) {
            for (let i = 0; i < offers.length; i++) {
                let {job_id, wage_points, wage_tokens, effort, job_number} = offers[i];
                var wage_displayed = js_vars.currency_is_points ? wage_points : wage_tokens;
                    if (effort === 1) {
                        var effort_displayed = js_vars.name_high_effort;
                    } else if (effort === 0) {
                        var effort_displayed = js_vars.name_low_effort;
                    } else {
                        var effort_displayed = "";
                        console.log("effort_displayed is wrong");
                    }
                if (offers[i].status === "open" && offers[i].employer_id == js_vars.my_id) {
                    console.log('Open, job number ' + job_number)
                    console.log(offers[i])
                    document.getElementById(`employer_wage_offered_${job_number}`).innerHTML = wage_displayed;
                    document.getElementById(`employer_effort_offered_${job_number}`).innerHTML = effort_displayed;
                    document.getElementById(`employer_job_id_offered_${job_number}`).innerHTML = job_id;
                }
                if (offers[i].status === "accepted" && offers[i].employer_id == js_vars.my_id) {
                    document.getElementById(`employer_wage_accepted_${job_number}`).innerHTML = wage_displayed;
                    document.getElementById(`employer_effort_accepted_${job_number}`).innerHTML = effort_displayed;
                    document.getElementById(`employer_job_id_accepted_${job_number}`).innerHTML = job_id;
                }
            }
        }