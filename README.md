# Helm chart for installing Tekton pipelines 

**This Helm chart is still in development**

> Copyright [2024] [Cogito Group Ltd]

[Cogito Group's](https://cogitogroup.co.uk) Tekton Helm chart to install CI/CD pipelines on Kubernetes with **one** command.

This repository contains a Helm chart and examples for installing Tekton pipelines on Kubernetes. The chart does not install the Tekton CRDs, you must install these separately, the chart is designed to be both platform and Kubernetes distribution agnostic.

Source repository https://github.com/cogitogroupltd/tekton-helm-chart



<!-- vscode-markdown-toc -->
* 1. [Summary](#Summary)
	* 1.1. [Features](#Features)
	* 1.2. [Successfully tested on](#Successfullytestedon)
	* 1.3. [Prerequisties](#Prerequisties)
* 2. [Install pipelines examples](#Installpipelinesexamples)
	* 2.1. [Example 1 - Clone, build and push docker image to ECR using Docker-in-docker](#Example1-ClonebuildandpushdockerimagetoECRusingDocker-in-docker)
	* 2.2. [Example 2 - Clone, build and push docker image to Dockerhub using Kaniko](#Example2-ClonebuildandpushdockerimagetoDockerhubusingKaniko)
	* 2.3. [Example 3 - Clone, build and push docker image to Dockerhub using Buildah](#Example3-ClonebuildandpushdockerimagetoDockerhubusingBuildah)
* 3. [Todo](#Todo)
* 4. [Troubleshooting](#Troubleshooting)

<!-- vscode-markdown-toc-config
	numbering=true
	autoSave=true
	/vscode-markdown-toc-config -->
<!-- /vscode-markdown-toc -->

##  1. <a name='Summary'></a>Summary

**This project is in development and should not be used in production**


###  1.1. <a name='Features'></a>Features

- Helm chart to deploy Tekton pipelines and all dependencies except Tekton Custom Resource Definitions
- Simplifies developer experience with automated Tekton resource linking  
- Declarative and immutable pipelines 
- Least-privilege with isolated permissions for each task run
- Create/Delete Github webhooks from inside Tekton
- Trigger pipelines from CronJob or Github webhook events


###  1.2. <a name='Successfullytestedon'></a>Successfully tested on

- AWS EKS version == v1.30
- OpenShift ROSA (OKD4) v1.28 - v1.30
- Openshift OKD3 - v1.28 - v1.30
- Kind [download](https://kind.sigs.k8s.io/) version == 1.30
- Microk8s version == v1.30
- Rancher K3s == v1.30
- Azure AKS == 1.30
- Google Kubernetes Engine (GKE)

###  1.3. <a name='Prerequisties'></a>Prerequisties

Before deploying the Helm chart the below steps are required:

- Kubernetes cluster >= v1.28, see [kind.md](./docs/kind.md).
- Kubectl > v1.25 [https://kubernetes.io/docs/tasks/tools/](https://kubernetes.io/docs/tasks/tools/). Only required to execute a `pipelineRun`.
- Helm > v3.0 [https://helm.sh/docs/intro/install/](https://helm.sh/docs/intro/install/). Required to deploy the Tekton pipelines in this Helm chart.
- Install Tekton, see [Installing Tekton](./docs/installing_tekton.md). Required dependency to deploy the Tekton pipelines in this Helm chart.

- SSH RSA Keypair linked with Github with **no passphrase**, see [Generate RSA](./docs/generate_rsa.md). Required for examples using git clone.
- AWSCli > v2.0 - Required to deploy the Tekton pipelines in this Helm chart.
- DockerHub username and password - required for examples using Dockerhub



See [prereqs.md](./docs/prereqs.md) for more information.

##  2. <a name='Installpipelinesexamples'></a>Install pipelines examples

Listed below are a series of examples of how to use the Helm chart to achieve common DevOps tasks. 


###  2.1. <a name='Example2-ClonebuildandpushdockerimagetoDockerhubusingKaniko'></a>Example 2 - Clone, build and push docker image to Dockerhub using Kaniko

See example [README.md](./examples/tekton-kaniko-build-deploy/README.md)

![](./examples/tekton-kaniko-build-deploy/2022-10-17-23-36-33.png)

###  2.2. <a name='Example3-ClonebuildandpushdockerimagetoDockerhubusingBuildah'></a>Example 3 - Clone, build and push docker image to Dockerhub using Buildah

See example [README.md](./examples/tekton-buildah-build-deploy/README.md)

![](./examples/tekton-buildah-build-deploy/2022-10-18-00-06-27.png)


###  2.3. <a name='Example1-ClonebuildandpushdockerimagetoECRusingDocker-in-docker'></a>Example 1 - Clone, build and push docker image to ECR using Docker-in-docker (not recommended)

Running docker-in-docker is not recommended due to security vulnerabilities and is only shown for demonstrational purposes.

See example [README.md](./examples/tekton-ecr-build-deploy/README.md)


![](./examples/tekton-ecr-build-deploy/2022-10-17-23-18-35.png)

##  3. <a name='Todo'></a>Todo

- [ ] Allow multiple installations of helm chart into same cluster; currently conflicts when ClusteRoles and ClusterRoleBindings are not unique
- [ ] Helm not correctly reconciling Task definition updates, despite 
- [ ] Remove hard coding in triggerTemplate by moving all built-in tasks to use an array same as calling a global custom task
- [ ] Add docs on taskPodTemplate vs podTemplate whereby a taskPodTemplate overrides the podTemplate
- [ ] Examples - Incorporate usage of eks.role.arn annotations to demonstrate easy utilisation of lease privilege
- [ ] Allow multiple installations of helm chart into same namespace; currently conflicts when task names are not unique
- [ ] Move resource defs from eventListener
- [ ] Remove dependency on cluster-admin ClusterRole by creating a new tekton-cluster-admin ClusterRole
- [ ] Documentation for Windows
- [ ] Auto generate dynamic \_taskRun.yaml for custom-task in helm output via Notes.txt
- [ ] Auto generate a dynamic \_pipelineRun.yaml for each pipeline in helm output via Notes.txt
- [ ] Add `taskcall[0].steps` to override `taskdefinition[0].steps` so that a developer can use the same task but have the steps overridden. This fix requires dynamic task creation in the background and hence post-pended GUID mapping.

More feature requests? Please raise a github [issue](https://github.com/cogitogroupltd/tekton-helm-chart/issues)

##  4. <a name='Troubleshooting'></a>Troubleshooting

See [FAQ.md](./docs/FAQ.md) or our [blog](https://cogitogroup.co.uk/blog)
