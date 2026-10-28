---
title: "VCSA 6.7: Error trying to join AD, error code [40024]"
date: 2019-08-03T09:38:00-04:00
slug: "vcsa-6-7-error-trying-to-join-ad-error-code-40024"
url: /2019/08/03/vcsa-6-7-error-trying-to-join-ad-error-code-40024/
author:
  - "jhowe"
year: ["2019"]
month: ["2019-08"]
categories:
  - "uncategorized"
  - "vmware"
tags: []
aliases:
  - "/2019/08/03/vcsa-6-7-error-trying-to-join-ad-error-code-40024/feed/"
---

Tried joining a VCSA to AD today and received the error message:

```text
Error: Idm client exception: Error trying to join AD, error code &#91;40024], user &#91;administrator], domain &#91;home.lab], orgUnit &#91;]
```

![](/wp-content/uploads/2019/08/image.png)

<!--more-->

Couldn’t find anything on google, so connected to the VCSA via SSH, tried a simple ping test to see if DNS was the issue.. no dice. Then tried adding the VCSA to AD manually.  
**Heavy Palmface**  
Looks like the administrator password is expired.

![](/wp-content/uploads/2019/08/image-2.png)

So.. I logged into the DC, and as we expected,

![](/wp-content/uploads/2019/08/image-1.png)

So, as it turns out, if AD is healthy, this isn’t an issue. Who would have known…

![](/wp-content/uploads/2019/08/image-3.png)
