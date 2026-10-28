---
title: "Set Up Enpass With HTTPS Protected WebDAV and Ditch LastPass"
date: 2020-04-27T09:00:00-04:00
slug: "ditch-lastpass-for-enpass-webdav-https-traefik"
url: /2020/04/27/ditch-lastpass-for-enpass-webdav-https-traefik/
author:
  - "jhowe"
year: ["2020"]
month: ["2020-04"]
categories:
  - "docker"
  - "linux"
  - "security"
  - "servers"
tags: []
aliases:
  - "/ditch-lastpass-for-enpass-webdav-https-traefik/"
  - "/2020/04/27/ditch-lastpass-for-enpass-webdav-https-traefik/feed/"
---

It’s time to ditch cloud based password managers. There.. I said it. What we are doing when we use them is giving ownership and management of our trusted secrets to someone else, and hoping that they will be able to protect them from bad guys, and make sure they are available when we need them.

That’s a heck of an ask, isn’t it? I’ve been a LastPass customer for a very, very long time.. I use it to share secrets with my family, I use it on my mobile device to log into apps. It’s a safe bet to say it’s a critical piece of how I operate, and they have never once let me down. That said, if they asked for money to continue using their service, I’d have to pay. If they had a security event where secrets were compromised or if they lost my data, I’d be in very, very bad shape.

In this article, I will talk about how to set up a WebDAV share that’s protected by HTTPS using Traefik, Let’s Encrypt, and a WebDAV container on your own server, and use it to sync your secrets with devices.

<!--more-->

