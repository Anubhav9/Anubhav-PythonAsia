# Anubhav-PythonAsia
All Files for presenting at PythonAsia2026

### Multi-cloud switch (demo flag)
`decision-service` can switch infra targets by changing one env flag:

- `DEPLOYMENT_PLATFORM=AWS` -> uses `AWS_DATABASE_HOST` and AWS object-store path
- `DEPLOYMENT_PLATFORM=GCP` -> uses `GCP_DATABASE_HOST` and GCP object-store path

Example local run:

`DEPLOYMENT_PLATFORM=AWS python3 decision-service/app.py`

`DEPLOYMENT_PLATFORM=GCP python3 decision-service/app.py`

Demo visibility endpoint:

`GET /api/v1/platform` -> returns active platform and resolved infra map.

### Manual Tasks - That needs to be revisited layer
i) SG to RDS from EKS Cluster is currently manaully added

ii) Ingress open to public node in EKS cluster ie editing inbound SG rule is manually added.

iii) Since we are using NodeSelector put nodes in public and private nodes, labels on the nodes are manually added.

iv) Database Schema Creation is manually done.
