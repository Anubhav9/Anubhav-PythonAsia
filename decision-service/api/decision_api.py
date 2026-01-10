import logging
from flask import Blueprint, request, jsonify
from services import decision_logic
from integration import credit_check_integration
import uuid
from repositories import users_repository
import utils
from datetime import datetime


decision_api=Blueprint("decision_api",__name__)

@decision_api.route("/v1/decision",methods=["POST"])
def invoke_decision():
    """
    API Method to invoke decision service
    :return: Whether user is eligible for a loan or not.
    """
    name=request.json.get("name")
    id_number=request.json.get("id_number")
    dob=request.json.get("dob")
    loan_type=request.json.get("loan_type")
    loan_amount=int(request.json.get("loan_amount"))
    loan_tenure=int(request.json.get("loan_tenure"))
    application_id = uuid.uuid4()

    required_parameters=["name","id_number","dob","loan_type","loan_amount","loan_tenure"]
    for i in required_parameters:
        result=decision_logic.check_if_info_not_supplied(i)
        if result == -1:
            response={f"message:{i} cannot be empty"}
            return jsonify(response),400
        elif result == 1:
            continue
    result_credit_check=credit_check_integration.invoke_credit_check_service(name,id_number,dob)
    if result_credit_check==-1:
        response={f"message:Something went wrong"}
        return jsonify(response),200
    result_decision_logic= decision_logic.check_conditional_approval(result_credit_check,loan_amount,loan_tenure)
    dob = datetime.strptime(dob, "%d-%m-%Y").date()
    if result_decision_logic==1:
        logging.info(f"[Business Logic Result]: Loan is approved for user")
        final_response = {"message": "Loan is conditionally approved"}
        username,password=utils.get_creds_for_db()
        result_insert_into_db=users_repository.insert_user_record_to_database(str(application_id),username,password,name,id_number,dob,loan_type,loan_tenure,loan_amount,"APPROVED")
        if result_insert_into_db==-1:
            logging.error(f"[Business Logic Result]: Insertion into database has failed for user with application_id {application_id}")
        return jsonify(final_response),200
    if result_decision_logic==-1:
        logging.info(f"[Business Logic Result]: Loan is not approved for user")
        username,password=utils.get_creds_for_db()
        result_insert_into_db=users_repository.insert_user_record_to_database(str(application_id),username,password,name,id_number,dob,loan_type,loan_tenure,loan_amount,"DECLINED")
        if result_insert_into_db == -1:
            logging.error(
                f"[Business Logic Result]: Insertion into database has failed for user with application_id {application_id}")
        final_response = {"message": "Loan is not approved"}
        return jsonify(final_response), 200






