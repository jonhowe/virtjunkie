---
title: "Register VMware Workspace as a Cloud Storage Provider in Office 2013"
date: 2013-06-09T14:25:52-04:00
slug: "register-vmware-workspace-as-a-cloud-storage-provider-in-office-2013"
url: /2013/06/09/register-vmware-workspace-as-a-cloud-storage-provider-in-office-2013/
author:
  - "jhowe"
year: ["2013"]
month: ["2013-06"]
categories:
  - "scripting"
  - "automation"
  - "vmware"
tags: []
aliases:
  - "/2013/06/09/register-vmware-workspace-as-a-cloud-storage-provider-in-office-2013/feed/"
---

I was lucky enough to spend the previous week in New Orleans, LA at Microsoft TechEd. I had a great time checking out the latest and greatest that our Redmond buddies are about to throw our way or has already tossed.

I spent the majority of my time focusing on Sharepoint 2013 and Exchange 2013, but I was able to spend some time focusing on the client side of things as well. One thing in particular that stood out to me in this area is how Microsoft is putting a lot of time and development into making their clients “Cloud Friendly”.  Office 2013 is the first version that fully supports cloud storage providers.

Microsoft has graciously ~~strategically~~ provided us with built in compatibility with Skydrive. While this makes things easy to get things up and running, it makes any IT Admin experience a combination of nausea, anger, and anxiety.  If you’re fortunate enough to have a sponsored, approved, supported cloud storage solution, you’ll undoubtedly want to use it.

I’ll show you how to accomplish just that in this post.

<!--more-->

There’s three key things to keep in mind here:

- You will need to be signed into Office using a Microsoft account. IE – Live, Hotmail, etc.
- We will need to provide URLs to a variety of icons that Office will reference.
- All changes will be made in the registry

Once we make sure we’re signed into office using a non-local account (ie, you signed into Microsoft), you will only have to run the batch file attached below, and restart Office.

The batch file I’m providing links to a public image hosting service that I don’t control. Regardless of the reliability of the image hosting service, I recommend that you take the icons I provided in the Horizon Icons.zip file below and host them yourself.

Required Files:

[Horizon Icons.zip](http://45.63.13.214/?attachment_id=467)

[Add Workspace Service.bat.zip](http://45.63.13.214/?attachment_id=468)

References:

[MSDN – Integrating additional cloud storage services in Office 2013](http://msdn.microsoft.com/en-us/library/office/jj984352.aspx)

When all is said and done, you’ll have something that looks like this:

[![Open from VMware Workspace](/wp-content/uploads/2013/06/Open-from-VMware-Workspace-300x229.png)](/wp-content/uploads/2013/06/Open-from-VMware-Workspace.png)
