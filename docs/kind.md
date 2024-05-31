# Install Kind Kubernetes cluster

PreRequisites:

- Docker
  - MacOS
    https://docs.docker.com/desktop/install/mac-install/
  - Windows
    https://docs.docker.com/desktop/install/windows-install/


For the most up-to-date instruction on how to install a local Kubernetes cluster using Kind (reference https://kind.sigs.k8s.io/docs/user/quick-start/)

- Download the binary for your operating system from [here](https://github.com/kubernetes-sigs/kind/releases)

For example for Kind CLI v0.22.0 on MacOS M1 click to download `kind-darwin-arm64`
https://github.com/kubernetes-sigs/kind/releases/tag/v0.22.0

- Move to a location on your computer for easy usage

```bash
chmod +x ~/Downloads/kind-darwin-arm64
mv ~/Downloads/kind-darwin-arm64 /usr/local/bin/kind
```

- Test it works!

```bash
$ kind version 
kind v0.22.0 go1.21.7 darwin/arm64
```




- Deploy Kind cluster (Mac M1)

```bash
kind create cluster --name kind --image=kindest/node:v1.22.0 --config cluster.yaml
kind get kubeconfig > ~/.kube/config_kind ;
# Configure current terminal to use Kind config for kubectl
export KUBECONFIG=~/.kube/config_kind
```


- Deploy Kind cluster (amd64)

```bash
unset DOCKER_DEFAULT_PLATFORM; kind create cluster --image=kindest/node:v1.22.0 --name kind --config cluster.yaml
kind get kubeconfig > ~/.kube/config_kind ;
# Configure current terminal to use Kind config for kubectl
export KUBECONFIG=~/.kube/config_kind
```