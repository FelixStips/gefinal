
    function cancelOffer(offer_cancelled) {
        let job_offer_number = parseInt(offer_cancelled.slice(-1));
        let cancel_job_id = parseInt(document.getElementById(`employer_job_id_offered_${job_offer_number}`).innerHTML);
        let cancel_employer_id = js_vars.my_id;
        liveSend({
            "information_type": "cancel",
            "employer_id": cancel_employer_id,
            "job_id": cancel_job_id,
            "job_number": job_offer_number,
        })
    }