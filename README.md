# Helm chart for installing Tekton pipelines
<!-- vscode-markdown-toc -->
1. [Todo](#Todo)
2. [Summary:](#Summary:)
	* 2.1. [PreRequisties:](#PreRequisties:)
	* 2.2. [Install Tekton](#InstallTekton)
3. [Example pipeline installation](#Installpipelinesexamples)

<!-- vscode-markdown-toc-config
	numbering=true
	autoSave=true
	/vscode-markdown-toc-config -->
<!-- /vscode-markdown-toc -->

[Cogito Group's](https://cogitogroup.co.uk) cloud agnostic and generic Tekton Helm chart to install DevOps pipelines ontop of Kubernetes with **one** command. 

Source repository https://github.com/cogitogroupltd/tekton-helm-chart

See `raw-output.yaml` files for example outputted Kubernetes YAML and example command used to generate.



##  1. <a name='Todo'></a>Todo
- Create Incubator project https://github.com/helm/community/blob/main/incubator.md
- Remove hard coding in triggerTemplate by moving all built-in tasks to use an array same as calling a global custom task
- Add docs on taskPodTemplate vs podTemplate whereby a taskPodTemplate overrides the podTemplate
- Examples - Incorpoate usage of eks.role.arn annotations to demonstrate easy utilisation of lease privilege 
- Allow multiple installations of helm chart into same namespace; currently conflicts when task names are not unique
- Move resource defs from eventListener
- Remove dependency on cluster-admin ClusterRole by creating a new tekton-cluster-admin ClusterRole 
- Documentation for Windows
- Test Documentation on WSL
- Create output-raw.yaml for each pipeline run
- Auto generate _taskRun.yaml for custom-task in helm output via Notes.txt
- Auto generate a _pipelineRun.yaml for each pipeline in helm output via Notes.txt
- Add `taskcall[0].steps` to override `taskdefinition[0].steps` so that a developer can use the same task but have the steps overridden. This fix requires dynamic task creation in the background.

##  2. <a name='Summary:'></a>Summary: 

- Prerequisites
- Install Tekton
- Deploy Github webhooks (optional)
- Install Tekton Helm chart

Features:
- Values.yaml driven pipeline development 
- Dynamic task generation
- Least-privilege with isolated permissions for each task run
- Create/Delete Github webhook tasks


Successfully tested on:
 - AWS EKS > v1.22
 - OpenShift ROSA (OKD4)
 - Openshift OKD3
 - Kind [download](https://kind.sigs.k8s.io/) > v1.22
 - Microk8s
 - Rancher K3s 
 - Google Kubernetes Engine (GKE)


###  2.1. <a name='PreRequisties:'></a>PreRequisties: 

In order to install the Tekton Helm chart you will need a Kubernetes cluster > v1.22 and the below tools

- Kubernetes cluster (optional, see [kind.md](./kind.md) for deploying a local Kind cluster)
- Kubectl > v1.22
- Helm > v3.0
- AWS (optional, required for some examples)
- Docker (optional, required for running local Kubernetes Kind cluster and building/pushing images)


- MacOS


```bash
brew install kubectl
brew install helm

# AWS cli
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip
sudo ./aws/install
```

- Windows - Windows subsystem for Linux (WSL)

```bash

# Kubectl
curl -LO https://dl.k8s.io/release/v1.21.0/bin/linux/amd64/kubectl
sudo install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl
sudo apt-get update

# helm
sudo apt-key add -
sudo apt-get install apt-transport-https --yes
echo "deb https://baltocdn.com/helm/stable/debian/ all main" | sudo tee /etc/apt/sources.list.d/helm-stable-debian.list
sudo apt-get update
sudo apt-get install helm

# AWS cli
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip
sudo ./aws/install
rm -fr awscliv2.zip
rm -fr ./aws
```



###  2.2. <a name='InstallTekton'></a>Install Tekton

```bash
# Install pipeline CRD
# See here for version list https://github.com/tektoncd/pipeline/tags
kubectl apply -f https://storage.googleapis.com/tekton-releases/pipeline/previous/v0.40.2/release.yaml
# Install trigger and interceptor CRDs
# See here for version list https://github.com/tektoncd/triggers/tags
kubectl apply --filename https://storage.googleapis.com/tekton-releases/triggers/previous/v0.20.1/release.yaml
kubectl apply --filename https://storage.googleapis.com/tekton-releases/triggers/previous/v0.20.1/interceptors.yaml

# Install Tekton dashboard
# See here for version list  https://github.com/tektoncd/dashboard/tags
kubectl apply --filename https://storage.googleapis.com/tekton-releases/dashboard/previous/v0.29.2/tekton-dashboard-release.yaml
sleep 2
kubectl get pods --namespace tekton-pipelines --watch

# when complete
sleep 3
kubectl wait --for=condition=ready pod -n tekton-pipelines -l app=tekton-dashboard

```

- Expose the Tekton dashboard via Kind NodePort, must have installed using [cluster.yaml](./cluster.yaml) in [kind.md](./kind.md)

```bash
kubectl delete service tekton-dashboard -n tekton-pipelines
kubectl expose deployment tekton-dashboard --namespace tekton-pipelines --type=NodePort
kubectl patch service tekton-dashboard --namespace=tekton-pipelines --type='json' --patch='[{"op": "replace", "path": "/spec/ports/0/nodePort", "value":30080}]'
```
OR 

Navigate to Tekton Dashboard at http://localhost:30080

- Expose the Tekton dashboard via `kubectl port-forward` (using this method intermittent connection timeouts at the time of writing this)

```bash
kubectl port-forward svc/tekton-dashboard -n tekton-pipelines 8887:9097 
```

Navigate to Tekton Dashboard at http://localhost:8887

NOTE: The Tekton dashboard has a tendency to drop whilst using port-forwarding, to work around this hit CTRL+C and rerun the port forward command above. 

##  3. <a name='Installpipelinesexamples'></a>Install pipelines examples

See example [README.md](./examples/tekton-ecr-build-deploy/README.md)

- Example 1 - Clone, build and push docker image to ECR using Docker-in-docker

![](./examples/tekton-ecr-build-deploy/2022-10-17-23-18-35.png)

- Example 2 - Clone, build and push docker image to Dockerhub using Kaniko

![](./examples/tekton-ecr-build-deploy/2022-10-17-23-36-33.png)

- Example 3 - Clone, build and push docker image to Dockerhub using Buildah

![](./examples/tekton-buildah-build-deploy/2022-10-18-00-06-27.png)