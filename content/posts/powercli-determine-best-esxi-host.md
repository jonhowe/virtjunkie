---
title: "Use PowerCLI to determine the ESXi host with the most available RAM"
date: 2018-12-11T17:30:28-05:00
slug: "powercli-determine-best-esxi-host"
url: /2018/12/11/powercli-determine-best-esxi-host/
author:
  - "jhowe"
year: ["2018"]
month: ["2018-12"]
categories:
  - "automation"
  - "powershell"
  - "scripting"
  - "vmware"
tags: []
aliases:
  - "/2018/12/11/powercli-determine-best-esxi-host/feed/"
---

I’m working on a project right now that requires me to do a shared nothing cross vCenter vMotion of about 6K VMs. As you might know, cross vCenter vMotion requires you to specify the ESXi host and the Datastore your VM will live in within the target vCenter; no targeting a cluster of any kind. This brings up some interesting challenges when trying to automate the migration of such a large amount of VMs. One in particular, is the need to target the ESXi host that has the most free space. I am using the function below to do just this – hopefully it helps!

```text
Function Get-BestDatastore
{
    Param (
        $vmhostlist
    )

    $destination_compute = $vmhostlist | get-vmhost -Server $vc_destination |
        Select-Object name,@{Name = "MemoryFreeGB"; Expression = {($_.MemoryTotalGB - $_.MemoryUsageGB)}} | 
        Sort-Object -Descending -Property MemoryFreeGB |
        Select-Object -First 1

    return $destination_compute
}

$vmhosts = get-cluster -name "destinationcluster" | get-vmhost
```
