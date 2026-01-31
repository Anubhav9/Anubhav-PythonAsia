import os
import requests
import constants
import interface
from db import connection


def health_check_call_to_credit_check_service():
    """
    Helper function to check if the Credit Check Service is up and running or not. Used for K8s readiness probe
    :return:
    """
    CREDIT_CHECK_SERVICE_URL=os.getenv("CREDIT_CHECK_URL","localhost:2112")
    COMPLETE_URL=f"http://{CREDIT_CHECK_SERVICE_URL}:2112{constants.HEALTH_CHECK_ENDPOINT}"
    custom_headers = {
        "Content-Type": "application/json"
    }
    response_from_services = requests.get(url=COMPLETE_URL,headers=custom_headers)
    if response_from_services.status_code==200:
        return 1
    else:
        return -1

def health_check_for_db_service():
    username,password= get_creds_for_db()
    database_host=interface.create_and_get_infra_details_map()["database_host"]
    result=connection.ping_database(username,password)
    return result



def get_creds_for_db():
    """
    DB creds being fetched as env variables
    :return: database username and password
    """
    db_username=os.getenv("DATABASE_USERNAME","root")
    db_password=os.getenv("DATABASE_PASSWORD","password123")
    return db_username,db_password