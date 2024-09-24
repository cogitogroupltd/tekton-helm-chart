# Tekton pipeline to build and push docker image to Dockerhub using Kaniko and deploy with Helm

Source repository https://github.com/cogitogroupltd/tekton-helm-chart

PreReqs:
- See Section 1.3 in [README.md](../../README.md)
- DockerHub credentials

Description:

- Deploys a single Tekton pipeline called `prod` using `./values-override.yaml`
- Stages
  - `git-clone` - Clone down the application source code from GitHub containing a `Dockerfile`
  - `build-push` - Build the Dockerfile using Kaniko and push it to Dockerhub using Kaniko using credentials specified in `config.json`
  - `rolling-update` - Deploy the docker image artifact to your existing Kubernetes deployment
- Uses local RSA private key located in `.auth/id_rsa` for `git-clone` and `git-clone-infra`

![](2022-10-17-23-36-33.png)
## Install pipelines


- Deploy Tekton pipeline helm chart

NOTE:

- Ignore `github_token` if you are planning to manually trigger builds, see below for setting up Triggers `Run a pipeline via Trigger (requires additional configuration)`

- Beware this will create a secret in the cluster with the private SSH key located at `.auth/id_rsa`

- Enter your Dockerhub username/password credentials inside [.env](../../.env) in place of $CONTAINER_REGISTRY_USERNAME and $CONTAINER_REGISTRY_PASSWORD

```bash
cd examples/kaniko-build-deploy
source ../../.env
export SSH_KEY_LOCATION=../../.auth/id_rsa
docker_auth=$(echo -n $CONTAINER_REGISTRY_USERNAME:$CONTAINER_REGISTRY_PASSWORD | base64)
tee "config.json" > /dev/null <<EOF
{"auths":{"https://index.docker.io/v1/":{"auth":"$docker_auth","email":"thisemail@isignored.com"}}}
EOF
helm upgrade --install pipelines -n tekton-resources --create-namespace ../../charts/tekton --set github_token="$(echo -n "ENTERTOKEN" | base64)" --set secret_ssh_key="$(cat $SSH_KEY_LOCATION)" --set-file=docker_config_json=config.json --values ./values-override.yaml
```



## Run a pipeline manually

```bash
cd examples/kaniko-build-deploy
kubectl create -f pipelinerun.yaml
```

- Check the deployed app

```bash
kubectl get pod --namespace default
```

## Navigate to the dashboard

- Open your browser and navigate to http://localhost:30080/#/namespaces/tekton-resources/pipelineruns

or using port-forward

- Execute a tunnel to the dashboard `kubectl port-forward svc/tekton-dashboard -n tekton-pipelines 8887:9097`

- Open your browser and navigate to http://localhost:8887/#/namespaces/tekton-resources/pipelineruns


## Run a pipeline via Trigger (requires additional configuration)

NOTE: If you are running locally you will need to configure inbound firewall rules on your router!

- Open inbound firewall rules to allow traffic from GitHub, see here https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/about-githubs-ip-addresses)
- Open outbound firewall rules to allow traffic to GitHub, see here https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/about-githubs-ip-addresses)
- Uncomment `.Values.services` in `values-override.yaml` and alter certificate ARN to expose your `EventListener` to GitHub on HTTPS
- Run install step above again and specify any `github_token` by replacing "ENTERTOKEN"
- Create public DNS entry for your new LoadBalancer resource eg. tekton.cogitogroup.co.uk

- Alter values in [_taskrun.yaml](../../charts/tekton/templates/create-webhook/_taskrun.yaml) according to your DNS entry, repository name.
- Create the webhook in Github

```bash
kubectl create -f ../../charts/tekton/templates/create-webhook/_taskrun.yaml
```
- Trigger push event using `git push` to repository defined in git-clone `./values-override.yaml` and 

or 

- Use an example github payload to test triggers locally (see Github -> Settings -> Webhooks -> Recent Deliveries) to export ane example `payload.json` (NOTE: This will not work if you have a webhook token setup and specified in `.Values.pipelines[0].trigger.token` )

```bash
kubectl run debug-pod --image=nginx 
kubectl cp payload.json debug-pod:/root/payload.json
kubectl exec -it debug-pod -- curl -X POST http://el-dev-listener.tekton-pipelines.svc.cluster.local:8080 -H 'X-GitHub-Event: pull_request' -d @/root/payload.json
```



## Uninstall

To uninstall the Tekton pipeline

```bash
helm delete pipelines -n tekton-resources
```