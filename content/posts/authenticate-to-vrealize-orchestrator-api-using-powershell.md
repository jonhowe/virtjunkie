---
title: "Authenticate to vRealize Orchestrator API using PowerShell"
date: 2022-08-15T13:27:40-04:00
lastmod: 2022-08-15T13:27:41-04:00
slug: "authenticate-to-vrealize-orchestrator-api-using-powershell"
url: /2022/08/15/authenticate-to-vrealize-orchestrator-api-using-powershell/
author:
  - "jhowe"
year: ["2022"]
month: ["2022-08"]
categories:
  - "automation"
  - "powershell"
  - "scripting"
  - "vmware"
tags: []
aliases:
  - "/2022/08/15/authenticate-to-vrealize-orchestrator-api-using-powershell/feed/"
---

![](/wp-content/uploads/2022/08/image-1388x1536.png)

I’m working on a project that requires direct interaction with the vRO API from a third party system. Maybe I’m getting less effective at using Google in my old age, but I had a heck of a time finding good solid code for authenticating to the API using anything, including PowerShell.

Typically I’d use [Invoke-vRARestMethod](https://jakkulabs.github.io/PowervRA/functions/Invoke-vRARestMethod/) from [PowerVRA](https://github.com/jakkulabs/PowervRA) for this, but unfortunately I had some additional requirements that mandate me using a bearer token.

As a point of reference, you can view all of of the available APIs for vRealize Automation by navigating to this url: https://{your-vra-url}/automation-ui/api-docs/. We’ll be working with the “Orchestrator” API

The function below will return a bearer token, which you can use in future API calls to vRA.

<script src="https://gist.github.com/jonhowe/36304d54b77e794427534b8b38f0bd0d.js"></script>

Param’s:  
Line 3: vra\_server – the fqdn of your vRA 8 instance  
Line 4: password – password associated with your vRA 8 account used to authenticate. As mentioned, please be smart here. Plantext passwords are bad.  
Line 5: username – Unlike vRA 7, vRA 8 needs you to split your username and domain apart. For example, in vRA 7 you’d authenticate using the username jon.smith@rainpole.com, where in vRA 8 you authenticate using just the username jon.smith  
Line 6: domain – This is where the domain goes (Example: rainpole.com)  
  
Lines 14-24: We’re setting the body up to be included in the rest request. There’s some special formatting required so we’re using the replace method to modify the string.  
  
Line 27: Build a simple variable with the URI used for authentication. More can be found on this in the API documentation mentioned above.  
  
Lines 29-35: Make the API call, build the bearer token (essentially add the word “Bearer ” to the beginning of the authentication token), and return it.

Short and sweet. I’ll be adding some more snippets and problems in the future.
