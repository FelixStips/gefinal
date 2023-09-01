    function acceptOffer() {
        let accepted_job_id = parseInt(document.getElementById("input_job_id_accept").value);
        try {
            let accepted_wage = parseInt(document.getElementById(`open_col_wage_${accepted_job_id}`).innerHTML);
            let effort = document.getElementById(`open_col_effort_${accepted_job_id}`).innerHTML.trim();
            let accepted_effort = 1 ? effort === js_vars.name_high_effort : 0;
            let accepted_employer_id = parseInt(document.getElementById(`open_col_employer_id_${accepted_job_id}`).innerHTML);
            let accepted_job_number = parseInt(document.getElementById(`open_col_job_number_${accepted_job_id}`).innerHTML);
            let worker_id = js_vars.my_id;
            let currency_is_points = js_vars.currency_is_points;
            liveSend({
                "information_type": "accept",
                "private": false,
                "employer_id": accepted_employer_id,
                "wage": accepted_wage,
                "effort": accepted_effort,
                "job_number": accepted_job_number,
                "job_id": accepted_job_id,
                "worker_id": worker_id,
                "employer_id": accepted_employer_id,
                "currency_is_points": currency_is_points,
            })
        } catch {
            alert("Error: Please enter a valid job ID.");
            return;
        } finally {
            document.getElementById("input_job_id_accept").value = "";
        }
    }