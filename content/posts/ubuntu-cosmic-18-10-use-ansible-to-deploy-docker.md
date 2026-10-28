---
title: "Ubuntu Cosmic 18.10 – Use Ansible To Deploy Docker"
date: 2018-12-14T17:45:36-05:00
slug: "ubuntu-cosmic-18-10-use-ansible-to-deploy-docker"
url: /2018/12/14/ubuntu-cosmic-18-10-use-ansible-to-deploy-docker/
author:
  - "jhowe"
year: ["2018"]
month: ["2018-12"]
categories:
  - "ansible"
  - "automation"
  - "docker"
  - "linux"
  - "ubuntu"
tags: []
aliases:
  - "/2018/12/14/ubuntu-cosmic-18-10-use-ansible-to-deploy-docker/feed/"
---

As it turns out, Docker doesn’t [officially support](https://docs.docker.com/v17.09/engine/installation/linux/docker-ce/ubuntu/#os-requirements) any version of Ubuntu past Artful. This is a bit of a challenge if you want to use a state configuration manager such as Ansible to deploy Docker, or even if you want to install it manually. I was able to get this working by using the test branch of the docker release for Ubuntu Cosmic.

<!--more-->

 I found a [popular role in Ansible Galaxy](https://galaxy.ansible.com/geerlingguy/docker) with a ton of installs, but the documentation that comes with it doesn’t work, which is fine… not a supported version, etc. I used the steps below to get it working.

Please be aware, the test branch is likely not stable, and shouldn’t be used for production. Follow this at your own risk.

1.) Run the command below to install the role

```text
root@server:~$ ansible-galaxy install geerlingguy.docker
```

2.) Create a text file named “install-docker.yml”  
  – The value assigned to docker\_apt\_release\_channel being “test”.  
  – Add your own username(s) under “docker\_users”  
(This yaml file is located on my github page here: <https://github.com/jonhowe/Virtjunkie.com/blob/master/install-docker.yml>)

```text
---
- name: Install Docker
  hosts: all
  become: yes
  become_method: sudo
  tasks:
  - name: Install Docker and docker-compose
    include_role:
       name: geerlingguy.docker
    vars:
       - docker_edition: 'ce'
       - docker_apt_release_channel: test
       - docker_package_state: present
       - docker_install_compose: true
       - docker_compose_version: "1.22.0"
       - docker_users:
          - jhowe
```

3.) Then it’s as easy as running the playbook

```text
root@server:~$ ansible-playbook -K install-docker.yml
```
