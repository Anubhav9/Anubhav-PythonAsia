from flask import Blueprint, request, jsonify
import utils
import interface


health_check_api=Blueprint("health_check_api",__name__)

@health_check_api.route("/v1/health",methods=["GET"])
def invoke_health_check():
    """
    Health Check URL for Decision Service
    :return: Status code 200 if service is up and running.
    """
    if utils.is_failure_mode_enabled(request):
        response = {
            "status": "SIMULATED_FAILURE",
            "message": "Failure mode enabled via X-FAILURE-MODE header",
        }
        return jsonify(response), 503

    response={"status":"UP"}
    return jsonify(response), 200

@health_check_api.route("/v1/ready",methods=["GET"])
def invoke_readiness_check():
    """
    Readiness Check for Database Service
    :return: Status code 200 if all external dependencies are functional. 503 if external dependency is not ready or not reachable
    """
    if utils.is_failure_mode_enabled(request):
        response = {
            "status": "SIMULATED_FAILURE",
            "message": "Failure mode enabled via X-FAILURE-MODE header",
        }
        return jsonify(response), 503

    credit_check_service_health_result=utils.health_check_call_to_credit_check_service()
    database_health_check_result=utils.health_check_for_db_service()
    final_result = credit_check_service_health_result*database_health_check_result
    if final_result==1:
        response = {"status": "READY"}
        return jsonify(response),200
    else:
        response = {"status": "NOT READY"}
        return jsonify(response),503


@health_check_api.route("/v1/platform", methods=["GET"])
def get_platform_details():
    """
    Demo endpoint to show active cloud routing context.
    :return: current deployment platform and resolved infra details.
    """
    current_platform = interface.get_current_deployment_platform()
    if current_platform == "INVALID":
        return jsonify(
            {
                "status": "INVALID",
                "message": "Unsupported DEPLOYMENT_PLATFORM value. Allowed values: AWS, GCP",
            }
        ), 400

    infra_details_map = interface.create_and_get_infra_details_map()
    return jsonify({"status": "OK", "infra": infra_details_map}), 200


