
    function sendOffer(offer_sent) {
         let job_offer_number = parseInt(offer_sent.slice(-1));
          let effort_input_element = document.getElementById(`effort_input_${job_offer_number}`);
          let wage_input_element = document.getElementById(`wage_input_${job_offer_number}`);
          if (!isNumeric(effort_input_element.value) || !isNumeric(wage_input_element.value)) {
            alert("Error: Please choose a wage and an effort level before sending the offer.");
            return;
          }
        let effort_inputted = parseInt(effort_input_element.value);
        let wage_inputted = parseInt(wage_input_element.value);
        let max_wage = js_vars.max_wage;
        var name_low_effort = js_vars.name_low_effort;
        var name_high_effort = js_vars.name_high_effort;
        if (isNaN(wage_inputted) || isNaN(effort_inputted)) {
            alert("Error: Please enter a number in both fields before sending offer.");
            return;
        } else if (wage_inputted < 0 || wage_inputted > max_wage) {
            alert("Error: Please specify a wage between 0 and " +  max_wage + ".");
            return;
        } else if (effort_inputted < 0 || effort_inputted > 1) {
            alert(`Error: Please choose either ${name_high_effort} or ${name_low_effort} effort.`);
            return;
        } else {
            let status = 'open';
            let my_id = js_vars.my_id;
            let currency_is_points = js_vars.currency_is_points;
            try {
            liveSend({
                "information_type": "offer",
                "employer_id": my_id,
                "wage": wage_inputted,
                "effort": effort_inputted,
                "status": status,
                "job_number": job_offer_number,
                "currency_is_points": currency_is_points,
            });
            } catch (err) {
                console.log('Error in sendOffer' + err);
            }
        }
        document.getElementById(`effort_input_${job_offer_number}`).value = "";
        document.getElementById(`wage_input_${job_offer_number}`).value = "";
    }