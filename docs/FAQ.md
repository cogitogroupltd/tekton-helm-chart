# FAQ

## Troubleshooting errors

To troubleshoot errors make sure you run `helm template` with the `--debug` flag to further inspect Kubernetes resources. 

For example:
```bash
helm template pipelines -n tekton-pipelines ./charts/tekton --set github_token="$(echo -n "ENTERTOKEN" | base64)" --set secret_ssh_key="$(cat .auth/id_rsa)" --set-file=docker_config_json=config.json --values ./examples/tekton-ecr-build-deploy/values-override.yaml --set secret_slack_webhook_uri=${SLACK_WEBHOOK_URI}
```


## Solutions to common problems

Command run: `helm upgrade --install pipelines -n tekton-pipelines ./charts/tekton --set github_token="$(echo -n "ENTERTOKEN" | base64)" --set secret_ssh_key="$(cat .auth/id_rsa)" --set-file=docker_config_json=config.json --values ./examples/tekton-ecr-build-deploy/values-override.yaml --set secret_slack_webhook_uri=${SLACK_WEBHOOK_URI}`

Error:
```
pod/tekton-pipelines-controller-5cfb9b8cfc-s8l45 condition met
secret "aws" deleted
secret/aws created
WARNING: Kubernetes configuration file is group-readable. This is insecure. Location: /Users/george/.kube/config_kind
WARNING: Kubernetes configuration file is world-readable. This is insecure. Location: /Users/george/.kube/config_kind
Error: UPGRADE FAILED: cannot patch "prod" with kind Pipeline: admission webhook "webhook.pipeline.tekton.dev" denied the request: mutation failed: cannot create patch for round tripped newBytes: cannot marshal interface: json: error calling MarshalJSON for type v1beta1.ArrayOrString: impossible ArrayOrString.Type: ""
```

Problem:
A property in the values-override.yaml is incorrect and the helm upgrade command fails with a non-descriptive type error.

Solution:

For me there was a mismatched type in the `AWS_ECR_ACCOUNT_ID` parameter pipelines[0].taskcall[0].params which specified "default" rather than "value"

before fix:

```yaml
pipelines:
  - name: prod
    taskcall:
    - name: helm-deploy
      taskRef:
        name: helm-deploy
      workspaces:
      - name: git-pvc
        workspace: "git-pvc"
      runAfter:
        - git-clone-infra
      params:
      - name: AWS_ECR_ACCOUNT_ID
        default: "009453609091"
      - name: AWS_ACCESS_KEY_ID
        value: "AKIAQEM32UCBS2RNSP5K"
```

after fix:
```yaml
pipelines:
  - name: prod
    taskcall:
    - name: helm-deploy
      taskRef:
        name: helm-deploy
      workspaces:
      - name: git-pvc
        workspace: "git-pvc"
      runAfter:
        - git-clone-infra
      params:
      - name: AWS_ECR_ACCOUNT_ID
        value: "009453609091"
      - name: AWS_ACCESS_KEY_ID
        value: "AKIAQEM32UCBS2RNSP5K"
```




Problem:
Tekton task fails to run with permission denied when trying to access Kubernetes objects

`Error from server (Forbidden): secrets "regcred" is forbidden: User "system:serviceaccount:tekton-pipelines:default" cannot delete resource "secrets" in API group "" in the namespace "api-infrared"`

Solution:
Kubernetes `serviceAccounts` can be defined in the `taskdefinitions` and should match the name of `Task` name
eg. To grant a `Task` full permission to Kubernetes cluster define as below
```yaml
taskdefinitions:
  serviceAccounts:
  - name: helm-deploy
    yaml: |-
      apiVersion: v1
      kind: ServiceAccount
      metadata:
        name: helm-deploy
        namespace: tekton-pipelines
      ---
      apiVersion: rbac.authorization.k8s.io/v1
      kind: ClusterRoleBinding
      metadata:
        name: "cluster-administrator-helm-deploy"
      subjects:
        - kind: ServiceAccount
          name: "helm-deploy"
          namespace: tekton-pipelines
      roleRef:
        kind: ClusterRole
        name: cluster-admin
        apiGroup: rbac.authorization.k8s.io
```
And match the `helm-deploy` name to your `Task` name

```yaml
taskdefinitions:
  tasks:
  - name: helm-deploy
```


