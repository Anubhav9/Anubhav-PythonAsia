from flask import Blueprint, request, jsonify
import utils


health_check_api=Blueprint("health_check_api",__name__)

@health_check_api.route("/v1/health",methods=["GET"])
def invoke_health_check():
    """
    Health Check URL for Decision Service
    :return: Status code 200 if service is up and running.
    """
    response={"status":"UP"}
    return jsonify(response), 200

@health_check_api.route("/v1/ready",methods=["GET"])
def invoke_readiness_check():
    """
    Readiness Check for Database Service
    :return: Status code 200 if all external dependencies are functional. 503 if external dependency is not ready or not reachable
    """
    credit_check_service_health_result=utils.health_check_call_to_credit_check_service()
    database_health_check_result=utils.health_check_for_db_service()
    final_result = credit_check_service_health_result*database_health_check_result
    if final_result==1:
        response = {"status": "READY"}
        return jsonify(response),200
    else:
        response = {"status": "NOT READY"}
        return jsonify(response),503


