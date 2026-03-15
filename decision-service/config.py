import os

# Runtime cloud selector for multi-cloud demos.
deployment_platform = os.getenv("DEPLOYMENT_PLATFORM", "AWS")

# Infra endpoints can be injected at runtime, keeping defaults for local/demo use.
AWS_DATABASE_HOST = os.getenv("AWS_DATABASE_HOST", "")
GCP_DATABASE_HOST = os.getenv("GCP_DATABASE_HOST", "")
AWS_OBJECT_STORE_URL = os.getenv("AWS_OBJECT_STORE_URL", "")
GCP_OBJECT_STORE_URL = os.getenv("GCP_OBJECT_STORE_URL", "")
OBJECT_STORE_NAME = os.getenv("OBJECT_STORE_NAME", "approval-letters-python-asia-2026-demo")
AWS_REGION = os.getenv("AWS_REGION", "ap-northeast-1")
GCP_PROJECT_ID = os.getenv("GCP_PROJECT_ID", "pythonasia-v1")
