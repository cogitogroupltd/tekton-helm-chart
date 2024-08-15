# Creating a new RSA key pair

```bash
cd tekton-helm-chart
# Generate .auth/id_rsa 
ssh-keygen -t rsa -f .auth/id_rsa -b 4096 -m PEM -q -N ""
```

## Associate SSH key pair with github

- Create a Github account

https://github.com/signup

- Login and navigate to Settings -> Keys 

https://github.com/settings/keys

- Click `New SSH key`

```
Title: <Type a friendly name here>
Key type: Authentication Key
Key: <Content of .auth/id_rsa.pub generated above>
```

# Removing passphrase from existing RSA key pair

```bash
encrypted_key="~/.ssh/id_rsa"
unencrypted_key=".auth/id_rsa"
openssl rsa -in $encrypted_key -out $unencrypted_key
```