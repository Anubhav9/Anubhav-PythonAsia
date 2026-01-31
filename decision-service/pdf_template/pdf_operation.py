import logging

from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML
def generate_html_template(application_id,applicant_name,loan_type,loan_amount,loan_tenure):
    """
    Generates the Rendered HTML Template which later will be converted to PDF
    :param application_id : The ID of the applicant
    :param applicant_name: The name of the applicant
    :param loan_type: The type of loan the applicant is seeking for
    :param loan_amount: The amount of loan applicant is seeking for
    :param loan_tenure: The total tenure of the loan
    """
    env = Environment(loader=FileSystemLoader("."))
    template = env.get_template("pdf_template/loan-approved.html")

    html = template.render(
        customer_name=applicant_name,
        application_id=application_id,
        loan_type=loan_type,
        loan_tenure=loan_tenure,
        loan_amount=loan_amount
    )
    return html

def generate_pdf_from_rendered_html(application_id,applicant_name,loan_type,loan_amount,loan_tenure):
    """
    Generates the PDF from the rendered html template
    :param application_id: Application ID of the applicant
    :param applicant_name: Name of the applicant
    :param loan_type: Loan Type applicant is seeking for
    :param loan_amount: Loan Amount applicant is seeking for
    :param loan_tenure: Tenure of the loan
    :return: A PDF output which will be stored in the bucket in format of ApplicationID_Report.pdf
    """
    html=generate_html_template(application_id,applicant_name,loan_type,loan_amount,loan_tenure)
    logging.info(f"[PDF Report Generation]: PDF report for application id {application_id} has been generated")
    return HTML(string=html).write_pdf()

