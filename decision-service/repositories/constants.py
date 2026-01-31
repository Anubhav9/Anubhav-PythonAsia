INSERT_SQL_STATEMENT = """
    INSERT INTO records(application_id, name, id_number, dob, loan_type, loan_tenure, loan_amount, result)
    VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
    """