Error:
```
george tekton$ helm upgrade --install pipelines -n tekton-pipelines ./charts/tekton --set github_token="$(echo -n "$GITHUB_WEBHOOK_SECRET" | base64)" --set secret_ssh_key="$(cat .auth/id_rsa)" --set-file=docker_config_json=config.json --values ./values-override.yaml --set secret_slack_webhook_uri=${SLACK_WEBHOOK_URI} --set "pipelines[0].trigger.token=$GITHUB_WEBHOOK_SECRET" --set "pipelines[1].trigger.token=$GITHUB_WEBHOOK_SECRET" --set "pipelines[2].trigger.token=$GITHUB_WEBHOOK_SECRET" --debug
WARNING: Kubernetes configuration file is group-readable. This is insecure. Location: /Users/george/.kube/config
WARNING: Kubernetes configuration file is world-readable. This is insecure. Location: /Users/george/.kube/config
history.go:56: [debug] getting history for release pipelines
upgrade.go:142: [debug] preparing upgrade for pipelines
upgrade.go:150: [debug] performing update for pipelines
upgrade.go:322: [debug] creating upgraded release for pipelines
client.go:218: [debug] checking 53 resources for changes
client.go:501: [debug] Looks like there are no changes for ServiceAccount "cronjob-tekton-cleanup"
client.go:501: [debug] Looks like there are no changes for ServiceAccount "pipelines-tekton-default-sa"
client.go:501: [debug] Looks like there are no changes for ServiceAccount "get-image-tag"
client.go:501: [debug] Looks like there are no changes for ServiceAccount "helm-deploy"
client.go:501: [debug] Looks like there are no changes for ServiceAccount "pipelines-tekton-triggers-sa"
client.go:501: [debug] Looks like there are no changes for Secret "github-secret"
client.go:501: [debug] Looks like there are no changes for Secret "pipelines-ssh-key"
client.go:501: [debug] Looks like there are no changes for Secret "pipelines-docker-config"
client.go:501: [debug] Looks like there are no changes for Secret "pipelines-webhook-secret"
client.go:501: [debug] Looks like there are no changes for Secret "promote-image-github-token"
client.go:501: [debug] Looks like there are no changes for Secret "develop-build-deploy-github-token"
client.go:501: [debug] Looks like there are no changes for Secret "ort-github-token"
client.go:501: [debug] Looks like there are no changes for ConfigMap "configmap-config"
client.go:501: [debug] Looks like there are no changes for ConfigMap "pipelines-kube-config"
client.go:501: [debug] Looks like there are no changes for ClusterRole "pipelines-tekton-triggers-cr"
client.go:501: [debug] Looks like there are no changes for ClusterRoleBinding "cluster-administrator-tekton-cronjob"
client.go:501: [debug] Looks like there are no changes for ClusterRoleBinding "cluster-administrator-tekton-pipelines-pipelines"
client.go:501: [debug] Looks like there are no changes for ClusterRoleBinding "cluster-administrator-get-image-tag"
client.go:501: [debug] Looks like there are no changes for ClusterRoleBinding "cluster-administrator-helm-deploy"
client.go:501: [debug] Looks like there are no changes for ClusterRoleBinding "pipelines-tekton-triggers-crb"
client.go:501: [debug] Looks like there are no changes for Role "pipelines-tekton-triggers-role"
client.go:501: [debug] Looks like there are no changes for RoleBinding "pipelines-tekton-triggers-rb"
client.go:510: [debug] Patch Service "pipelines-webhook" in namespace tekton-pipelines
client.go:501: [debug] Looks like there are no changes for CronJob "cronjob-tekton-cleanup"
client.go:510: [debug] Patch EventListener "dev-listener" in namespace tekton-pipelines
client.go:250: [debug] error updating the resource "dev-listener":
         cannot patch "dev-listener" with kind EventListener: Internal error occurred: failed calling webhook "webhook.triggers.tekton.dev": failed to call webhook: Post "https://tekton-triggers-webhook.openshift-pipelines.svc:443/defaulting?timeout=10s": service "tekton-triggers-webhook" not found
client.go:510: [debug] Patch Pipeline "promote-image" in namespace tekton-pipelines
client.go:510: [debug] Patch Pipeline "develop-build-deploy" in namespace tekton-pipelines
client.go:510: [debug] Patch Pipeline "ort" in namespace tekton-pipelines
client.go:510: [debug] Patch Pipeline "dev" in namespace tekton-pipelines
client.go:510: [debug] Patch Route "webhook" in namespace tekton-pipelines
client.go:510: [debug] Patch Task "buildah-build" in namespace tekton-pipelines
client.go:250: [debug] error updating the resource "buildah-build":
         cannot patch "buildah-build" with kind Task: admission webhook "webhook.pipeline.tekton.dev" denied the request: mutation failed: cannot decode incoming new object: json: unknown field "type"
client.go:510: [debug] Patch Task "pipelines-create-webhook" in namespace tekton-pipelines
client.go:510: [debug] Patch Task "pipelines-delete-webhook" in namespace tekton-pipelines
client.go:510: [debug] Patch Task "git-clone" in namespace tekton-pipelines
client.go:250: [debug] error updating the resource "git-clone":
         cannot patch "git-clone" with kind Task: admission webhook "webhook.pipeline.tekton.dev" denied the request: mutation failed: cannot decode incoming new object: json: unknown field "type"
client.go:510: [debug] Patch Task "kaniko-build" in namespace tekton-pipelines
client.go:250: [debug] error updating the resource "kaniko-build":
         cannot patch "kaniko-build" with kind Task: admission webhook "webhook.pipeline.tekton.dev" denied the request: mutation failed: cannot decode incoming new object: json: unknown field "type"
client.go:510: [debug] Patch Task "kubectl-restart-deployment" in namespace tekton-pipelines
client.go:510: [debug] Patch Task "send-to-webhook-slack" in namespace tekton-pipelines
client.go:510: [debug] Patch Task "get-image-tag" in namespace tekton-pipelines
client.go:250: [debug] error updating the resource "get-image-tag":
         cannot patch "get-image-tag" with kind Task: admission webhook "webhook.pipeline.tekton.dev" denied the request: mutation failed: cannot decode incoming new object: json: unknown field "type"
client.go:510: [debug] Patch Task "helm-deploy" in namespace tekton-pipelines
client.go:250: [debug] error updating the resource "helm-deploy":
         cannot patch "helm-deploy" with kind Task: admission webhook "webhook.pipeline.tekton.dev" denied the request: mutation failed: cannot decode incoming new object: json: unknown field "value"
client.go:510: [debug] Patch Task "ort-code-analysis" in namespace tekton-pipelines
client.go:510: [debug] Patch Task "echo-pipeline-params" in namespace tekton-pipelines
client.go:510: [debug] Patch Trigger "promote-image" in namespace tekton-pipelines
client.go:250: [debug] error updating the resource "promote-image":
         cannot patch "promote-image" with kind Trigger: Internal error occurred: failed calling webhook "webhook.triggers.tekton.dev": failed to call webhook: Post "https://tekton-triggers-webhook.openshift-pipelines.svc:443/defaulting?timeout=10s": service "tekton-triggers-webhook" not found
client.go:510: [debug] Patch Trigger "develop-build-deploy" in namespace tekton-pipelines
client.go:250: [debug] error updating the resource "develop-build-deploy":
         cannot patch "develop-build-deploy" with kind Trigger: Internal error occurred: failed calling webhook "webhook.triggers.tekton.dev": failed to call webhook: Post "https://tekton-triggers-webhook.openshift-pipelines.svc:443/defaulting?timeout=10s": service "tekton-triggers-webhook" not found
client.go:510: [debug] Patch Trigger "ort" in namespace tekton-pipelines
client.go:250: [debug] error updating the resource "ort":
         cannot patch "ort" with kind Trigger: Internal error occurred: failed calling webhook "webhook.triggers.tekton.dev": failed to call webhook: Post "https://tekton-triggers-webhook.openshift-pipelines.svc:443/defaulting?timeout=10s": service "tekton-triggers-webhook" not found
client.go:510: [debug] Patch Trigger "dev" in namespace tekton-pipelines
client.go:250: [debug] error updating the resource "dev":
         cannot patch "dev" with kind Trigger: Internal error occurred: failed calling webhook "webhook.triggers.tekton.dev": failed to call webhook: Post "https://tekton-triggers-webhook.openshift-pipelines.svc:443/defaulting?timeout=10s": service "tekton-triggers-webhook" not found
client.go:510: [debug] Patch TriggerBinding "promote-image" in namespace tekton-pipelines
client.go:250: [debug] error updating the resource "promote-image":
         cannot patch "promote-image" with kind TriggerBinding: Internal error occurred: failed calling webhook "webhook.triggers.tekton.dev": failed to call webhook: Post "https://tekton-triggers-webhook.openshift-pipelines.svc:443/defaulting?timeout=10s": service "tekton-triggers-webhook" not found
client.go:510: [debug] Patch TriggerBinding "develop-build-deploy" in namespace tekton-pipelines
client.go:250: [debug] error updating the resource "develop-build-deploy":
         cannot patch "develop-build-deploy" with kind TriggerBinding: Internal error occurred: failed calling webhook "webhook.triggers.tekton.dev": failed to call webhook: Post "https://tekton-triggers-webhook.openshift-pipelines.svc:443/defaulting?timeout=10s": service "tekton-triggers-webhook" not found
client.go:510: [debug] Patch TriggerBinding "ort" in namespace tekton-pipelines
client.go:250: [debug] error updating the resource "ort":
         cannot patch "ort" with kind TriggerBinding: Internal error occurred: failed calling webhook "webhook.triggers.tekton.dev": failed to call webhook: Post "https://tekton-triggers-webhook.openshift-pipelines.svc:443/defaulting?timeout=10s": service "tekton-triggers-webhook" not found
client.go:510: [debug] Patch TriggerBinding "dev" in namespace tekton-pipelines
client.go:250: [debug] error updating the resource "dev":
         cannot patch "dev" with kind TriggerBinding: Internal error occurred: failed calling webhook "webhook.triggers.tekton.dev": failed to call webhook: Post "https://tekton-triggers-webhook.openshift-pipelines.svc:443/defaulting?timeout=10s": service "tekton-triggers-webhook" not found
client.go:510: [debug] Patch TriggerTemplate "promote-image" in namespace tekton-pipelines
client.go:250: [debug] error updating the resource "promote-image":
         cannot patch "promote-image" with kind TriggerTemplate: Internal error occurred: failed calling webhook "webhook.triggers.tekton.dev": failed to call webhook: Post "https://tekton-triggers-webhook.openshift-pipelines.svc:443/defaulting?timeout=10s": service "tekton-triggers-webhook" not found
client.go:510: [debug] Patch TriggerTemplate "develop-build-deploy" in namespace tekton-pipelines
client.go:250: [debug] error updating the resource "develop-build-deploy":
         cannot patch "develop-build-deploy" with kind TriggerTemplate: Internal error occurred: failed calling webhook "webhook.triggers.tekton.dev": failed to call webhook: Post "https://tekton-triggers-webhook.openshift-pipelines.svc:443/defaulting?timeout=10s": service "tekton-triggers-webhook" not found
client.go:510: [debug] Patch TriggerTemplate "ort" in namespace tekton-pipelines
client.go:250: [debug] error updating the resource "ort":
         cannot patch "ort" with kind TriggerTemplate: Internal error occurred: failed calling webhook "webhook.triggers.tekton.dev": failed to call webhook: Post "https://tekton-triggers-webhook.openshift-pipelines.svc:443/defaulting?timeout=10s": service "tekton-triggers-webhook" not found
client.go:510: [debug] Patch TriggerTemplate "dev" in namespace tekton-pipelines
client.go:250: [debug] error updating the resource "dev":
         cannot patch "dev" with kind TriggerTemplate: Internal error occurred: failed calling webhook "webhook.triggers.tekton.dev": failed to call webhook: Post "https://tekton-triggers-webhook.openshift-pipelines.svc:443/defaulting?timeout=10s": service "tekton-triggers-webhook" not found
upgrade.go:431: [debug] warning: Upgrade "pipelines" failed: cannot patch "dev-listener" with kind EventListener: Internal error occurred: failed calling webhook "webhook.triggers.tekton.dev": failed to call webhook: Post "https://tekton-triggers-webhook.openshift-pipelines.svc:443/defaulting?timeout=10s": service "tekton-triggers-webhook" not found && cannot patch "buildah-build" with kind Task: admission webhook "webhook.pipeline.tekton.dev" denied the request: mutation failed: cannot decode incoming new object: json: unknown field "type" && cannot patch "git-clone" with kind Task: admission webhook "webhook.pipeline.tekton.dev" denied the request: mutation failed: cannot decode incoming new object: json: unknown field "type" && cannot patch "kaniko-build" with kind Task: admission webhook "webhook.pipeline.tekton.dev" denied the request: mutation failed: cannot decode incoming new object: json: unknown field "type" && cannot patch "get-image-tag" with kind Task: admission webhook "webhook.pipeline.tekton.dev" denied the request: mutation failed: cannot decode incoming new object: json: unknown field "type" && cannot patch "helm-deploy" with kind Task: admission webhook "webhook.pipeline.tekton.dev" denied the request: mutation failed: cannot decode incoming new object: json: unknown field "value" && cannot patch "promote-image" with kind Trigger: Internal error occurred: failed calling webhook "webhook.triggers.tekton.dev": failed to call webhook: Post "https://tekton-triggers-webhook.openshift-pipelines.svc:443/defaulting?timeout=10s": service "tekton-triggers-webhook" not found && cannot patch "develop-build-deploy" with kind Trigger: Internal error occurred: failed calling webhook "webhook.triggers.tekton.dev": failed to call webhook: Post "https://tekton-triggers-webhook.openshift-pipelines.svc:443/defaulting?timeout=10s": service "tekton-triggers-webhook" not found && cannot patch "ort" with kind Trigger: Internal error occurred: failed calling webhook "webhook.triggers.tekton.dev": failed to call webhook: Post "https://tekton-triggers-webhook.openshift-pipelines.svc:443/defaulting?timeout=10s": service "tekton-triggers-webhook" not found && cannot patch "dev" with kind Trigger: Internal error occurred: failed calling webhook "webhook.triggers.tekton.dev": failed to call webhook: Post "https://tekton-triggers-webhook.openshift-pipelines.svc:443/defaulting?timeout=10s": service "tekton-triggers-webhook" not found && cannot patch "promote-image" with kind TriggerBinding: Internal error occurred: failed calling webhook "webhook.triggers.tekton.dev": failed to call webhook: Post "https://tekton-triggers-webhook.openshift-pipelines.svc:443/defaulting?timeout=10s": service "tekton-triggers-webhook" not found && cannot patch "develop-build-deploy" with kind TriggerBinding: Internal error occurred: failed calling webhook "webhook.triggers.tekton.dev": failed to call webhook: Post "https://tekton-triggers-webhook.openshift-pipelines.svc:443/defaulting?timeout=10s": service "tekton-triggers-webhook" not found && cannot patch "ort" with kind TriggerBinding: Internal error occurred: failed calling webhook "webhook.triggers.tekton.dev": failed to call webhook: Post "https://tekton-triggers-webhook.openshift-pipelines.svc:443/defaulting?timeout=10s": service "tekton-triggers-webhook" not found && cannot patch "dev" with kind TriggerBinding: Internal error occurred: failed calling webhook "webhook.triggers.tekton.dev": failed to call webhook: Post "https://tekton-triggers-webhook.openshift-pipelines.svc:443/defaulting?timeout=10s": service "tekton-triggers-webhook" not found && cannot patch "promote-image" with kind TriggerTemplate: Internal error occurred: failed calling webhook "webhook.triggers.tekton.dev": failed to call webhook: Post "https://tekton-triggers-webhook.openshift-pipelines.svc:443/defaulting?timeout=10s": service "tekton-triggers-webhook" not found && cannot patch "develop-build-deploy" with kind TriggerTemplate: Internal error occurred: failed calling webhook "webhook.triggers.tekton.dev": failed to call webhook: Post "https://tekton-triggers-webhook.openshift-pipelines.svc:443/defaulting?timeout=10s": service "tekton-triggers-webhook" not found && cannot patch "ort" with kind TriggerTemplate: Internal error occurred: failed calling webhook "webhook.triggers.tekton.dev": failed to call webhook: Post "https://tekton-triggers-webhook.openshift-pipelines.svc:443/defaulting?timeout=10s": service "tekton-triggers-webhook" not found && cannot patch "dev" with kind TriggerTemplate: Internal error occurred: failed calling webhook "webhook.triggers.tekton.dev": failed to call webhook: Post "https://tekton-triggers-webhook.openshift-pipelines.svc:443/defaulting?timeout=10s": service "tekton-triggers-webhook" not found
Error: UPGRADE FAILED: cannot patch "dev-listener" with kind EventListener: Internal error occurred: failed calling webhook "webhook.triggers.tekton.dev": failed to call webhook: Post "https://tekton-triggers-webhook.openshift-pipelines.svc:443/defaulting?timeout=10s": service "tekton-triggers-webhook" not found && cannot patch "buildah-build" with kind Task: admission webhook "webhook.pipeline.tekton.dev" denied the request: mutation failed: cannot decode incoming new object: json: unknown field "type" && cannot patch "git-clone" with kind Task: admission webhook "webhook.pipeline.tekton.dev" denied the request: mutation failed: cannot decode incoming new object: json: unknown field "type" && cannot patch "kaniko-build" with kind Task: admission webhook "webhook.pipeline.tekton.dev" denied the request: mutation failed: cannot decode incoming new object: json: unknown field "type" && cannot patch "get-image-tag" with kind Task: admission webhook "webhook.pipeline.tekton.dev" denied the request: mutation failed: cannot decode incoming new object: json: unknown field "type" && cannot patch "helm-deploy" with kind Task: admission webhook "webhook.pipeline.tekton.dev" denied the request: mutation failed: cannot decode incoming new object: json: unknown field "value" && cannot patch "promote-image" with kind Trigger: Internal error occurred: failed calling webhook "webhook.triggers.tekton.dev": failed to call webhook: Post "https://tekton-triggers-webhook.openshift-pipelines.svc:443/defaulting?timeout=10s": service "tekton-triggers-webhook" not found && cannot patch "develop-build-deploy" with kind Trigger: Internal error occurred: failed calling webhook "webhook.triggers.tekton.dev": failed to call webhook: Post "https://tekton-triggers-webhook.openshift-pipelines.svc:443/defaulting?timeout=10s": service "tekton-triggers-webhook" not found && cannot patch "ort" with kind Trigger: Internal error occurred: failed calling webhook "webhook.triggers.tekton.dev": failed to call webhook: Post "https://tekton-triggers-webhook.openshift-pipelines.svc:443/defaulting?timeout=10s": service "tekton-triggers-webhook" not found && cannot patch "dev" with kind Trigger: Internal error occurred: failed calling webhook "webhook.triggers.tekton.dev": failed to call webhook: Post "https://tekton-triggers-webhook.openshift-pipelines.svc:443/defaulting?timeout=10s": service "tekton-triggers-webhook" not found && cannot patch "promote-image" with kind TriggerBinding: Internal error occurred: failed calling webhook "webhook.triggers.tekton.dev": failed to call webhook: Post "https://tekton-triggers-webhook.openshift-pipelines.svc:443/defaulting?timeout=10s": service "tekton-triggers-webhook" not found && cannot patch "develop-build-deploy" with kind TriggerBinding: Internal error occurred: failed calling webhook "webhook.triggers.tekton.dev": failed to call webhook: Post "https://tekton-triggers-webhook.openshift-pipelines.svc:443/defaulting?timeout=10s": service "tekton-triggers-webhook" not found && cannot patch "ort" with kind TriggerBinding: Internal error occurred: failed calling webhook "webhook.triggers.tekton.dev": failed to call webhook: Post "https://tekton-triggers-webhook.openshift-pipelines.svc:443/defaulting?timeout=10s": service "tekton-triggers-webhook" not found && cannot patch "dev" with kind TriggerBinding: Internal error occurred: failed calling webhook "webhook.triggers.tekton.dev": failed to call webhook: Post "https://tekton-triggers-webhook.openshift-pipelines.svc:443/defaulting?timeout=10s": service "tekton-triggers-webhook" not found && cannot patch "promote-image" with kind TriggerTemplate: Internal error occurred: failed calling webhook "webhook.triggers.tekton.dev": failed to call webhook: Post "https://tekton-triggers-webhook.openshift-pipelines.svc:443/defaulting?timeout=10s": service "tekton-triggers-webhook" not found && cannot patch "develop-build-deploy" with kind TriggerTemplate: Internal error occurred: failed calling webhook "webhook.triggers.tekton.dev": failed to call webhook: Post "https://tekton-triggers-webhook.openshift-pipelines.svc:443/defaulting?timeout=10s": service "tekton-triggers-webhook" not found && cannot patch "ort" with kind TriggerTemplate: Internal error occurred: failed calling webhook "webhook.triggers.tekton.dev": failed to call webhook: Post "https://tekton-triggers-webhook.openshift-pipelines.svc:443/defaulting?timeout=10s": service "tekton-triggers-webhook" not found && cannot patch "dev" with kind TriggerTemplate: Internal error occurred: failed calling webhook "webhook.triggers.tekton.dev": failed to call webhook: Post "https://tekton-triggers-webhook.openshift-pipelines.svc:443/defaulting?timeout=10s": service "tekton-triggers-webhook" not found
helm.go:84: [debug] cannot patch "dev-listener" with kind EventListener: Internal error occurred: failed calling webhook "webhook.triggers.tekton.dev": failed to call webhook: Post "https://tekton-triggers-webhook.openshift-pipelines.svc:443/defaulting?timeout=10s": service "tekton-triggers-webhook" not found && cannot patch "buildah-build" with kind Task: admission webhook "webhook.pipeline.tekton.dev" denied the request: mutation failed: cannot decode incoming new object: json: unknown field "type" && cannot patch "git-clone" with kind Task: admission webhook "webhook.pipeline.tekton.dev" denied the request: mutation failed: cannot decode incoming new object: json: unknown field "type" && cannot patch "kaniko-build" with kind Task: admission webhook "webhook.pipeline.tekton.dev" denied the request: mutation failed: cannot decode incoming new object: json: unknown field "type" && cannot patch "get-image-tag" with kind Task: admission webhook "webhook.pipeline.tekton.dev" denied the request: mutation failed: cannot decode incoming new object: json: unknown field "type" && cannot patch "helm-deploy" with kind Task: admission webhook "webhook.pipeline.tekton.dev" denied the request: mutation failed: cannot decode incoming new object: json: unknown field "value" && cannot patch "promote-image" with kind Trigger: Internal error occurred: failed calling webhook "webhook.triggers.tekton.dev": failed to call webhook: Post "https://tekton-triggers-webhook.openshift-pipelines.svc:443/defaulting?timeout=10s": service "tekton-triggers-webhook" not found && cannot patch "develop-build-deploy" with kind Trigger: Internal error occurred: failed calling webhook "webhook.triggers.tekton.dev": failed to call webhook: Post "https://tekton-triggers-webhook.openshift-pipelines.svc:443/defaulting?timeout=10s": service "tekton-triggers-webhook" not found && cannot patch "ort" with kind Trigger: Internal error occurred: failed calling webhook "webhook.triggers.tekton.dev": failed to call webhook: Post "https://tekton-triggers-webhook.openshift-pipelines.svc:443/defaulting?timeout=10s": service "tekton-triggers-webhook" not found && cannot patch "dev" with kind Trigger: Internal error occurred: failed calling webhook "webhook.triggers.tekton.dev": failed to call webhook: Post "https://tekton-triggers-webhook.openshift-pipelines.svc:443/defaulting?timeout=10s": service "tekton-triggers-webhook" not found && cannot patch "promote-image" with kind TriggerBinding: Internal error occurred: failed calling webhook "webhook.triggers.tekton.dev": failed to call webhook: Post "https://tekton-triggers-webhook.openshift-pipelines.svc:443/defaulting?timeout=10s": service "tekton-triggers-webhook" not found && cannot patch "develop-build-deploy" with kind TriggerBinding: Internal error occurred: failed calling webhook "webhook.triggers.tekton.dev": failed to call webhook: Post "https://tekton-triggers-webhook.openshift-pipelines.svc:443/defaulting?timeout=10s": service "tekton-triggers-webhook" not found && cannot patch "ort" with kind TriggerBinding: Internal error occurred: failed calling webhook "webhook.triggers.tekton.dev": failed to call webhook: Post "https://tekton-triggers-webhook.openshift-pipelines.svc:443/defaulting?timeout=10s": service "tekton-triggers-webhook" not found && cannot patch "dev" with kind TriggerBinding: Internal error occurred: failed calling webhook "webhook.triggers.tekton.dev": failed to call webhook: Post "https://tekton-triggers-webhook.openshift-pipelines.svc:443/defaulting?timeout=10s": service "tekton-triggers-webhook" not found && cannot patch "promote-image" with kind TriggerTemplate: Internal error occurred: failed calling webhook "webhook.triggers.tekton.dev": failed to call webhook: Post "https://tekton-triggers-webhook.openshift-pipelines.svc:443/defaulting?timeout=10s": service "tekton-triggers-webhook" not found && cannot patch "develop-build-deploy" with kind TriggerTemplate: Internal error occurred: failed calling webhook "webhook.triggers.tekton.dev": failed to call webhook: Post "https://tekton-triggers-webhook.openshift-pipelines.svc:443/defaulting?timeout=10s": service "tekton-triggers-webhook" not found && cannot patch "ort" with kind TriggerTemplate: Internal error occurred: failed calling webhook "webhook.triggers.tekton.dev": failed to call webhook: Post "https://tekton-triggers-webhook.openshift-pipelines.svc:443/defaulting?timeout=10s": service "tekton-triggers-webhook" not found && cannot patch "dev" with kind TriggerTemplate: Internal error occurred: failed calling webhook "webhook.triggers.tekton.dev": failed to call webhook: Post "https://tekton-triggers-webhook.openshift-pipelines.svc:443/defaulting?timeout=10s": service "tekton-triggers-webhook" not found
helm.sh/helm/v3/pkg/kube.(*Client).Update
        helm.sh/helm/v3/pkg/kube/client.go:263
helm.sh/helm/v3/pkg/action.(*Upgrade).releasingUpgrade
        helm.sh/helm/v3/pkg/action/upgrade.go:376
runtime.goexit
        runtime/asm_arm64.s:1133
UPGRADE FAILED
main.newUpgradeCmd.func2
        helm.sh/helm/v3/cmd/helm/upgrade.go:199
github.com/spf13/cobra.(*Command).execute
        github.com/spf13/cobra@v1.3.0/command.go:856
github.com/spf13/cobra.(*Command).ExecuteC
        github.com/spf13/cobra@v1.3.0/command.go:974
github.com/spf13/cobra.(*Command).Execute
        github.com/spf13/cobra@v1.3.0/command.go:902
main.main
        helm.sh/helm/v3/cmd/helm/helm.go:83
runtime.main
        runtime/proc.go:255
runtime.goexit
        runtime/asm_arm64.s:1133
```

