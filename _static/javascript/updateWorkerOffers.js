        function updateWorkerOffers(offers) {
            for (let i = 0; i < offers.length; i++) {
                if (offers[i].status === "accepted" && offers[i].worker_id == js_vars.my_id) {
                    let {job_id, wage_points, wage_tokens, effort} = offers[i];
                    let wage_displayed = js_vars.currency_is_points ? wage_points : wage_tokens;
                    if (effort === 1) {
                        var effort_displayed = js_vars.name_high_effort;
                    } else if (effort === 0) {
                        var effort_displayed = js_vars.name_low_effort;
                    } else {
                        var effort_displayed = "";
                        console.log("effort_displayed is wrong");
                    }
                    document.getElementById("worker_wage_accepted").innerHTML = wage_displayed;
                    document.getElementById("worker_effort_accepted").innerHTML = effort_displayed;
                    document.getElementById("worker_job_id_accepted").innerHTML = job_id;
                }
                if (offers[i].status === "open" && offers[i].private === true && offers[i].worker_id == js_vars.my_id) {
                    let {job_id, wage_points, wage_tokens, effort} = offers[i];
                    let wage_displayed = js_vars.currency_is_points ? wage_points : wage_tokens;
                    if (effort === 1) {
                        var effort_displayed = js_vars.name_high_effort;
                    } else if (effort === 0) {
                        var effort_displayed = js_vars.name_low_effort;
                    } else {
                        var effort_displayed = "";
                        console.log("effort_displayed is wrong");
                    }
                    document.getElementById("wage_private").innerHTML = wage_displayed;
                    document.getElementById("effort_private").innerHTML = effort_displayed;
                    document.getElementById("job_id_private").innerHTML = job_id;
                    document.getElementById("employer_id_private").innerHTML = offers[i].employer_id;
                    document.getElementById("job_number_private").style.display = offers[i].job_number;
                }
            }
        }