# Install Tekton



ToDo:
- Move buildpush script to configMap
- Create _taskRun output for custom-task
- Write up usage of example
- Slack webhook uri - how to exclude
- EventListener add secret
- github_token - ignore if empty? Or prompt user for input if required



```bash
# Deploy Kind cluster (Mac M1)
unset DOCKER_DEFAULT_PLATFORM; kind create cluster --name kind --image=rossgeorgiev/kind-node-arm64:v1.21.0 --config ~/.kube/cluster.yaml
kind get kubeconfig > ~/.kube/config_kind ;
export KUBECONFIG=~/.kube/config_kind

# Install pipeline CRD
kubectl apply -f https://storage.googleapis.com/tekton-releases/pipeline/previous/v0.36.0/release.yaml
# Install trigger CRDs
kubectl apply --filename https://storage.googleapis.com/tekton-releases/triggers/latest/release.yaml
kubectl apply --filename https://storage.googleapis.com/tekton-releases/triggers/latest/interceptors.yaml

# Install Tekton dashboard
kubectl apply --filename https://storage.googleapis.com/tekton-releases/dashboard/latest/tekton-dashboard-release.yaml
#kubectl get pods --namespace tekton-pipelines --watch

# when complete
sleep 3
kubectl wait --for=condition=ready pod -n tekton-pipelines -l app=tekton-dashboard
kubectl port-forward svc/tekton-dashboard -n tekton-pipelines 8887:9097 &


# Install sample app to deploy to with Tekton
helm upgrade --install nginx ./charts/common --namespace default --values ./examples/common-nginx-helloworld/override-values.yaml

# Deploy Tekton pipeline helm chart
export SLACK_WEBHOOK_URI=https://hooks.slack.com/services/TJL9A5PMJ/B03KPQ2V4JG/DUMMY
docker_auth=$(echo -n george7522:somepass! | base64)
tee "config.json" > /dev/null <<EOF
{"auths":{"https://index.docker.io/v1/":{"auth":"$docker_auth","email":"george@gcrosby.co.uk"}}}
EOF

kubectl wait --for=condition=ready pod -n tekton-pipelines -l app=tekton-pipelines-controller
kubectl delete secret --ignore-not-found=true aws ; kubectl create secret generic aws --from-file=/Users/george/.aws/CC
helm upgrade --install dev ./charts/tekton --set github_token="$(echo -n "ENTERTOKEN" | base64)"  --set secret_ssh_key="$(cat /Users/george/.ssh/id_rsa)" --set-file=docker_config_json=config.json --values ./examples/tekton-stg-dummy/values-override.yaml --set secret_slack_webhook_uri=${SLACK_WEBHOOK_URI} --values charts/tekton/values-override.yml --debug


# Create a pipeline run
kubectl create -f /Users/george/dev/cogitogroupltd/boilerplate/charts/tekton/templates/_pipelinerun.yml 
#or using webhook listener, example payload.json supplied.
kubectl cp payload.json $(kubectl get pod | grep -i nginx-app | awk '{print $1}'):/root/payload.json
kubectl exec -it deploy/nginx-app -- curl -X POST http://el-dev-listener.default.svc.cluster.local:8080 -H 'X-GitHub-Event: pull_request' -d @/root/payload.json
```