Problem:
Type mismatch in `taskdefinition[].params`, the only accepted values are below:

- name
- default
- description
- type

Solution:

Ensure any fields under `taskdefinitions.tasks[].params` have the correct types for example only `name` and `type`:

```yaml
taskdefinitions:
  tasks:
  - name: ecr-build-push
    params:
    - name: app_short_name
      type: string
```

Problem:


```
tekton-helm-chart$ cd examples/tekton-buildah-build-deploy
source ../../.auth/dockerhub.env
export SLACK_WEBHOOK_URI=https://hooks.slack.com/services/TJL9A5PMJ/B03KPQ2V4JG/DUMMY
export SSH_KEY_LOCATION=../../.auth/id_rsa
docker_auth="$(echo -n "${DOCKERHUB_USERNAME}":"${DOCKERHUB_PASSWORD}" | base64)"
tee "config.json" > /dev/null <<EOF
{"auths":{"https://index.docker.io/v1/":{"auth":"$docker_auth","email":"thisemail@isignored.com"}}}
EOF
helm upgrade --install pipelines -n tekton-pipelines ../../charts/tekton --set github_token="$(echo -n "ENTERTOKEN" | base64)" --set secret_ssh_key="$(cat $SSH_KEY_LOCATION)" --set-file=docker_config_json=config.json --values ./values-override.yaml
WARNING: Kubernetes configuration file is group-readable. This is insecure. Location: /Users/george/.kube/config_kind
WARNING: Kubernetes configuration file is world-readable. This is insecure. Location: /Users/george/.kube/config_kind
Release "pipelines" does not exist. Installing it now.
Error: admission webhook "validation.webhook.pipeline.tekton.dev" denied the request: validation failed: invalid value: couldn't add link between rolling-update and buildah-build: task rolling-update depends on buildah-build but buildah-build wasn't present in Pipeline: spec.tasks
```


