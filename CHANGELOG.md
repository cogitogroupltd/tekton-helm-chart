# Changelog

All notable changes to the Tekton Helm Chart will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Changed
- Enhanced SEO optimization for better discoverability
- Improved Chart.yaml metadata with comprehensive keywords
- Updated README.md with keyword-rich content structure

## [0.5.2] - 2024-06-10

### Features
- Helm chart to deploy Tekton pipelines and all dependencies except Tekton CRDs
- Automated Tekton resource linking for simplified developer experience
- Declarative and immutable Tekton pipeline definitions
- Least-privilege RBAC with isolated permissions for each task run
- GitHub webhook creation and deletion from within Tekton
- Pipeline triggers via CronJob or GitHub webhook events

### Platform Support
- CPU Architectures: ARM64 (MacM1, MacM2), AMD64
- AWS EKS v1.30
- OpenShift ROSA (OKD4) v1.28 - v1.30
- OpenShift OKD3 v1.28 - v1.30
- Kind v1.29, v1.30
- MicroK8s v1.30
- Rancher K3s v1.30
- Azure AKS v1.30
- Google Kubernetes Engine (GKE)

### Examples
- Kaniko container build pipeline
- Buildah container build pipeline
- Docker-in-Docker pipeline (educational)

### Documentation
- Installation prerequisites guide
- Tekton installation instructions
- RSA key generation guide
- FAQ and troubleshooting
- Kind cluster setup guide

## [0.5.1] - 2024-XX-XX

### Added
- Initial public release of Tekton Helm Chart
- Basic Tekton pipeline deployment support

## Future Plans

### Planned Enhancements
- Multiple installations in same cluster with unique ClusterRoles
- Improved Helm reconciliation for Task definition updates
- Remove hard coding in triggerTemplate
- Enhanced documentation for taskPodTemplate vs podTemplate
- Examples with EKS role ARN annotations
- Multiple installations in same namespace support
- Dynamic resource definitions for eventListener
- Windows documentation
- Auto-generated taskRun.yaml and pipelineRun.yaml
- Step override support for task calls

---

For more details, see the [GitHub repository](https://github.com/cogitogroupltd/tekton-helm-chart) or raise an [issue](https://github.com/cogitogroupltd/tekton-helm-chart/issues).
