# Tekton pipeline to build and push docker image to Dockerhub using Kaniko and deploy with Helm

Source repository https://github.com/cogitogroupltd/tekton-helm-chart

PreReqs:
- See [README.md](../../charts/tekton/README.md)

Description:

- Deploys a single Tekton pipeline called `prod` using `./values-override.yaml`
- Stages
  - `git-clone` - Clone down the application source code from GitHub containing a `Dockerfile`
  - `build-push` - Build the Dockerfile and push it to Dockerhub using Kaniko using credentials specified in `config.json`
  - `git-clone-infra` - Clone down the Helm chart `common` for use with the `helm-deploy` stage
  - `helm-deploy` - Deploy the docker image artifact from Dockerhub using Helm 
- Uses local RSA private key located in `~/.ssh/id_rsa` for `git-clone` and `git-clone-infra`
- Secures webhook to `EventListener` communication using a token specified in `.Values.github_token`

## Install pipelines


- Deploy Tekton pipeline helm chart

```bash

export SLACK_WEBHOOK_URI=https://hooks.slack.com/services/TJL9A5PMJ/B03KPQ2V4JG/DUMMY
docker_auth=$(echo -n george7522:somepass! | base64)
tee "config.json" > /dev/null <<EOF
{"auths":{"https://index.docker.io/v1/":{"auth":"$docker_auth","email":"george@gcrosby.co.uk"}}}
EOF
helm upgrade --install pipelines -n tekton-pipelines ../../charts/tekton --set github_token="$(echo -n "ENTERTOKEN" | base64)" --set secret_ssh_key="$(cat ~/.ssh/id_rsa)" --set-file=docker_config_json=config.json --values ./values-override.yaml
```