Solution: 

A `runAfter` statement is referencing a task name that does not exist in the pipeline.

For example this input file may have caused the error

`values-override.yaml`
```yaml
    taskcall:
    - name: git-clone
      taskRef:
        name: "git-clone"
      params:
      - name: url
        value: git@github.com:cogitogroupltd/docker-nginx-hello-world
      - name: revision #revision/commit
        value: $(params.git_revision)
      workspaces:
      - name: ssh-directory
        workspace: ssh-creds
      - name: output
        workspace: git-pvc
    - name: buildah-build-push
      taskRef:
        name: buildah-build
      params:
      - name: IMAGE
        value: cogitoexample/docker-nginx-hello-world
      runAfter:
      - git-clone
      workspaces:
      - name: source
        workspace: git-pvc
      - name: dockerconfig
        workspace: docker-creds-cm
    - name: rolling-update
      taskRef:
        name: rolling-update
      params:
      - name: deployment
        value: nginx-app
      - name: namespace
        value: default
      - name: tag
        value: $(params.git_revision)
      - name: git_repository_name
        value: $(params.git_repository_name)
      - name: docker_registry
        value: cogitoexample
      - name: docker_repository
        value: docker-nginx-hello-world
      runAfter:
      - buildah-build
```

This is because the `runAfter` should reference the name `buildah-build-push`
```yaml
      runAfter:
      - buildah-build
```