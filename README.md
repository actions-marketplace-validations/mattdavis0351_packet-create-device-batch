# GitHub Actions for creating devices within projects on Packet.com

## Automate your infrastructure

This GitHub Action will create a new device in an existing project on [packet.com](https://packet.com). Devices are compute resources available within your organization projects.

# Creating devices

With this action you can automate your workflow to by provisioning devices inside of projects using the [packet.com api](https://api.packet.net).

To use this action you will first need an [authentication token](https://www.packet.com/developers/api/authentication/) which can be generated through the [Packet Portal](https://app.packet.net/login?redirect=%2F%3F__woopraid%3DjUPDKi0tqtym).

You will also need a public/private key pair. [Learn how to generate keys](https://www.packet.com/developers/docs/servers/key-features/ssh-keys/) for either a user or a project.

**NEVER share your private key with anyone!**

**Packet.com is NOT a free service, so you will be asked to provide billing information. This action will NOT have access to that information.**

## Sample workflow that uses the packet-create-project action

```yaml
# File: .github/workflows/workflow.yml

on: [push]

name: Packet Project Sample

jobs:
  create-new-device:
    runs-on: ubuntu-latest
    name: Creating new device in existing packet project
    steps:
      - uses: mattdavis0351/packet-create-device@v1
        with:
          API_key: ${{ secrets.PACKET_API_KEY }}
          project_name: My Project
          host_name: actions-host
          plan: "t3.small.x86"
          facility: "sjc1"
          operating_system: "flatcar_stable"
          user_ssh_keys: ${{ secrets.PACKET_PUBLIC_KEY }}
```

## Available Inputs

| Input              | Description                                             | Default Value   | Required           |
| ------------------ | ------------------------------------------------------- | --------------- | ------------------ |
| `API_key`          | Packet.com API authorization token                      | No key supplied | :white_check_mark: |
| `project_name`     | Desired name for new project                            | GitHub Actions  | :white_check_mark: |
| `host_name`        | Desired host name for new device                        | default         | :white_check_mark: |
| `plan`             | Desired server type for device                          | default         | :white_check_mark: |
| `facility`         | Geographical location for device                        | default         | :white_check_mark: |
| `operating_system` | Desired operating system for device                     | default         | :white_check_mark: |
| `user_ssh_keys`    | SSH keys for any user account you wish to add to device |                 | :x:                |
| `project_ssh_keys` | Project level SSH keys for device                       |                 | :x:                |

## Outputs from action

This action supplies the following outputs which can be consumed by subsequent actions in the current job.

| Output         | Description                          |
| -------------- | ------------------------------------ |
| `ip_addresses` | IP addresses of newly created device |
| `device_id`    | ID of the newly created device       |
