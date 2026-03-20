# PythonAsia 2026 Presentation Brief

## 1) Talk Theme

This repository demonstrates a practical multi-cloud architecture in Python where:

- AWS is the primary runtime cloud.
- GCP is the secondary/disaster-recovery cloud.
- The application can switch cloud context via a deployment flag.
- Data artifacts (approval letters) can be synced from AWS S3 to GCP GCS through a manual, on-demand pipeline.

The goal is to show enterprise-realistic trade-offs, not a perfect active-active setup.

---

## 2) Business Use Case

Loan decisioning platform with two services:

- `decision-service`: main orchestration service
- `credit-check-service`: external dependency for credit score

For approved applications, an approval letter PDF is stored in cloud object storage.

---

## 3) High-Level Architecture

### Application Layer

- `decision-service` (Flask):
  - accepts loan applications
  - calls credit-check service
  - stores decision data in PostgreSQL
  - generates and looks up approval letter artifacts in object storage
  - exposes dashboard/API for approved applications
- `credit-check-service` (Flask):
  - returns credit score for applicant details

### Data and Artifacts

- Database (Postgres):
  - source of truth for loan applications/decisions
- Object storage:
  - AWS S3 (primary artifact store)
  - GCP GCS (secondary artifact store)

### Infra

- AWS:
  - EKS, RDS, S3, VPC networking, IAM, OIDC provider, node groups
- GCP:
  - GKE, Cloud SQL, GCS, VPC/networking, Workload Identity

---

## 4) Cloud Switching Model

Cloud routing is controlled through:

- `DEPLOYMENT_PLATFORM=AWS|GCP`

Current app config reads this and selects cloud-specific infra endpoints.

Primary behavior:

- AWS is primary for runtime and data generation.
- GCP is secondary used for failover and recovered access.

---

## 5) Security Model (Key Talking Point)

### AWS Side

- IRSA model:
  - Kubernetes ServiceAccount -> OIDC trust -> IAM Role -> S3 permissions

### GCP Side

- Workload Identity model:
  - Kubernetes ServiceAccount -> GSA mapping -> GCS IAM permissions

Both avoid static cloud credentials in application pods.

---

## 6) Repo Structure (Important Folders)

- `decision-service/` -> main API, dashboard, DB/object-store logic, Kubernetes manifests
- `credit-check-service/` -> credit check API + deployment manifests
- `aws-infra/` -> AWS Terraform resources
- `gcp-infra/` -> GCP Terraform resources
- `aws-infra-bootstrap/` -> Terraform backend bootstrap (S3 state + DynamoDB lock)
- `.github/workflows/` -> infra/deploy/sync automation

---

## 7) Key APIs and UI

### Decision APIs

- `POST /api/v1/decision` -> runs decision flow
- `GET /api/v1/applications` -> approved-only applications with active-platform link status
- `GET /api/v1/dashboard` -> server-rendered table for demo visibility

### Health and Platform

- `GET /api/v1/health`
- `GET /api/v1/ready`
- `GET /api/v1/platform` -> shows current deployment platform and infra map

### Failure Simulation

- Header-driven simulated failure:
  - `X-FAILURE-MODE: true`
  - returns `503` with `SIMULATED_FAILURE` on key endpoints for demo failover narrative

---

## 8) Pipelines in GitHub Actions

### Infra Pipelines

- `infra-aws-bootstrap.yml`
  - creates Terraform backend resources (S3 bucket + DynamoDB lock table)
- `infra-aws.yml`
  - action input: `plan | apply | destroy`
  - two-job model: `plan` then environment-approved `apply/destroy`
  - uses remote state backend config
- `infra-gcp.yml`
  - action input: `plan | apply`
  - Terraform plan/apply for GCP stack

### App CD Pipeline

- `cd-deploy.yml`
  - deploys app manifests to EKS or GKE
  - selects cloud based on `decision-service/config.py` default platform
  - sets deployment env vars and DB host
  - runs Kubernetes DB migration job
  - updates image tags and waits for rollout

### Manual Sync Pipeline

- `sync-s3-to-gcs.yml`
  - on-demand only (`workflow_dispatch`)
  - reads approved application IDs from AWS DB
  - checks object existence in S3
  - copies missing artifacts to GCS
  - supports dry-run mode

---

## 9) Database Schema Automation

Originally schema creation was manual.

Now automated via Kubernetes Job:

- `decision-service/cd/db-migration-configmap.yaml`
- `decision-service/cd/db-migration-job.yaml`
- SQL source:
  - `decision-service/migrations/001_init_records.sql`

This runs during CD before app rollout, for both AWS and GCP deployment paths.

---

## 10) Demo Narrative (Recommended)

1. Show AWS as active platform (`/api/v1/platform`).
2. Submit approved decision request.
3. Show dashboard row and approval artifact behavior.
4. Trigger simulated AWS failure using `X-FAILURE-MODE: true`.
5. Trigger failover deployment to GCP via CD workflow.
6. Show platform switched to GCP.
7. Trigger manual sync workflow (`sync-s3-to-gcs`).
8. Show recovered artifact availability on GCP path.

---

## 11) Operational Trade-offs (Be Honest in Talk)

- This is primary-secondary DR, not active-active.
- Manual sync creates temporary inconsistency windows by design.
- This design favors operator control, low accidental cost, and clear auditability.
- Architecture is intentionally pragmatic and incrementally hardenable.

---

## 12) Known Constraints / Risks

- Cloud account quotas and billing state can block nodegroup launches.
- Terraform state must remain remote/persistent for reliable apply/destroy behavior.
- Some naming collisions can occur when reusing existing account resources; imports or unique naming may be required.

---

## 13) Secrets / Variables Expectations

### Secrets (sensitive)

- `AWS_ACCESS_KEY_ID`
- `AWS_SECRET_ACCESS_KEY`
- `GCP_SA_KEY`
- `DATABASE_PASSWORD`
- `TF_VAR_PYTHON_ASIA_DB_PASSWORD`

### Variables (non-sensitive)

- `AWS_DATABASE_HOST`
- `GCP_DATABASE_HOST`
- `AWS_TF_STATE_BUCKET`
- `AWS_TF_LOCK_TABLE`

---

## 14) Suggested Slide Storyline

1. Problem statement: multi-cloud reliability and blast-radius reduction
2. Architecture overview
3. Security identity model (IRSA vs GKE Workload Identity)
4. Infra automation model (bootstrap + infra + CD)
5. Live demo (normal -> failure -> failover -> sync)
6. Trade-offs and production hardening roadmap

---

## 15) Elevator Pitch (One Slide)

"We built a practical multi-cloud Python platform where AWS runs as primary, GCP runs as secondary, failover is controlled, sync is auditable, and security uses workload identities instead of static cloud keys."

