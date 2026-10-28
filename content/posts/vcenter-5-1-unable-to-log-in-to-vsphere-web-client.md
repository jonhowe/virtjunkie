---
title: "vCenter 5.1 – Unable to Log in to vSphere Web Client"
date: 2013-04-10T19:00:30-04:00
slug: "vcenter-5-1-unable-to-log-in-to-vsphere-web-client"
url: /2013/04/10/vcenter-5-1-unable-to-log-in-to-vsphere-web-client/
author:
  - "jhowe"
year: ["2013"]
month: ["2013-04"]
categories:
  - "servers"
  - "vmware"
tags: []
aliases:
  - "/2013/04/10/vcenter-5-1-unable-to-log-in-to-vsphere-web-client/feed/"
---

In a new installation of vCenter 5.1, when trying to access the vSphere Web Client for the first time, you will encounter the following message:

[text]  
In order for this direct link to work, you must first log in to the  
vSphere Web Client at least once from https://{webclient  
-host}:{webclient-https-port}.  
[/text]

You can resolve this error and fix the issue using the following steps:  

<!--more-->

Let’s say the name of your vCenter server is vCenter. As long as your SSO configuration was done correctly, and you kept the default ports during installation you can log in using the following URL:

<https://vcenter-test:9443/vsphere-client>

Once you log in using that URL, log out, and then try accessing the URL that originally provided the error (which is: https://vcenter-test/vsphere-client/), and it works!

![vcenter1](/wp-content/uploads/2013/04/vcenter1.png)
