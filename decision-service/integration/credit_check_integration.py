import os
import requests
import constants
import logging


def invoke_credit_check_service(name,id_number,dob):
    CREDIT_CHECK_URL = os.getenv("CREDIT_CHECK_URL", "localhost:2112")
    COMPLETE_REQUEST_URL=f"http://{CREDIT_CHECK_URL}:2112{constants.CREDIT_CHECK_ENDPOINT}"
    request_body={
        "name": name,
        "id_number": id_number,
        "dob": str(dob)
    }
    custom_header={
        "Content-Type": "application/json"
    }

    logging.debug(f"Checking error - request body is {request_body}")

    response = requests.post(url=COMPLETE_REQUEST_URL, headers=custom_header, json=request_body)
    if response.status_code==200:
        credit_score=response.json()["credit_score"]
        logging.debug(f"[Response from Credit Check Service]: Credit Score of the user is {credit_score}")
        return int(credit_score)
    else:
        logging.error(f"[Response from Credit Check Service]: Credit Check Service had an error status code : {response.status_code}")
        return -1
