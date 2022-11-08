

WARNING: This method of building images in Kubernetes is DEPRECIATED, Kubernetes will be dropping support for Docker in future versions. Please see Kaniko build [example](../tekton-kaniko-build-deploy/README.md) or Buildah build [example](../tekton-buildah-build-deploy/README.md)

# Tekton pipeline to build and push docker image to ECR and use Helm to deploy

Source repository https://github.com/cogitogroupltd/tekton-helm-chart

PreReqs:
- See [README.md](../../charts/tekton/README.md)

Description:

- Deploys a single Tekton pipeline called `prod` using `./values-override.yaml`
- Stages
  - `git-clone` - Clone down the application source code from GitHub containing a `Dockerfile`
  - `ecr-build-push` - Build the Dockerfile using Docker-in-docker and push it to ECR using the AWS credentials either in the `aws` secret or `AWS_ECR_ACCOUNT_ID`, `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`. The default will push to an ECR repository called "test"
  - `git-clone-infra` - Clone down the Helm chart `common` for use with the `helm-deploy` stage
  - `helm-deploy` - Deploy the docker image artifact from ECR using Helm to the cluster where Tekton is installed
- Uses local RSA private key located in root of this repository `.auth/id_rsa` for `git-clone` and `git-clone-infra`

![](2022-10-17-23-18-35.png)

## Install the pipeline

Ignore `github_token` if you are planning to manually trigger builds, see below for setting up Triggers `Run a pipeline via Trigger (requires additional configuration)`

NOTE:

- Ignore `github_token` if you are planning to manually trigger builds, see below for setting up Triggers `Run a pipeline via Trigger (requires additional configuration)`

- Beware this will create a secret in the cluster with the private SSH key located at `.auth/id_rsa`

```bash
cd examples/tekton-ecr-build-deploy
export DOCKERHUB_USERNAME=
export DOCKERHUB_PASSWORD=
export SLACK_WEBHOOK_URI=https://hooks.slack.com/services/TJL9A5PMJ/B03KPQ2V4JG/DUMMY
export SSH_KEY_LOCATION=../../.auth/id_rsa
docker_auth="$(echo -n "${DOCKERHUB_USERNAME}":"${DOCKERHUB_PASSWORD}" | base64)"
tee "config.json" > /dev/null <<EOF
{"auths":{"https://index.docker.io/v1/":{"auth":"$docker_auth","email":"thisemail@isignored.com"}}}
EOF
helm upgrade --install pipelines -n tekton-pipelines ../../charts/tekton --set github_token="$(echo -n "ENTERTOKEN" | base64)" --set secret_ssh_key="$(cat ../../.auth/id_rsa)" --values ./values-override.yaml
```

## Run a pipeline manually

```bash
cd examples/tekton-ecr-build-deploy
kubectl create -f pipelinerun.yaml
```

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
- Trigger push event using `git push` to repository defined in git-clone `./values-override.yaml` 

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
helm delete pipelines -n tekton-pipelines
```