from flask import Blueprint, jsonify

health_check_api=Blueprint("health_check_api",__name__)

@health_check_api.route("/v1/health",methods=["GET"])
def invoke_health_endpoint():
    response={"status":"UP"}
    return jsonify(response),200