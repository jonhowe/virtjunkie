---
title: "PowerCLI – Get All VM Details from get-task"
date: 2019-03-04T22:18:20-05:00
slug: "get-details-from-get-task"
url: /2019/03/04/get-details-from-get-task/
author:
  - "jhowe"
year: ["2019"]
month: ["2019-03"]
categories:
  - "automation"
  - "powershell"
  - "scripting"
  - "vmware"
tags: []
aliases:
  - "/2019/03/04/get-details-from-get-task/feed/"
---

I’ve been working on a project that uses the -runasync parameter on the move-vm cmdlet. The obvious problem with running jobs asynchronously is that you lose the ability to determine the status of whatever task as soon as you submit it.

<!--more-->

I ran into a challenge on this project where I needed to validate some details from the job that was submitted asynchronously. It was more difficult and annoying than I thought it would be, but I managed to get a function together that can get a bunch of information.

The script assumes a pre-existing connection to vCenter and accepts the parameters below.

1. Status\_to\_check – with a default value of “Initiate vMotion Receive operation”
2. vCenter – the FQDN of the vCenter server. I added this in case you are connected to multiple vCenter servers.

```text
function Test-vCenterTasks
{
    param(
        $status_to_check = "Initiate vMotion receive operation",
        $vcenter
    )
    
    $tasks = get-task -Server $vcenter
    $vmotions=$tasks | ? { $_.name -eq $status_to_check}
    $rs = @()
    foreach ($vmotion in $vmotions)
    {
        $vminflight = $vmotion.ExtensionData.Info.EntityName
        $vmobj = get-vm $vminflight -Server $vcenter
        $cluster = $vmobj | Get-Cluster -Server $vcenter

        $obj = New-Object –typename PSObject
        $obj | Add-Member –membertype NoteProperty –name VM_Name –value $vmobj.name
        $obj | Add-Member –membertype NoteProperty –name VM_Cluster –value $cluster.name
        $obj | Add-Member –membertype NoteProperty –name StartTime –value $vmotion.StartTime
        $obj | Add-Member –membertype NoteProperty –name Progress –value $vmotion.PercentComplete
        $obj | Add-Member –membertype NoteProperty –name Description –value $vmotion.Description
        $rs += $obj
    }

    return $rs
}

Test-vCenterTasks -vcenter "vcenter-server-fqdn"
```
