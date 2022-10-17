# Tekton pipeline to build and push docker image to Dockerhub using Buildah

Source repository https://github.com/cogitogroupltd/tekton-helm-chart

PreReqs:
- See [README.md](../../charts/tekton/README.md)

Description:

- Deploys a single Tekton pipeline called `prod` using `./values-override.yaml`
- Stages
  - `git-clone` - Clone down the application source code from GitHub containing a `Dockerfile`
  - `buildah-build-push` - Build the Dockerfile using Buildah and pushes it to Dockerhub using the credentials in `config.json`
  - `rolling-update` - Deploy the docker image artifact to your existing Kubernetes deployment
- Uses local RSA private key located in `~/.ssh/id_rsa` for `git-clone` 
- Secures webhook to `EventListener` communication using a token specified in `.Values.github_token`

![](2022-10-18-00-06-27.png)


## Install the pipeline

```bash
export SLACK_WEBHOOK_URI=https://hooks.slack.com/services/TJL9A5PMJ/B03KPQ2V4JG/DUMMY
docker_auth=$(echo -n george7522:pass! | base64)
tee "config.json" > /dev/null <<EOF
{"auths":{"https://index.docker.io/v1/":{"auth":"$docker_auth","email":"george@gcrosby.co.uk"}}}
EOF
helm upgrade --install pipelines -n tekton-pipelines ../../charts/tekton --set github_token="$(echo -n "ENTERTOKEN" | base64)" --set secret_ssh_key="$(cat ~/.ssh/id_rsa)" --set-file=docker_config_json=config.json --values ./values-override.yaml
```