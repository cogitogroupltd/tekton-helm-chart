ARG version=latest-alpine-jdk11
FROM --platform=linux/arm64 jenkins/agent:$version

ARG version
ARG user=jenkins

LABEL Description="This is a base image which can be used as a CI/CD agent" Vendor="project" Version="$version"


# AWSCLI version, if this changes please change boto3 and botocore pip installs at the bottom.
ENV AWSCLI_VERSION=1.18.127

# 
# Install the entrypoint
#
USER root
COPY jenkins-agent /usr/local/bin/jenkins-agent
RUN chmod +x /usr/local/bin/jenkins-agent &&\
    ln -s /usr/local/bin/jenkins-agent /usr/local/bin/jenkins-slave

# Update the list of packages and upgrade
RUN apk -U upgrade

# Install envsubst command for replacing config files in system startup
# - it needs libintl package
# - only weights 100KB combined with it's libraries
RUN apk add gettext libintl 

# Install Trivy
# Git commit hash references release tag v0.12 
RUN apk add curl \ 
    && curl -sfL https://raw.githubusercontent.com/aquasecurity/trivy/49691ba85e9e0f94546b031b3a8b80b3ba949f0f/contrib/install.sh | sh -s -- -b /usr/local/bin
    #&& trivy filesystem --exit-code 1 --no-progress /

#
# Install Kubectl and Helm
#
# Note: Latest version of kubectl may be found at:
# https://github.com/kubernetes/kubernetes/releases
ENV KUBE_LATEST_VERSION="v1.20.4"
# Note: Latest version of helm may be found at
# https://github.com/kubernetes/helm/releases
ENV HELM_VERSION="v3.6.3"
RUN apk add --no-cache ca-certificates bash git openssh curl jq zip \
    && wget -q https://storage.googleapis.com/kubernetes-release/release/${KUBE_LATEST_VERSION}/bin/linux/amd64/kubectl -O /usr/local/bin/kubectl \
    && chmod +x /usr/local/bin/kubectl \
    && wget -q https://get.helm.sh/helm-${HELM_VERSION}-linux-amd64.tar.gz -O - | tar -xzO linux-amd64/helm > /usr/local/bin/helm \
    && chmod +x /usr/local/bin/helm \
    && chmod g+rwx /root \
    && mkdir /config \
    && chmod g+rwx /config 

#
# Install Docker
#
RUN apk add --update docker openrc
RUN rc-update add docker boot

#
# Install AWSCli
#
RUN apk -Uuv add groff less py-pip
RUN pip install awscli==${AWSCLI_VERSION}
RUN rm /var/cache/apk/*

#
# Install NPM
#
RUN apk update \
    && apk add nodejs=16.16.0-r0 npm \
    && node -v \
    && npm -v

#
# Install Dependencies for scripts
#
RUN apk add --no-cache python3 alpine-sdk 

#
# Install dig/nslookup (bindtools) and checksumdir
#
RUN apk add bind-tools \
    && pip install checksumdir

# Install terraform 
ENV TERRAFORM_VERSION=1.0.11
RUN wget https://releases.hashicorp.com/terraform/${TERRAFORM_VERSION}/terraform_${TERRAFORM_VERSION}_linux_amd64.zip
RUN unzip terraform_${TERRAFORM_VERSION}_linux_amd64.zip && rm terraform_${TERRAFORM_VERSION}_linux_amd64.zip
RUN mv terraform /usr/bin/terraform
RUN terraform version


# Setup profile 
RUN echo 'echo' >> ~/.bashrc && \
    echo 'echo "==========================="' >> ~/.bashrc && \
    echo 'terraform --version' >> ~/.bashrc && \
    echo 'echo "==========================="' >> ~/.bashrc && \
    echo 'echo' >> ~/.bashrc && \
    echo 'alias tf=terraform' >> ~/.bashrc && \
    echo 'echo' >> ~/.bashrc 


# Add fontconfig libraries for libSkiaSharp
RUN apk add --no-cache fontconfig fontconfig-dev fontconfig-static


# USER ${user}
WORKDIR /home/jenkins/

ENTRYPOINT ["jenkins-agent"]
