# OpsTrack Ansible Deployment

This directory contains an Ansible playbook that converts a clean Ubuntu server into a working OpsTrack application server.

The playbook installs Docker, deploys the containerized application stack and verifies the application health automatically.

## Architecture

The Mac acts as the Ansible control node and connects to the managed Ubuntu server over SSH.

The managed server runs:

- Nginx as the public reverse proxy
- Two-network Docker Compose architecture
- OpsTrack using `wkavindu/opstrack:latest`
- MongoDB with persistent storage
- Health and readiness checks

## Requirements

Control node:

- Ansible
- SSH client
- `community.docker` Ansible collection
- A dedicated SSH private key

Managed node:

- Ubuntu 24.04
- Python 3
- SSH access
- Passwordless sudo for the managed user

Ansible and Docker do not need to be preinstalled on the managed server.

## Install the Required Collection

From the repository root:

```bash
ansible-galaxy collection install \
  --requirements-file deploy/ansible/requirements.yml
```

## Configure the Inventory

Copy the safe example:

```bash
cp \
  deploy/ansible/inventory.example.ini \
  deploy/ansible/inventory.ini
```

Update `inventory.ini` with the server IP, SSH user and private-key path.

Example:

```ini
[webservers]
opstrack-server ansible_host=192.0.2.10

[webservers:vars]
ansible_user=ubuntu
ansible_ssh_private_key_file=~/.ssh/opstrack_ansible
ansible_python_interpreter=/usr/bin/python3
```

The real `inventory.ini` is excluded from Git.

## Test Connectivity

```bash
cd deploy/ansible

ansible webservers --module-name ping
```

Expected:

```text
"ping": "pong"
```

Test privilege escalation:

```bash
ansible webservers \
  --become \
  --module-name command \
  --args "whoami"
```

Expected:

```text
"stdout": "root"
```

If the SSH key uses a passphrase, load it into the SSH agent:

```bash
ssh-add ~/.ssh/opstrack_ansible
```

## Validate the Playbook

```bash
ansible-playbook --syntax-check playbook.yml

ansible-playbook playbook.yml --list-hosts

ansible-playbook playbook.yml --list-tasks
```

## Deploy OpsTrack

```bash
ansible-playbook playbook.yml
```

The playbook:

1. Updates the APT cache
2. Installs Docker and Docker Compose
3. Enables and starts Docker
4. Creates `/opt/opstrack`
5. Installs the Nginx configuration
6. Creates a protected environment file
7. Installs the Docker Compose definition
8. Starts the application stack
9. Verifies `/health`
10. Verifies `/ready`

## Idempotency Test

Run the same playbook again:

```bash
ansible-playbook playbook.yml
```

The second recap should report:

```text
changed=0
failed=0
unreachable=0
```

This proves the server already matches the desired configuration.

## Verify the Application

```bash
curl http://SERVER_IP/health

curl http://SERVER_IP/ready
```

Expected:

```json
{"service":"opstrack","status":"healthy"}
{"database":"connected","status":"ready"}
```

Check the managed containers:

```bash
ansible webservers \
  --become \
  --module-name command \
  --args "docker compose -f /opt/opstrack/compose.yaml ps"
```

## Secret Management

The application secret is generated locally by Ansible’s password lookup and saved in:

```text
deploy/ansible/.opstrack_secret
```

This file and the real inventory are excluded from Git.

On the server, the generated environment is stored at:

```text
/etc/opstrack.env
```

It is owned by `root:root` with mode `0600`.

Never commit either secret file or a private SSH key.

## Persistent Data

MongoDB data is stored in a named Docker volume. Application containers can be replaced without deleting the database.

Do not run `docker compose down --volumes` unless permanent database deletion is intended.

## Using This Playbook with AWS EC2

The same playbook can manage an Ubuntu EC2 instance by updating:

- `ansible_host` to the EC2 public IP
- `ansible_ssh_private_key_file` to the EC2 private key
- Security Group rules to allow SSH from the control node and HTTP on port 80

No application passwords or cloud credentials need to be stored in the playbook.