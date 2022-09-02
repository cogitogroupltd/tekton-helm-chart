# Tekton pipeline to build and push docker image to ECR and use Helm to deploy

PreReqs:
- See [README.md](../../charts/tekton/README.md)

Description:

- Deploys a single Tekton pipeline called `prod` using `./values-override.yaml`
- Stages
  - `git-clone` - Clone down the application source code from GitHub containing a `Dockerfile`
  - `ecr-build-push` - Build the Dockerfile and push it to ECR using the AWS credentials either in the `aws` secret or `AWS_ECR_ACCOUNT_ID`, `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`
  - `git-clone-infra` - Clone down the Helm chart `common` for use with the `helm-deploy` stage
  - `helm-deploy` - Deploy the docker image artifact from ECR using Helm 
- Uses local RSA private key located in `~/.ssh/id_rsa` for `git-clone` and `git-clone-infra`
- Secures webhook to `EventListener` communication using a token specified in `.Values.github_token`


## Install

```bash
cd examples/tekton-ecr-build-deploy
helm upgrade --install pipelines -n tekton-pipelines ../../charts/tekton --set github_token="$(echo -n "ENTERTOKEN" | base64)" --set secret_ssh_key="$(cat ~/.ssh/id_rsa)" --values ./values-override.yaml
```

## Run a pipeline manually

```bash
cd examples/tekton-ecr-build-deploy
kubectl create -f pipelinerun.yaml
```

## Run a pipeline via Trigger (requires security group rules to allow traffic from GitHub org, see here https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/about-githubs-ip-addresses)

```bash
# Create the Github Webhook
kubectl create -f ../../charts/tekton/templates/create-webhook/_taskrun.yaml
# Trigger push event using `git push` to repository defined in git-clone ./values-override.yaml
```

## Uninstall

To uninstall the Tekton pipeline

```bash
helm delete pipelines -n tekton-pipelines
```