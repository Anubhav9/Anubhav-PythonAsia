import logging
import boto3
from botocore.exceptions import ClientError
from google.cloud import storage
from interface import create_and_get_infra_details_map
from pdf_template.pdf_operation import generate_pdf_from_rendered_html
from urllib.parse import quote
import config


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


def _get_report_key(application_id):
    return f"reports/{application_id}_approval_report.pdf"


def _aws_object_exists(bucket_name, key_name):
    s3 = boto3.client("s3")
    try:
        s3.head_object(Bucket=bucket_name, Key=key_name)
        return True
    except ClientError as err:
        error_code = err.response.get("Error", {}).get("Code", "")
        if error_code in {"404", "NoSuchKey", "NotFound"}:
            return False
        logging.error(f"[Object Store]: AWS head_object failed for key {key_name}. Error is {err}")
        return False
    except Exception as e:
        logging.error(f"[Object Store]: AWS head_object unexpected error for key {key_name}. Error is {e}")
        return False


def _gcp_object_exists(bucket_name, key_name):
    try:
        client = storage.Client()
        bucket = client.bucket(bucket_name)
        blob = bucket.blob(key_name)
        return blob.exists(client)
    except Exception as e:
        logging.error(f"[Object Store]: GCP blob exists check failed for key {key_name}. Error is {e}")
        return False


def _build_console_url(platform, bucket_name, key_name):
    encoded_key = quote(key_name, safe="")
    if platform == "AWS":
        return f"https://s3.console.aws.amazon.com/s3/object/{bucket_name}?region={config.AWS_REGION}&prefix={encoded_key}"
    if platform == "GCP":
        return (
            f"https://console.cloud.google.com/storage/browser/_details/"
            f"{bucket_name}/{encoded_key}?project={config.GCP_PROJECT_ID}"
        )
    return None


def get_active_platform_report_details(application_id):
    """
    For a given application, return approval-letter details for active deployment platform only.
    """
    infra_details_map = create_and_get_infra_details_map()
    deployment_platform = infra_details_map.get("deployment_platform")
    bucket_name = infra_details_map.get("object_store_name")
    key_name = _get_report_key(application_id)

    exists = False
    if deployment_platform == "AWS":
        exists = _aws_object_exists(bucket_name, key_name)
    elif deployment_platform == "GCP":
        exists = _gcp_object_exists(bucket_name, key_name)

    return {
        "platform": deployment_platform,
        "key": key_name,
        "exists": exists,
        "url": _build_console_url(deployment_platform, bucket_name, key_name) if exists else None,
    }


