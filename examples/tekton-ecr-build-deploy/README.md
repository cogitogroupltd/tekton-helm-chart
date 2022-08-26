# Install


helm upgrade --install pipelines -n tekton-pipelines ./charts/tekton --set github_token="$(echo -n "ENTERTOKEN" | base64)" --set secret_ssh_key="$(cat /Users/george/.ssh/id_rsa)" --set-file=docker_config_json=config.json --values /Users/george/dev/cogitogroupltd/tekton-helm-chart/examples/tekton-ecr-build-deploy/values-override.yaml --set secret_slack_webhook_uri=${SLACK_WEBHOOK_URI}