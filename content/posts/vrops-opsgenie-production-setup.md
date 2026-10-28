---
title: "Configure vROps To Send Alerts to OpsGenie and Microsoft Teams"
date: 2021-07-23T18:35:59-04:00
lastmod: 2021-07-27T12:53:28-04:00
slug: "vrops-opsgenie-production-setup"
url: /2021/07/23/vrops-opsgenie-production-setup/
author:
  - "jhowe"
year: ["2021"]
month: ["2021-07"]
categories:
  - "automation"
  - "hashicorp"
  - "infrastructureascode"
  - "packer"
  - "python"
  - "scripting"
  - "vexpert"
  - "vmware"
tags: []
aliases:
  - "/2021/07/23/vrops-opsgenie-production-setup/feed/"
---

Packer, Photon, Python, Flask, WSGI, vROps. Holy smokes folks.. I’m not sure I could make a more click-bait-y post if I tried!

I recently took a position at a new company and had the opportunity to stand up a greenfield environment. Part of this environment was obviously configuring monitoring. Since we’re pretty heavily tied to VMware here, we’re using vROps for our monitoring. For escalation of alerts, we’re using OpsGenie, and for normal collaboration we’re using Teams. Unfortunately, vROps versions older than 8.4 do not support sending alerts to OpsGenie or Teams out of the box. Fortunately, we can still get this working with a bit of work.

<!--more-->

Table of Contents

Toggle

