<!-- vscode-markdown-toc -->
* 1. [Install Tekton](#InstallTekton)
* 2. [Example pipeline installations](#Examplepipelineinstallations)

<!-- vscode-markdown-toc-config
	numbering=true
	autoSave=true
	/vscode-markdown-toc-config -->
<!-- /vscode-markdown-toc --># Tekton pipelines Helm Chart



Successfully tested on:
 - AWS Elastic Kubernetes Services using NLB and ALB (AWS EKS v1.24)
 - Kind [download](https://kind.sigs.k8s.io/)
 - Rancher K3s 
 - Google Kubernetes Engine (GKE)
 - RedHat OpenShift AWS (ROSA)
 - RedHat Origin Kubernetes Distribution (OKD v4.0)

##  1. <a name='InstallTekton'></a>Install Tekton


- Installl Tekton system components

```bash
cd tekton-helm-chart/charts/tekton

# Deploy Kind cluster (Mac M1)
unset DOCKER_DEFAULT_PLATFORM; kind create cluster --name kind --image=rossgeorgiev/kind-node-arm64:v1.21.0 --config ./cluster.yaml
kind get kubeconfig > ~/.kube/config_kind ;
export KUBECONFIG=~/.kube/config_kind

# Deploy Kind cluster
kind create cluster --name kind ./cluster.yaml
kind get kubeconfig > ~/.kube/config_kind ;
export KUBECONFIG=~/.kube/config_kind

# Wait for the nodes to become ready
kubectl wait --for=condition=ready node kind-control-plane

# Install pipeline CRD
kubectl apply -f https://storage.googleapis.com/tekton-releases/pipeline/previous/v0.36.0/release.yaml
# Install trigger, interceptors CRDs
kubectl apply --filename https://storage.googleapis.com/tekton-releases/triggers/latest/release.yaml
kubectl apply --filename https://storage.googleapis.com/tekton-releases/triggers/latest/interceptors.yaml

# Install Tekton dashboard
kubectl apply --filename https://storage.googleapis.com/tekton-releases/dashboard/latest/tekton-dashboard-release.yaml

# when complete
sleep 3
kubectl wait --for=condition=ready pod -n tekton-pipelines -l app=tekton-dashboard
kubectl port-forward svc/tekton-dashboard -n tekton-pipelines 8887:9097 &

```

- Build and push Docker image for running pipeline stages (optional)

See [docker/cicd-agent/README.md](../../docker/cicd-agent/README.md)

- Open browser and navigate to http://localhost:8887


##  2. <a name='Examplepipelineinstallations'></a>Example pipeline installations

See [./examples](./examples)