INSERT_SQL_STATEMENT = """
    INSERT INTO records(application_id, name, id_number, dob, loan_type, loan_tenure, loan_amount, result)
    VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
    """

SELECT_APPROVED_APPLICATIONS_SQL = """
    SELECT application_id, name, loan_type, loan_amount, result
    FROM records
    WHERE result = 'APPROVED'
    ORDER BY application_id DESC
    LIMIT %s
    """
