import logging
import services.constants as constants

def check_if_loan_type_valid(loan_type):
    """
    Helper function to check if loan type is within the valid types or not
    :param loan_type: loan type supplied by user
    :return: 1, if valid -1,otherwise
    """
    logging.debug(f"[Business Logic Validation]: Loan Type supplied is: {loan_type} ")
    valid_loan_types=[constants.LOAN_TYPE_CAR_LOAN,constants.LOAN_TYPE_HOME_LOAN,constants.LOAN_TYPE_PERSONAL_LOAN]
    if loan_type not in valid_loan_types:
        logging.error(f"[Business Logic Validation]: Loan type supplied is Invalid")
        return -1
    return 1

def check_if_info_not_supplied(parameter):
    """
    Helper function to check if a required field is not empty
    :param parameter: parameter for whom we need to check if the field is empty
    :return: 1-if field is not empty , -1-if field is empty
    """
    if parameter is None:
        logging.error(f"[Business Logic Validation] {parameter} cannot be None")
        return -1
    return 1

def check_conditional_approval(credit_score,loan_amount,tenure):
    """
    Helper function for business logic. All rules needs to go in here
    :param credit_score: Credit score of the applicant
    :param loan_amount: Loan amount of the applicant
    :param tenure: Tenure of the applicant
    :return: 1, if loan is conditionally approved. -1, if loan is not approved
    """
    if(credit_score>750 and loan_amount<500000 and tenure<5 ):
        logging.debug(f"[Business Logic Result]: Loan is conditionally approved")
        return 1
    else:
        logging.debug(f"[Business Logic Result]: Loan is not approved")
        return -1
