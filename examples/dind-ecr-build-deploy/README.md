

WARNING: This method of building images in Kubernetes is DEPRECIATED, Kubernetes will be dropping support for Docker in future versions. Please see Kaniko build [example](../kaniko-build-deploy/README.md) or Buildah build [example](../buildah-build-deploy/README.md)

# Tekton pipeline to build and push docker image to ECR and use Helm to deploy

Source repository https://github.com/cogitogroupltd/tekton-helm-chart

PreReqs:
- See Section 1.3 in [README.md](../../README.md)

Description:

- Deploys a single Tekton pipeline called `prod` using the Helm chart inputs defined in `./values-override.yaml`
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
cd examples/dind-ecr-build-deploy
source ../../.env
export SLACK_WEBHOOK_URI=https://hooks.slack.com/services/TJL9A5PMJ/B03KPQ2V4JG/DUMMY
export SSH_KEY_LOCATION=../../.auth/id_rsa
docker_auth="$(echo -n "${CONTAINER_REGISTRY_USERNAME}":"${DOCKERHUB_PASSWORD}" | base64)"
tee "config.json" > /dev/null <<EOF
{"auths":{"https://index.docker.io/v1/":{"auth":"$docker_auth","email":"thisemail@isignored.com"}}}
EOF
helm template pipelines -n tekton-resources --create-namespace tekton/pipeline --set secret_ssh_key="$(cat $SSH_KEY_LOCATION)" --values ./values-override.yaml | kubectl apply -n tekton-resources -f -
```

## Run a pipeline manually

```bash
cd examples/dind-ecr-build-deploy
kubectl create -f pipelinerun.yaml
```

## Navigate to the dashboard

- Open your browser and navigate to http://localhost:30080/#/namespaces/tekton-resources/pipelineruns

or using port-forward

- Execute a tunnel to the dashboard `kubectl port-forward svc/tekton-dashboard -n tekton-pipelines 8887:9097`

- Open your browser and navigate to http://localhost:8887/#/namespaces/tekton-resources/pipelineruns



## Uninstall

To uninstall the Tekton pipeline

```bash
helm template pipelines -n tekton-resources --create-namespace tekton/pipeline --set secret_ssh_key="$(cat $SSH_KEY_LOCATION)" --values ./values-override.yaml | kubectl delete -n tekton-resources -f -
```