import logging
from flask import Blueprint, request, jsonify, render_template
from services import decision_logic
from integration import credit_check_integration
import uuid
from repositories import users_repository
from object_store import object_operations
import utils
from datetime import datetime
import interface


decision_api=Blueprint("decision_api",__name__)


def _fetch_approved_applications_with_active_links(limit):
    username, password = utils.get_creds_for_db()
    approved_applications = users_repository.fetch_approved_applications(username, password, limit)
    current_platform = interface.get_current_deployment_platform()
    response_items = []
    for item in approved_applications:
        report_details = object_operations.get_active_platform_report_details(item["application_id"])
        response_items.append(
            {
                "application_id": item["application_id"],
                "name": item["name"],
                "loan_type": item["loan_type"],
                "loan_amount": item["loan_amount"],
                "decision": item["decision"],
                "approval_letter_url": report_details["url"],
                "approval_letter_status": "AVAILABLE" if report_details["exists"] else "NOT_SYNCED",
                "approval_letter_key": report_details["key"],
            }
        )
    return current_platform, response_items

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


@decision_api.route("/v1/applications", methods=["GET"])
def list_approved_applications():
    """
    API method to fetch approved applications with active-platform approval links.
    """
    limit_value = request.args.get("limit", default=50, type=int)
    limit = max(1, min(limit_value, 200))
    current_platform, response_items = _fetch_approved_applications_with_active_links(limit)
    return jsonify(
        {
            "deployment_platform": current_platform,
            "count": len(response_items),
            "items": response_items,
        }
    ), 200


@decision_api.route("/v1/dashboard", methods=["GET"])
def render_dashboard():
    """
    Render an operator dashboard for approved applications and active-platform links.
    """
    limit = request.args.get("limit", default=50, type=int)
    limit = max(1, min(limit, 200))
    current_platform, response_items = _fetch_approved_applications_with_active_links(limit)
    return render_template(
        "dashboard.html",
        deployment_platform=current_platform,
        applications=response_items,
    )






