# Tekton pipeline to build and push docker image to Dockerhub using Kaniko and deploy with Helm

Source repository https://github.com/cogitogroupltd/tekton-helm-chart

PreReqs:
- See [README.md](../../charts/tekton/README.md)

Description:

- Deploys a single Tekton pipeline called `prod` using `./values-override.yaml`
- Stages
  - `git-clone` - Clone down the application source code from GitHub containing a `Dockerfile`
  - `build-push` - Build the Dockerfile using Kaniko and push it to Dockerhub using Kaniko using credentials specified in `config.json`
  - `git-clone-infra` - Clone down the Helm chart `common` for use with the `helm-deploy` stage
  - `helm-deploy` - Deploy the docker image artifact from Dockerhub using Helm 
- Uses local RSA private key located in `~/.ssh/id_rsa` for `git-clone` and `git-clone-infra`
- Secures webhook to `EventListener` communication using a token specified in `.Values.github_token`

![](2022-10-17-23-36-33.png)
## Install pipelines


- Deploy Tekton pipeline helm chart (NOTE: replace credentials)

Ignore `github_token` if you are planning to manually trigger builds, see below for setting up Triggers `Run a pipeline via Trigger (requires additional configuration)`

```bash

export SLACK_WEBHOOK_URI=https://hooks.slack.com/services/TJL9A5PMJ/B03KPQ2V4JG/DUMMY
docker_auth=$(echo -n george7522:somepass! | base64)
tee "config.json" > /dev/null <<EOF
{"auths":{"https://index.docker.io/v1/":{"auth":"$docker_auth","email":"george@gcrosby.co.uk"}}}
EOF
helm upgrade --install pipelines -n tekton-pipelines ../../charts/tekton --set github_token="$(echo -n "ENTERTOKEN" | base64)" --set secret_ssh_key="$(cat ~/.ssh/id_rsa)" --set-file=docker_config_json=config.json --values ./values-override.yaml
```



## Run a pipeline manually

```bash
cd examples/tekton-kaniko-build-deploy
kubectl create -f pipelinerun.yaml
```

## Run a pipeline via Trigger (requires additional configuration)

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



## Uninstall

To uninstall the Tekton pipeline

```bash
helm delete pipelines -n tekton-pipelines
```