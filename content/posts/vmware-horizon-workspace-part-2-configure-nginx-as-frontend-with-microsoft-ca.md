---
title: "VMware Horizon Workspace – Part 2 – Configure Nginx as Frontend with Microsoft CA"
date: 2013-08-01T22:45:23-04:00
slug: "vmware-horizon-workspace-part-2-configure-nginx-as-frontend-with-microsoft-ca"
url: /2013/08/01/vmware-horizon-workspace-part-2-configure-nginx-as-frontend-with-microsoft-ca/
author:
  - "jhowe"
year: ["2013"]
month: ["2013-08"]
categories:
  - "horizon-workspace"
  - "servers"
  - "vmware"
tags: []
aliases:
  - "/2013/08/01/vmware-horizon-workspace-part-2-configure-nginx-as-frontend-with-microsoft-ca/feed/"
---

So yesterday, [VMware released Horizon Workspace 1.5](https://www.vmware.com/support/horizon_workspace/doc/hw_release_notes_15.html "VMware® Horizon Workspace 1.5 Release Notes"). HUGE improvement over the GA release… Holey smokes. Any further tutorials will reference this version.

Anyways, more to the point. In this post I will demonstrate how to do a base configuration of Horizon Workspace using an internal Microsoft Certificate Authority with Nginx as a frontend. This setup is only acceptable for setting up workspace in a lab environment, since in a production environment you’ll need a trusted third party cert. Doing this in a lab environment is important because it will allow you to set up and test every feature you’ll be using in a production environment.

Requirements:

- Microsoft Active Directory Certificate Services
- Linux Machine running Nginx
- Horizon Workspace 1.5 Downloaded and installed with no configuration.
  - We’ll be using the workspace FQDN of hzn.test.in (This obviously assumes the domain of test.in)

<!--more-->

1. On Linux machine, generate private key(1) and CSR(2)
   1. 

```bash
openssl genrsa -out hzn.test.in.key 1024
```

   2. 

```bash
openssl req -new -key hzn.test.in.key -out hzn.test.in.csr
```

2. Take CSR and get a certificate from your internal Domain CA. Download the certificate. Rename it as hzn.test.in.crt
3. Download your internal Domain CA root key
   1. On the machine running AD Cert Services, open the command line and type the following command:
   2. [text]certutil -ca.cert %userprofile%\Desktop\test.in-root.cer[/text]
4. Ensure that Nginx is forwarding traffic correctly to the gateway-va. Below is a snippet (Entries in square brackets need to be changed]:
   1. [text]  
      server {  
      listen [load balancer IP];  
      server\_name hzn.test.in;  
      ssl on;  
      ssl\_certificate [path to]hzn.test.in.crt  
      ssl\_certificate\_key [path to]hzn.test.in.key

      location / {  
      proxy\_pass https://gateway-va.test.in:443/;  
      proxy\_set\_header Host $host;  
      proxy\_set\_header X-Real-IP $remote\_addr;  
      proxy\_set\_header X-Forwarded-For $proxy\_add\_x\_forwarded\_for;  
      proxy\_read\_timeout 1800;  
      proxy\_connect\_timeout 1800;  
      }  
      [/text]
5. Place your domain root ca key (gathered in step 3) into the [configurator web interface](https://configurator-va.test.in/)
   1. Open the web interface and navigate to the FQDN & SSL section
   2. Select Yes under External Load Balancer
   3. Enter: hzn.test.in:443 in the Horizon Workspace FQDN section
   4. Paste the domain root ca key in the “Load Balancer Root CA Certificate” section.
6. You’re all set!  You can now log into the Horizon Workspace Admin page by navigating to https://hzn.test.in/admin

I’d be happy to answer any questions on this. Feel free to post a comment if you like. I’ll answer any questions I can.
