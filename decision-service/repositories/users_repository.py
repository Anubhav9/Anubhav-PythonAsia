import logging
from db.connection import connect_to_database
import repositories.constants as constants


def insert_user_record_to_database(application_id, username, password,
                                  name, id_number, dob,
                                  loan_type, loan_tenure, loan_amount, decision):
    """
    Helper function to insert data to the records table
    :param application_id: Application ID of the applicant
    :param username: username for the database
    :param password: password for the database
    :param name: name of the applicant
    :param id_number: ID number for the applicant
    :param dob: Date of Birth for the applicant
    :param loan_type: The type of loan applicant is seeking for
    :param loan_tenure: The tenure of the loan
    :param loan_amount: The amount, the applicant is seeking for
    :param result: Result - whether the loan for the applicant is approved or not
    :return: 1, if the data is successfully inserted to the records table. -1 if there is an exception and insertion is not successful
    """

    result,conn_object = connect_to_database(username,password)
    if result==-1:
        logging.error(f"[Database Insertion Operation]: Database Insertion cannot be performed")
        return -1
    try:
        conn_object.autocommit = True
        cursor = conn_object.cursor()
        logging.debug(f"[Database Insertion Operation]: Basic Hygiene Check is being performed")
        cursor.execute("select current_database(), current_schema()")
        logging.debug(f"[Database Insertion Operation]: {cursor.fetchone()}")
        logging.debug(f"[Database Insertion Operation]: Inserting the actual data now")
        cursor.execute(constants.INSERT_SQL_STATEMENT, (
        application_id, name, id_number, dob,
        loan_type, loan_tenure, str(loan_amount), decision
        ))
        logging.info(f"[Database Insertion Operation]: Data in the records table has been inserted")
        cursor.close()
        conn_object.close()
        return  1
    except Exception as e:
        logging.error(f"[Database Insertion Operation]: Failure: Insertion to records table is not successful. Exception is {e}")
        cursor.close()
        conn_object.close()
        return -1


def fetch_approved_applications(username, password, limit=50):
    """
    Fetch latest approved applications from records table.
    :return: list of records or empty list on failure.
    """
    result, conn_object = connect_to_database(username, password)
    if result == -1:
        logging.error("[Database Read Operation]: Could not connect to database")
        return []

    cursor = conn_object.cursor()
    try:
        cursor.execute(constants.SELECT_APPROVED_APPLICATIONS_SQL, (limit,))
        rows = cursor.fetchall()
        response = []
        for row in rows:
            response.append(
                {
                    "application_id": str(row[0]),
                    "name": row[1],
                    "loan_type": row[2],
                    "loan_amount": row[3],
                    "decision": row[4],
                }
            )
        return response
    except Exception as e:
        logging.error(f"[Database Read Operation]: Failed to fetch approved records. Exception is {e}")
        return []
    finally:
        cursor.close()
        conn_object.close()