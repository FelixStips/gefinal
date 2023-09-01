        function updateInfobox(market_information) {
            let {workers_left, open_offers, average_wage_tokens, average_wage_points, average_effort} = market_information;
            document.getElementById("workers_left").innerHTML = workers_left;
            document.getElementById("offers_left").innerHTML = open_offers;
            let share_standard = average_effort * 100;
            document.getElementById("average_effort").innerHTML = share_standard.toFixed(0);
            if (document.getElementById("average_wage_tokens")) {
                document.getElementById("average_wage_tokens").innerHTML = average_wage_tokens.toFixed(1);
            } else if (document.getElementById("average_wage_points")) {
                document.getElementById("average_wage_points").innerHTML = average_wage_points.toFixed(1);
            } else {
                console.log("no average_wage_tokens")
            }
        }