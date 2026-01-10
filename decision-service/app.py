import logging
from flask import Flask
from api.decision_api import decision_api
from api.health_check_api import health_check_api

app=Flask(__name__)
logging.basicConfig(level=logging.DEBUG)

app.register_blueprint(decision_api,url_prefix="/api")
app.register_blueprint(health_check_api,url_prefix="/api")


if __name__=="__main__":
    app.run(host="0.0.0.0",debug=True,port=2212)