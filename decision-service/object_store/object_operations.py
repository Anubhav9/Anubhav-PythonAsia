import logging
import boto3
from google.cloud import storage
from interface import create_and_get_infra_details_map
from pdf_template.pdf_operation import generate_pdf_from_rendered_html


def insert_into_object_store(application_id,applicant_name,loan_type,loan_amount,loan_tenure):
    infra_details_map=create_and_get_infra_details_map()
    deployment_platform=infra_details_map.get("deployment_platform")
    bucket_host=infra_details_map.get("object_store_host")
    bucket_name=infra_details_map.get("object_store_name")
    html_report = generate_pdf_from_rendered_html(application_id, applicant_name, loan_type, loan_amount, loan_tenure)
    key_name = f"reports/{application_id}_approval_report.pdf"
    match deployment_platform:
        case "AWS":
            logging.debug(f"[Object Store]: The current deployment platform is AWS")
            logging.debug(f"[Object Store]: Since current deployment platform is AWS, proceeding to use boto3")
            s3=boto3.client("s3")

            try:
                s3.put_object(Body=html_report,ContentType="application/pdf",Bucket=bucket_name,Key=key_name)
                logging.info(f"[Object Store]: With deployment platform set to AWS, the report has been uploaded to the bucket")
                return True
            except Exception as e:
                logging.error(f"[Object Store]: With deployment platform set to AWS, an error occured while uploading the approval to report to the bucket. Error is {e}")
                return False
        case "GCP":
            logging.debug(f"[Object Store]: The current deployment platform is GCP")
            logging.debug(f"[Object Store]: Since the current deployment platform is GCP, proceeding to use GCS Library")
            client = storage.Client()
            bucket = client.bucket(bucket_name)
            blob = bucket.blob(key_name)
            try:
                blob.upload_from_string(html_report,content_type="application/pdf")
                logging.info(f"[Object Store]: With deployment platform set to GCP, the report has been uploaded to the bucket")
                return True
            except Exception as e:
                logging.error(f"[Object Store]: With deployment platform set to GCP, an error occured while uploading the approval to report to the bucket. Error is {e}")
                return False


