

### Install Tekton core components and CRDs

It's recommended to follow the installation instruction on Tekton website here https://tekton.dev/docs/installation/

Below we run through an example of installing versions compatible with 
```bash
# Install pipeline CRD
# See here for version list https://github.com/tektoncd/pipeline/tags
kubectl apply -f https://storage.googleapis.com/tekton-releases/pipeline/previous/v0.59.0/release.yaml
# Install trigger and interceptor CRDs
# See here for version list https://github.com/tektoncd/triggers/tags
kubectl apply --filename https://storage.googleapis.com/tekton-releases/triggers/previous/v0.27.0/release.yaml
kubectl apply --filename https://storage.googleapis.com/tekton-releases/triggers/previous/v0.27.0/interceptors.yaml

# Install Tekton dashboard
# See here for version list  https://github.com/tektoncd/dashboard/tags
kubectl apply --filename https://storage.googleapis.com/tekton-releases/dashboard/previous/v0.46.0/release.yaml
sleep 2
kubectl get pods --namespace tekton-pipelines --watch

# when complete
sleep 3
kubectl wait --for=condition=ready pod -n tekton-pipelines -l app=tekton-dashboard

```

- Expose the Tekton dashboard via Kind NodePort, must have installed using [cluster.yaml](./cluster.yaml) in [kind.md](./docs/kind.md)

```bash
kubectl delete service tekton-dashboard -n tekton-pipelines
kubectl expose deployment tekton-dashboard --namespace tekton-pipelines --type=NodePort
kubectl patch service tekton-dashboard --namespace=tekton-pipelines --type='json' --patch='[{"op": "replace", "path": "/spec/ports/0/nodePort", "value":30080}]'
```

Navigate to Tekton Dashboard at http://localhost:30080

OR

- Expose the Tekton dashboard via `kubectl port-forward` (using this method intermittent connection timeouts at the time of writing this)

```bash
kubectl port-forward svc/tekton-dashboard -n tekton-pipelines 8887:9097
```

Navigate to Tekton Dashboard at http://localhost:8887

NOTE: The Tekton dashboard has a tendency to drop whilst using port-forwarding, to work around this hit CTRL+C and rerun the port forward command above.