- [Overview](#Overview "Overview")
- [Approach](#Approach "Approach")
- [Create Photon Packer Template](#Create_Photon_Packer_Template "Create Photon Packer Template")
  - [Create Custom ISO](#Create_Custom_ISO "Create Custom ISO")
  - [Use Packer To Create vSphere Template](#Use_Packer_To_Create_vSphere_Template "Use Packer To Create vSphere Template")
- [Deploy Photon 4 VM](#Deploy_Photon_4_VM "Deploy Photon 4 VM")
- [Configure Server](#Configure_Server "Configure Server")
  - [Install Packages](#Install_Packages "Install Packages")
  - [Configure Shims](#Configure_Shims "Configure Shims")
    - [Configure Teams](#Configure_Teams "Configure Teams")
    - [Configure OpsGenie](#Configure_OpsGenie "Configure OpsGenie")
    - [Disable Unused Shims](#Disable_Unused_Shims "Disable Unused Shims")
    - [Disable Welcome Page](#Disable_Welcome_Page "Disable Welcome Page")
- [Configure Systemd](#Configure_Systemd "Configure Systemd")
- [Configure Nginx](#Configure_Nginx "Configure Nginx")
- [Enable and Start All Services](#Enable_and_Start_All_Services "Enable and Start All Services")
- [Configure vRealize Operations Manager](#Configure_vRealize_Operations_Manager "Configure vRealize Operations Manager")
  - [Add a New Rest Notification Plugin](#Add_a_New_Rest_Notification_Plugin "Add a New Rest Notification Plugin")
    - [OpsGenie](#OpsGenie "OpsGenie")
    - [Teams](#Teams "Teams")
- [References](#References "References")

## Overview

Update – Starting in vROps 8.4 you can use the webhook plugin that is delivered with vROps to accomplish this. [**LINK**](https://docs.vmware.com/en/vRealize-Operations-Manager/8.4/com.vmware.vcom.core.doc/GUID-9314313D-1DE6-4160-AEFD-76B23AB5DAD9.html)

While vROps does have the ability to send outgoing notifications via REST API, it doesn’t have the ability to let you customize what fields are sent, or how they are formatted. Because of this limitation, [some very thoughtful folks](https://github.com/vmw-loginsight/webhook-shims/graphs/contributors) created [a project called webhook-shims](https://github.com/vmw-loginsight/webhook-shims). This is essentially a Python Flask project that accepts web requests, translates them, then forwards the correctly formatted request off to whatever system you want notifications sent to.

This project hasn’t been updated in over 3 years, has a number of pending PR’s and Issues, so my spidey sense says it’s likely dead. So please be smart about how and where you use this, and consider the implications of running this in production. That said, from a functional standpoint, it seems to work well, and in the rest of this post I’ll go over how to set this up to run in a production fashion.

The list to the right are the applications that the project supports, and the bold items are what I’ll show example configuration for.

- bigpanda
- bugzilla
- groove
- hipchat
- jenkins
- jira
- kafkatopic
- **opsgenie**
- pagerduty
- pivotaltracker
- pushbullet
- servicenow
- slack
- socialcast
- travisci
- vrealizeorchestrator
- zendesk
- moogsoft
- **msteams**

## Approach

We’ll be running this whole project using Photon OS 4.

While we could simply run the python script in a [screen](https://www.gnu.org/software/screen/), [tmux](https://github.com/tmux/tmux/wiki), or similar session, but there are serious limitations in doing that. Admittedly, my python isn’t as strong as some of my other scripting languages, but after a bit of digging, it became clear that things like security, performance, and monitoring are either limited or unavailable if we do this. We’ll use a WSGI server called [Gunicorn](https://gunicorn.org/) to run the python script, and use systemd to create a socket and service, and finally, use Nginx to connect directly to the socket. Whew! Even just reading that after completing this entire project feels like a lot, but don’t worry. As always, I’ll explain each step in detail and give you code to create this project.

## Create Photon Packer Template

If you don’t know this about me by now, I’m a huge fan of packer. As such, we’ll be using it to create a template. You can find the source code for this packer template on [my website’s github repository](https://github.com/jonhowe/Virtjunkie.com/tree/master/Packer/PhotonOS4)

To get a local copy, run the following command:

git clone https://github.com/jonhowe/Virtjunkie.com.git

You can find all source code in the directory Virtjunkie.com/Packer/PhotonOS4.

### Create Custom ISO

Unfortunately, Photon OS, even in v4, doesn’t support providing the kickstart file via CD-ROM or floppy (see [Issue#1113](https://github.com/vmware/photon/issues/1113), [Issue#798)](https://github.com/vmware/photon/issues/798). Unfortunately, this means that if we want (or need) to use the vsphere-iso builder, we’ll need to create an ISO with the kickstart file embedded. [I’m not going to duplicate documentation, so here’s the official documentation from VMware on how to add a kickstart file.](https://vmware.github.io/photon/docs/user-guide/working-with-kickstart/#building-an-iso-with-a-kickstart-config-file)

Instead of using the sample my\_ks.cfg file provided in the ISO, use the version below.

IMPORTANT: Ensure that you replace [yourpassword] with your actual password

<script src="https://gist.github.com/jonhowe/7da290c7cfd660ddb220c96349d0f024.js"></script>

### Use Packer To Create vSphere Template

IMPORTANT: Ensure that the password assigned to “root\_password” in Virtjunkie.com/Packer/PhotonOS4/packer-photon.json.pkr.hcl matches what is set in the kickstart file above

```text
packer build -var-file=nable.auto.pkrvars.hcl -var-file=vars iso-local-4.0GA.json -only=vsphere-iso.vmware-template packer-photon.json.pkr.hcl
```

## Deploy Photon 4 VM

For production systems, I typically use Terraform to deploy my VMs, and that’s what I did. I’m not going to go over that, as I’ve done it before. If nothing else, just deploy the VM from a template, assign it a static IP in the guest customization specification, and then log in using credentials set in the kickstart file.

## Configure Server

### Install Packages

Execute the commands below to install required packages, and to clone the repository

<script src="https://gist.github.com/jonhowe/b66c9d6881db4ec00c30852d292f6102.js"></script>

### Configure Shims

There’s a bit of config we’ll need to do in order to make this production ready.

#### Configure Teams

A fellow VMware vExpert, Shane Moore has an excellent article. So that I don’t recreate the wheel, please [see his instructions](https://www.virtuallyshane.com/posts/how-to-send-vrealize-operations-alerts-into-microsoft-teams) for how to prep your environment to use Microsoft Teams.

In short, you’ll create a webhook connector in the Microsoft Teams channel, and plug the URL that you get from Teams into the teams shim file.

#### Configure OpsGenie

OpsGenie is pretty simple. All we’ll need to do is create an integration by selecting your team in Opsgenie, navigating to Integrations, then selecting Add Integration.

- [![](/wp-content/uploads/2021/07/image-1536x207.png)](/wp-content/uploads/2021/07/image-1024x138.png)

In the resulting list of available integrations, select API.

- [![](/wp-content/uploads/2021/07/image-1.png)](/wp-content/uploads/2021/07/image-1.png)

Then note the API key (you can grab it later, it doesn’t disappear when you navigate away). We’ll use that when we configure outbound settings in vROps to use OpsGenie.

#### Disable Unused Shims

In my environment, I’m only going to be using Teams and OpsGenie alerts. To reduce bloat and access points that could cause me security issues, I’m disabling all shims not in use.

Edit the file
loginsightwebhookdemo/webhook-shims/loginsightwebhookdemo/\_\_init\_\_.py

<script src="https://gist.github.com/jonhowe/1d6fa1a003732c7200ec1ca28e509751.js"></script>

#### Disable Welcome Page

This could probably be optional, but I appreciate not having a welcome/hello world webpage open for a production service. We’ll disable it.

Edit the file
loginsightwebhookdemo/webhook-shims/loginsightwebhookdemo/\_\_init\_\_.py

<script src="https://gist.github.com/jonhowe/872a49c369ee36ff9bee6be431572a49.js"></script>

## Configure Systemd

Create two files:
/etc/systemd/system/gunicorn.service and
/etc/systemd/system/gunicorn.socket and populate with the text below.

/etc/systemd/system/gunicorn.service

This service file ensures that Gunicorn is started the same way, and is managed by systemd. You’ll note that it *requires* gunicorn.socket, which we will create later.

<script src="https://gist.github.com/jonhowe/e6b1d294dca6235f00b80c58a6f31af6.js"></script>

/etc/systemd/system/gunicorn.socket

This socket file sets permissions for the socket assigned to gunicorn

<script src="https://gist.github.com/jonhowe/8398a06c4395763a82faa480de19206e.js"></script>

## Configure Nginx

Replace the file
/etc/nginx/nginx.conf with the contents below

This is telling Nginx to connect directly to the socket we’re creating with the systemd socket gunicorn.socket we created earlier.

<script src="https://gist.github.com/jonhowe/78964d1cc4a32bf5e13a7369a36eaa13.js"></script>

## Enable and Start All Services

Finally, enable, and start both services, and restart Nginx

```bash
systemctl enable gunicorn.socket
systemctl enable gunicorn.service
systemctl restart gunicorn.socket 
systemctl restart gunicorn.service
systemctl restart nginx.service
```

## Configure vRealize Operations Manager

At this point, all we need to do is configure an outbound instance for Microsoft Teams and OpsGenie.

### Add a New Rest Notification Plugin

#### OpsGenie

To do this, sign into vROps, and navigate to Administration ->Management->Outbound Settings, or https://[Your\_vROps\_URL]/ui/index.action#/administration/outbound-alert-settings

- [![](/wp-content/uploads/2021/07/image-2-300x166.png)](/wp-content/uploads/2021/07/image-2.png)

After you select the Rest Notification Plugin, there are 3 fields required in the Add/Edit Outbound Instance box

|  |  |  |
| --- | --- | --- |
| Item | Description | Example |
| Instance Name | Name of the rest notification plugin created | Opsgenie |
| URL | URL to OpsGenie shim endpoint | http://<IP or Hostname of Photon VM>/endpoint/opsgenie/<api key> |
| Content Type | Content Type – Unless you’re working with a SOAP API (which we aren’t), this will always be application/json |  |

- [![](/wp-content/uploads/2021/07/image-3.png)](/wp-content/uploads/2021/07/image-3.png)

Finally, navigate to Alerts -> Configuration -> Notification (https://[Your\_vROps\_URL]/ui/index.action#/alerts/notifications) and add a new rule that targets the adapter you just created.

- [![](/wp-content/uploads/2021/07/image-4-768x423.png)](/wp-content/uploads/2021/07/image-4.png)

#### Teams

Again, I’m not in the business of recreating the wheel, [so check out Shane’s blog for info on how to do this](https://www.virtuallyshane.com/posts/how-to-send-vrealize-operations-alerts-into-microsoft-teams).

## References

|  |  |
| --- | --- |
| <https://www.virtuallyshane.com/posts/how-to-send-vrealize-operations-alerts-into-microsoft-teams> | Fellow vExpert Shane Moore’s article for setting MS Teams forwarding |
| <https://github.com/vmw-loginsight/webhook-shims> | Official Github site for the webhook-shims project |
| <https://blogs.vmware.com/management/2017/01/vrealize-webhooks-infinite-integrations.html> | VMware Blog article that got me started on this journey |
| <https://vmware.github.io/photon/docs/user-guide/working-with-kickstart/> | VMware Photon documentation |
| <https://github.com/vmware/photon/issues/1113> | Github Issue for presenting Kickstart file to Photon over cdrom/floppy |
| <https://github.com/vmware/photon/issues/798> | Another Github Issue for presenting Kickstart file to Photon over cdrom/floppy |
