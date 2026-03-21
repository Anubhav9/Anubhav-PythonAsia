# From Config to Cloud : A Pythonic Approach to Platform Independent Design

This repository contains the demo application and infrastructure used to present a practical multi-cloud Python architecture at PythonAsia 2026.

The core idea is simple:

- run the same application stack on AWS and GCP
- keep cloud-specific infrastructure behind a small runtime switch
- use AWS as the primary cloud
- use GCP as the secondary / failover cloud
- show the trade-offs of stateful failover honestly instead of pretending this is magic

## What This Repo Demonstrates

The demo models a small loan processing system with two Python services:

- `decision-service`: the main application users talk to
- `credit-check-service`: an internal dependency used during loan evaluation

When a loan is approved:

- a record is written to PostgreSQL
- an approval letter PDF is generated
- the PDF is stored in cloud object storage

The app can then be deployed on either AWS or GCP and show the active platform through API and UI endpoints.

## Multi-Cloud Design

Cloud selection is controlled by one runtime setting:

- `DEPLOYMENT_PLATFORM=AWS`
- `DEPLOYMENT_PLATFORM=GCP`

`decision-service` reads this value and resolves:

- which database host to use
- which object store to use
- which platform metadata to show in the demo

Current operating model:

- AWS is the primary runtime
- GCP is the secondary runtime
- approval letter artifacts can be synced from AWS S3 to GCP GCS through a manual pipeline

This is a primary-secondary disaster recovery style setup, not active-active.

## Main Application Features

`decision-service` exposes:

- `POST /api/v1/decision`
- `GET /api/v1/health`
- `GET /api/v1/ready`
- `GET /api/v1/platform`
- `GET /api/v1/applications`
- `GET /api/v1/dashboard`

Notable demo features:

- runtime platform visibility through `/api/v1/platform`
- approved-applications dashboard through `/api/v1/dashboard`
- object-store link resolution based on the active platform only
- header-based failure simulation using `X-FAILURE-MODE: true`

## Repo Structure

```text
.
├── decision-service/            # Main Flask app, dashboard, DB access, object storage, K8s manifests
├── credit-check-service/        # Supporting Flask service used during loan evaluation
├── aws-infra/                   # Terraform for AWS: VPC, EKS, RDS, S3, IAM, OIDC/IRSA
├── aws-infra-bootstrap/         # Terraform bootstrap for AWS remote state backend
├── gcp-infra/                   # Terraform for GCP: VPC, GKE, Cloud SQL, GCS, Workload Identity
├── .github/workflows/           # Infra, deploy, and sync workflows
├── PRESENTATION_BRIEF.md        # Speaker-oriented presentation notes
└── README.md                    # Repo overview
```

## Key Folders

### `decision-service/`

Contains the core business application:

- Flask API routes
- DB repository layer
- object-store integration for S3/GCS
- PDF generation
- dashboard template
- Kubernetes deployment manifests

Important files:

- `decision-service/config.py`
- `decision-service/interface.py`
- `decision-service/api/decision_api.py`
- `decision-service/api/health_check_api.py`
- `decision-service/object_store/object_operations.py`
- `decision-service/templates/dashboard.html`

### `credit-check-service/`

Simple support service used by `decision-service` to simulate an upstream dependency during loan evaluation.

### `aws-infra/`

Terraform for the AWS deployment path:

- VPC and subnets
- EKS cluster and node groups
- RDS PostgreSQL
- S3 bucket
- IAM roles and IRSA/OIDC wiring

### `gcp-infra/`

Terraform for the GCP deployment path:

- VPC and subnet
- Cloud NAT and router
- GKE cluster and node pools
- Cloud SQL PostgreSQL
- GCS bucket
- Workload Identity and GSA bindings

### `.github/workflows/`

Automation used for both infra and application operations:

- `infra-aws-bootstrap.yml`
- `infra-aws.yml`
- `infra-gcp.yml`
- `cd-deploy.yml`
- `sync-s3-to-gcs.yml`

## Deployment Model

### Application Deploy

`cd-deploy.yml`:

- reads the default deployment platform from `decision-service/config.py`
- connects to EKS or GKE
- applies Kubernetes manifests
- injects database and platform environment variables
- runs a DB migration job
- updates service image tags
- waits for rollout completion

### Infrastructure Deploy

Infra is managed separately for each cloud:

- `infra-aws.yml` for AWS
- `infra-gcp.yml` for GCP

Both are designed around manual `plan` / `apply` style execution so the demo remains operator-controlled.

### Artifact Sync

`sync-s3-to-gcs.yml` performs manual synchronization of approved-loan PDFs:

- reads approved application IDs from the AWS side
- checks whether the corresponding objects exist in GCS
- copies only missing artifacts

## Security Model

This repo intentionally demonstrates keyless cloud access from Kubernetes pods.

### AWS

- Kubernetes ServiceAccount
- OIDC trust
- IAM Role for Service Accounts (IRSA)
- S3 permissions on the assumed role

### GCP

- Kubernetes ServiceAccount
- Google Service Account (GSA)
- Workload Identity binding
- GCS IAM roles on the GSA

This avoids putting static cloud credentials inside application containers.

## Demo Flow

A simple live demo path is:

1. Deploy the app on AWS
2. Submit a loan request
3. Show approval and generated artifact
4. Show `/api/v1/platform`
5. Show `/api/v1/dashboard`
6. Trigger simulated AWS failure with `X-FAILURE-MODE: true`
7. Deploy the same app to GCP
8. Sync missing approval letters from S3 to GCS
9. Show the same dashboard flow on GCP

## Important Trade-Offs

This repo is intentionally honest about multi-cloud complexity:

- stateful failover is harder than stateless failover
- artifact sync is manual by design in order to keep control and cost predictable
- AWS and GCP networking models are not identical
- “same architecture” across clouds still requires cloud-specific IAM and infra patterns

