        function acceptPrivateOffer() {
            let accepted_wage = parseInt(document.getElementById('wage_private').innerHTML);
            let effort = document.getElementById('effort_private').innerHTML.trim();
            let accepted_effort = effort === js_vars.name_high_effort ? 1 : 0;
            let currency_is_points = js_vars.currency_is_points;
            let job_id = parseInt(document.getElementById('job_id_private').innerHTML);
            let employer_id = parseInt(document.getElementById('employer_id_private').innerHTML);
            let job_number = parseInt(document.getElementById('job_number_private').innerHTML);
            try {
                liveSend({
                    "information_type": "accept",
                    "private": true,
                    "job_id": job_id,
                    "employer_id": employer_id,
                    "worker_id": js_vars.my_id,
                    "wage": accepted_wage,
                    "effort": accepted_effort,
                    "currency_is_points": currency_is_points,
                    "job_number": job_number,
                })
            } catch (err) {
                console.log('Error in acceptPrivateOffer' + err);
            }
        }
