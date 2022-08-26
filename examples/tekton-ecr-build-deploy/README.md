# How to install

cd tekton-helm-chart
export SLACK_WEBHOOK_URI=https://hooks.slack.com/services/TJL9A5PMJ/B03KPQ2V4JG/DUMMY
docker_auth=$(echo -n 'george7522:SOMEPASS' | base64)
tee "config.json" > /dev/null <<EOF
{"auths":{"https://index.docker.io/v1/":{"auth":"$docker_auth","email":"george@gcrosby.co.uk"}}}
EOF

helm upgrade --install pipelines -n tekton-pipelines ./charts/tekton --set github_token="$(echo -n "ENTERTOKEN" | base64)" --set secret_ssh_key="$(cat /Users/george/.ssh/id_rsa)" --set-file=docker_config_json=config.json --values /Users/george/dev/cogitogroupltd/tekton-helm-chart/examples/tekton-ecr-build-deploy/values-override.yaml --set secret_slack_webhook_uri=${SLACK_WEBHOOK_URI}