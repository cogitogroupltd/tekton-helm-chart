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


- Deploy Tekton pipeline helm chart

NOTE:

- Ignore `github_token` if you are planning to manually trigger builds, see below for setting up Triggers `Run a pipeline via Trigger (requires additional configuration)`

- Beware this will create a secret in the cluster with the private SSH key located at `~/.ssh/id_rsa`

- Enter your Dockerhub username/password credentials in place of $DOCKERHUB_USER and $DOCKERHUB_PASSWORD


```bash
cd examples/tekton-buildah-build-deploy
export DOCKERHUB_USERNAME=
export DOCKERHUB_PASSWORD=
export SLACK_WEBHOOK_URI=https://hooks.slack.com/services/TJL9A5PMJ/B03KPQ2V4JG/DUMMY
# export SSH_KEY_LOCATION=~/.ssh/id_rsa #uncomment this if you are using SSH credentials for cloning
docker_auth="$(echo -n "${DOCKERHUB_USERNAME}":"${DOCKERHUB_PASSWORD}" | base64)"
tee "config.json" > /dev/null <<EOF
{"auths":{"https://index.docker.io/v1/":{"auth":"$docker_auth","email":"thisemail@isignored.com"}}}
EOF
helm upgrade --install pipelines -n tekton-pipelines ../../charts/tekton --set github_token="$(echo -n "ENTERTOKEN" | base64)" --set secret_ssh_key="$(cat $SSH_KEY_LOCATION)" --set-file=docker_config_json=config.json --values ./values-override.yaml
```