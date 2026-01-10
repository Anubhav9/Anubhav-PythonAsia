from flask import Flask, request, jsonify
import random
from datetime import datetime
from api.credit_check_api import  credit_check_api
from api.health_check_api import health_check_api

app=Flask(__name__)
app.register_blueprint(credit_check_api,url_prefix="/api")
app.register_blueprint(health_check_api,url_prefix="/api")

if __name__=="__main__":
    app.run(host="0.0.0.0",debug=True,port=2112)