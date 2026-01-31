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