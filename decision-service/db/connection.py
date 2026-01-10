import logging
import config
import interface
import psycopg2


def connect_to_database(username,password):
    """
    Helper function to establish connection with the database
    :param username: username to connect to database
    :param password: password corresponding to the provided username
    :return: result (1/-1) and conn object - conn object only returned if successful, otherwise None
    """
    logging.debug(f"[Database Operation]: The current deployment platform being set is: {config.deployment_platform}")
    all_details_details = interface.create_and_get_infra_details_map()
    database_host = all_details_details["database_host"]
    logging.debug(f"[Database Operation]: The current Database URL being used is: {database_host}")
    if database_host is None:
        logging.error(f"[Database Operation]: FATAL - Either empty URL for Database is received or URL might be invalid")
        return -1,None
    try:
        conn = psycopg2.connect(
            dbname="postgres",   # confirm this is the DB you want
            user=username,
            password=password,
            host=database_host,
            port=5432,
            connect_timeout=10
        )
        conn.autocommit = True
        return 1,conn
    except Exception as e:
        logging.error(f"[Database Operation]: The connection with the database could not be established. The exception occoured is {e}")
        return -1,None

def ping_database(username,password):
    """
    Helper function to do health check for the database
    :param username: username to connect to the database
    :param password: password corresponding to the provided username
    :return: 1/-1 - corresponding to health check success / failure
    """
    result,conn_object=connect_to_database(username,password)
    if(result==1):
        logging.debug(f"[Database Operation]: Database seems to be connected")
        sql_statemet="SELECT 1;"
        cursor = conn_object.cursor()
        try:
            cursor.execute(sql_statemet)
            cursor.fetchone()
            logging.info(f"[Database Operation]: The DB is connected and reachable")
            return 1
        except Exception as e:
            logging.error(f"[Database Operation]:The Database is connected but health check resulted in failure. Exception is {e}")
            return -1