
    function noMoreOffers() {
        //console.log(document.getElementById('employer_accepted_1').style.display);
        //console.log(document.getElementById('employer_accepted_2').style.display);

        let job1_open = (document.getElementById('employer_accepted_1').style.display === "block") ? 0 : 1;
        let job2_open = (document.getElementById('employer_accepted_2').style.display === "block") ? 0 : 1;
        let jobs_open = job1_open + job2_open
        try {
            liveSend({
                "information_type": "done",
                "employer_id": js_vars.my_id,
                "jobs_open" : jobs_open,
            })
        }
        catch (err) {
            console.log('Error in noMoreOffers' + err);
        }
    }