Before I begin, it’s important to understand that using WebDAV isn’t the only way to sync your secrets with Enpass. [There are others](https://www.enpass.io/docs/manual-desktop/sync.html#supclouds):

- Dropbox
- Google Drive
- OneDrive (Personal/Business)
- iCloud
- Box
- Folder sync

Table of Contents

Toggle

- [Base Server Set Up](#Base_Server_Set_Up "Base Server Set Up")
  - [Get a VPS](#Get_a_VPS "Get a VPS")
  - [Harden the OS](#Harden_the_OS "Harden the OS")
- [Set Up Docker, Traefik, and WebDAV](#Set_Up_Docker_Traefik_and_WebDAV "Set Up Docker, Traefik, and WebDAV")
  - [Create Traefik Configuration](#Create_Traefik_Configuration "Create Traefik Configuration")
    - [Create Traefik Configuration](#Create_Traefik_Configuration-2 "Create Traefik Configuration")
    - [Define Traefik Container](#Define_Traefik_Container "Define Traefik Container")
    - [Start Traefik Container](#Start_Traefik_Container "Start Traefik Container")
  - [Create WebDAV Configuration](#Create_WebDAV_Configuration "Create WebDAV Configuration")
    - [Define WebDAV Application Configuration](#Define_WebDAV_Application_Configuration "Define WebDAV Application Configuration")
    - [Start the WebDAV Container](#Start_the_WebDAV_Container "Start the WebDAV Container")
  - [Bringing it all together](#Bringing_it_all_together "Bringing it all together")
    - [Summary](#Summary "Summary")
    - [Final Directory Structure](#Final_Directory_Structure "Final Directory Structure")
- [Migrate to Enpass Using WebDAV](#Migrate_to_Enpass_Using_WebDAV "Migrate to Enpass Using WebDAV")
  - [Export Secrets From Lastpass](#Export_Secrets_From_Lastpass "Export Secrets From Lastpass")
  - [Import Secrets To Enpass](#Import_Secrets_To_Enpass "Import Secrets To Enpass")
  - [Connect EnPass To WebDav Share](#Connect_EnPass_To_WebDav_Share "Connect EnPass To WebDav Share")
- [Risks](#Risks "Risks")
- [Trafeik Resources](#Trafeik_Resources "Trafeik Resources")

## Base Server Set Up

### Get a VPS

First thing we need is a server that is public internet facing. The easiest way to do this is to use a service that provides virtual private servers. I like Vultr because of their price/performance/feature availability ratio. They are cheaper than DigitalOcean and AWS, as easy, if not easier to manage, and have the scale you need to put your data pretty much wherever you want. If you do use Vultr, please do me a favor and use [this link](https://www.vultr.com/?ref=8531966-6G) to sign up. I’ll get a little kickback, but you’ll get $100 USD to use on the site in your first month.

[![](/wp-content/uploads/2020/04/2020-04-26_09-57.png)](https://www.vultr.com/?ref=8531966-6G)

The OS doesn’t really matter, as long as you can install docker on it. A very small VPS will suffice, and mine costs $3.50 USD/Month.

### Harden the OS

I won’t go into very much depth with this subject, but here are a few general guidelines:

- Disable root login via SSH
- Require public key authentication for SSH sessions
- Enable multi factor authentication for your remote user
- Only install packages you need
- Ensure all updates are installed, and continue to do so on a regular basis

## Set Up Docker, Traefik, and WebDAV

All code is on the GitHub repository I use to share all code for this site. You can find it here: <https://github.com/jonhowe/Virtjunkie.com/tree/master/DitchLastPass>

First and foremost, this will not be a tutorial on how to administer Docker, WebDAV, or especially Traefik, but I’ll give you the exact steps and code for setting this up yourself, and provide some links at the end you can use to learn more about these topics.

All of the following steps will be executed on your VPS, so please sure you are connected to it via SSH or a similar terminal window.

We’ll be using an external docker bridge network in this configuration, the following command will create it

```text
docker network create proxy
```

### Create Traefik Configuration

First of all, let’s create the directory structure we’ll need for Traefik (line 1). We’ll also be creating a file that will be used for storing SSL certificates (line 2), and setting permissions on it (line 3).

```text
mkdir -p $HOME/docker/traefik/data
touch $HOME/docker/traefik/data/acme.json
chmod 600 $HOME/docker/traefik/data/acme.json
```

#### Create Traefik Configuration

Create a new file in the **`traefik/data`** directory we just created called `traefik.yml` with the contents below.

Changes Required:

- Line 24: Modify your email address

```text
#File Path
#$HOME/docker/traefik/data/traefik.yml

#/2020/04/27/ditch-lastpass-for-enpass-webdav-https-traefik/
#https://github.com/jonhowe/Virtjunkie.com/tree/master/DitchLastPass

api:
  dashboard: false

entryPoints:
  http:
    address: ":80"
  https:
    address: ":443"

providers:
  docker:
    endpoint: "unix:///var/run/docker.sock"
    exposedByDefault: false

certificatesResolvers:
  http:
    acme:
      email: your.email@domain.com
      storage: acme.json
      httpChallenge:
        entryPoint: http
```

#### Define Traefik Container

Create a new file in the **`traefik/data`** directory called `docker-compose.yml`

Changes Required:

- Line 30: Modify to fit the hostname of your server
- Line 31: Add in credentials compatible with basic auth. You can use the output from the command below to achieve this.
  - `echo $(htpasswd -nb [your user] [your pass]) | sed -e s/\$/\$\$/g`
- Line 35: Modify to fit the hostname of your server

```text
#File Path
#$HOME/docker/traefik/docker-compose.yml

#/2020/04/27/ditch-lastpass-for-enpass-webdav-https-traefik/
#https://github.com/jonhowe/Virtjunkie.com/tree/master/DitchLastPass

version: '3'

services:
  traefik:
    image: traefik:v2.0
    container_name: traefik
    restart: unless-stopped
    security_opt:
      - no-new-privileges:true
    networks:
      - proxy
    ports:
      - 80:80
      - 443:443
    volumes:
      - /etc/localtime:/etc/localtime:ro
      - /var/run/docker.sock:/var/run/docker.sock:ro
      - ./data/traefik.yml:/traefik.yml:ro
      - ./data/acme.json:/acme.json
      - ./data/logs/:/logs/
    labels:
      - "traefik.enable=true"
      - "traefik.http.routers.traefik.entrypoints=http"
      - "traefik.http.routers.traefik.rule=Host(`custom.hostname.com`)"
      - "traefik.http.middlewares.traefik-auth.basicauth.users=traefikuser:htpasswd-encrypted-string"
      - "traefik.http.middlewares.traefik-https-redirect.redirectscheme.scheme=https"
      - "traefik.http.routers.traefik.middlewares=traefik-https-redirect"
      - "traefik.http.routers.traefik-secure.entrypoints=https"
      - "traefik.http.routers.traefik-secure.rule=Host(`custom.hostname.com`)"
      - "traefik.http.routers.traefik-secure.middlewares=traefik-auth"
      - "traefik.http.routers.traefik-secure.tls=true"
      - "traefik.http.routers.traefik-secure.tls.certresolver=http"
      - "traefik.http.routers.traefik-secure.service=api@internal"

networks:
  proxy:
```

#### Start Traefik Container

```text
cd $HOME/docker/traefik
docker-compose up -d
```

### Create WebDAV Configuration

Before we begin, we need to create the directory structure for the WebDAV container. Use the following command to do so.

```text
mkdir -p $HOME/docker/webdav/dav/
```

We’ll be using a [container authored by bytemark](https://hub.docker.com/r/bytemark/webdav/) for this project. It’s essentially just apache with the webdav module installed. As of today, the container is less than 100MB.

#### Define WebDAV Application Configuration

Changes Required:

- Line 15: Username used to authenticate to the WebDAV service.
- Line 16: Password you’ll use to authenticate to the WebDAV service. This is stored in plaintext in this example, but storing the variable in an external file is best practice.
- Line 17: Modify to fit the hostname of your server
- Line 27: Modify to fit the hostname of your server
- Line 31: Modify to fit the hostname of your server

```text
#File path
#$HOME/docker/webdav/docker-compose.yml

#/2020/04/27/ditch-lastpass-for-enpass-webdav-https-traefik/
#https://github.com/jonhowe/Virtjunkie.com/tree/master/DitchLastPass

version: '3'
services:
  webdav:
    image: bytemark/webdav
    container_name: webdav
    restart: unless-stopped
    environment:
      AUTH_TYPE: Basic
      USERNAME: your-username
      PASSWORD: secure-passsword
      SERVER_NAMES: your-dav.domain.com
    networks:
      - proxy
    security_opt:
      - no-new-privileges:true
    volumes:
      - ./dav:/var/lib/dav
    labels:
      - "traefik.enable=true"
      - "traefik.http.routers.webdav.entrypoints=http"
      - "traefik.http.routers.webdav.rule=Host(`your-dav.domain.com`)"
      - "traefik.http.middlewares.webdav-https-redirect.redirectscheme.scheme=https"
      - "traefik.http.routers.webdav.middlewares=webdav-https-redirect"
      - "traefik.http.routers.webdav-secure.entrypoints=https"
      - "traefik.http.routers.webdav-secure.rule=Host(`your-dav.domain.com`)"
      - "traefik.http.routers.webdav-secure.tls=true"
      - "traefik.http.routers.webdav-secure.tls.certresolver=http"
      - "traefik.http.routers.webdav-secure.service=webdav"
      - "traefik.http.services.webdav.loadbalancer.server.port=80"
      - "traefik.docker.network=proxy"
networks:
  proxy:
    external: true
```

#### Start the WebDAV Container

Run the following command to bring up the webdav container

```text
cd $HOME/docker/webdav
docker-compose up -d
```

### Bringing it all together

#### Summary

At this point you should have two containers running on your VPS. Traefik is acting as a reverse proxy for the WebDAV container, and is providing SSL encryption to it. The SSL certificate is provided by [Let’s Encrypt](https://letsencrypt.org/).

#### Final Directory Structure

```text
user@webdav-server:~/docker$ tree
.
├── traefik
│&nbsp;&nbsp; ├── data
│&nbsp;&nbsp; │&nbsp;&nbsp; ├── acme.json
│&nbsp;&nbsp; │&nbsp;&nbsp; └── traefik.yml
│&nbsp;&nbsp; └── docker-compose.yml
└── webdav
    ├── dav
    │&nbsp;&nbsp; ├── data
    │&nbsp;&nbsp; │&nbsp;&nbsp; └── Enpass
    │&nbsp;&nbsp; │&nbsp;&nbsp;     └── vault.enpassdbsync
    │&nbsp;&nbsp; ├── DavLock
    │&nbsp;&nbsp; ├── DavLock.dir
    │&nbsp;&nbsp; └── DavLock.pag
    └── docker-compose.yml

6 directories, 8 files
```

## Migrate to Enpass Using WebDAV

Now that we’ve got a functional and secure WebDAV instance, we just need to migrate to it. These steps are pretty easy, but I want to include them to be comprehensive.

### Export Secrets From Lastpass

To make our transition from Lastpass as seamless as possible, we’ll export our secrets so we can import them into Enpass. The easiest way to do this is from the Lastpass Vault.

![](/wp-content/uploads/2020/04/2020-04-26_11-51.png)

Step 1 – Open Your Vault

---

![](/wp-content/uploads/2020/04/2020-04-26_11-55.png)

Step 2 – Export Secrets

1. Select “More Options”
2. Select “Advanced”
3. Select “Export”
4. If prompted, enter your Master Password, and note where the CSV export file name and path.

### Import Secrets To Enpass

Pretty easy stuff here, just open enpass, and kick off the import.

![](/wp-content/uploads/2020/04/Peek-2020-04-26-12-55.gif)

Import Steps:

1. Open Enpass
2. Select Menu
3. Select File
4. Select Import
5. When prompted to “Select from where you want to import your data into Enpass”, select Lastpass
6. Navigate to the directory you exported the CSV to
7. Select continue to finish the import

### Connect EnPass To WebDav Share

At this point you’ve got a functioning WebDAV service protected by SSL, as well as a local instance of Enpass that has your lastpass secrets. We just need to connect EnPass to your Webdav instance to allow us to sync to it. Once you have [EnPass Installed](https://www.enpass.io/downloads/), follow the steps below to connect it to your WebDAV Service.

![](/wp-content/uploads/2020/04/Peek-2020-04-26-12-20.gif)

Connection Steps:

1. Open Enpass
2. Select Settings
3. Select Vaults
4. Select the Vault you’d like to sync
5. Enter the URL of your server, and ensure to include the https:// prefix
6. Enter the username and password created in Section 2.2.1
7. Ensure that the checkbox for “Bypass SSL Certificate Validation” is unchecked. We want to validate the SSL certificate since we are using Let’s Encrypt.

## Risks

There are some things that LastPass does for us that we don’t get with this solution. In particular, we are somewhat exposed to brute force attempts to the webdav service. Also, LastPass has a number of email notifications that go out when things happen in your vault. We are really only notified when a new client joins the vault in Enpass.

## Trafeik Resources

<https://medium.com/@containeroo/traefik-2-0-docker-a-simple-step-by-step-guide-e0be0c17cfa5>  
<https://containo.us/blog/traefik-2-0-docker-101-fc2893944b9d/>
