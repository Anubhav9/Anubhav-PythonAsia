
from flask import Blueprint, request, jsonify
import random
from datetime import datetime

credit_check_api=Blueprint("credit_check_api",__name__)

@credit_check_api.route("/v1/credit-check",methods=["POST"])
def invoke_credit_check():
    print("Credit Check request invoked")
    name=request.json.get("name")
    id_number=request.json.get("id_number")
    dob=request.json.get("dob")

    print(f"Name received is {name}")
    print(f"ID Number received is {id_number}")
    print(f"DOB received is {dob}")

    if(name is None):
        response={"message":"Name cannot be empty"}
        return jsonify(response),400
    if(id_number is None):
        response = {"message": "ID Number cannot be empty"}
        return jsonify(response), 400
    if(dob is None):
        response = {"message": "Date of Birth cannot be empty"}
        return jsonify(response), 400

    credit_score=random.randint(600,950)
    last_refreshed_date=datetime.now().strftime("%d-%m-%Y")
    response={
        "credit_score":credit_score,
        "last_refreshed_date":last_refreshed_date
    }
    return jsonify(response),200
