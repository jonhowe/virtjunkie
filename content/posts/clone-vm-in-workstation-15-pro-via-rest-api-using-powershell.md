---
title: "Clone VM in Workstation 15 Pro via REST API using Powershell"
date: 2018-11-26T09:51:36-05:00
slug: "clone-vm-in-workstation-15-pro-via-rest-api-using-powershell"
url: /2018/11/26/clone-vm-in-workstation-15-pro-via-rest-api-using-powershell/
author:
  - "jhowe"
year: ["2018"]
month: ["2018-11"]
categories:
  - "automation"
  - "powershell"
  - "scripting"
  - "vmware"
tags: []
aliases:
  - "/clone-vm-in-workstation-15-pro-via-rest-api-using-powershell/"
  - "/2018/11/26/clone-vm-in-workstation-15-pro-via-rest-api-using-powershell/feed/"
---

After [posting yesterday about modifying the parent image to allow for hostname changes](/prompt-for-a-new-hostname-on-boot/), I was still looking for something a little more streamlined. I remember r[eading about the new REST API](https://blogs.vmware.com/workstation/2018/09/workstation-15-is-here.html) that is available on workstation, so I wrote a little script to use the Workstation API to clone a VM.

<!--more-->

Also just FYI – this performs a full clone, not a linked clone. I’m not sure that linked clone functionality is available via the API yet. I’m hoping to use the vmrun command to accomplish this, and while I know it is packaged with Workstation Pro, [the only documentation I can find](https://docs.vmware.com/en/VMware-Fusion/11/com.vmware.fusion.using.doc/GUID-FF306A59-080E-497E-857D-F45125927FB3.html) for it is associated with Fusion. I also have been thinking about using [vagrant](https://www.vagrantup.com/vmware/index.html) for this as well.

This is very basic functionality, and exists simply to showcase the functionality. There’s no error checking, and it could be expanded a lot. Regardless, enjoy!

```powershell
<#
Original Links: 
https://github.com/jonhowe/Virtjunkie.com/blob/master/clone-workstation-vm.ps1
http://www.virtjunkie.com/clone-vm-in-workstation-15-pro-via-rest-api-using-powershell/
The API will need to be running. Use this link to configure it.
https://docs.vmware.com/en/VMware-Workstation-Pro/15.0/com.vmware.ws.using.doc/GUID-C3361DF5-A4C1-432E-850C-8F60D83E5E2B.html
#>
$user = '[Username]'
$pass = '[Password]'
$VMToClone = "[Template Name To Clone]"
$newvmname = "[New VM Name]"
$REST_URL = "https://[Your IP and port]/api/vms"

function Select-VM {
    param (
        $vmname
    )

    $rs=Invoke-WorkstationRestRequest -method Get

    foreach ($vm in $rs)
    {
        $pathsplit = ($vm.path).split("/")
        $vmxfile = $pathsplit[($pathsplit.Length)-1]
        $thisVM = ($vmxfile).split(".")[0]
        if ($thisVM -eq $vmname) { return $vm;break}
    } 
}

function Select-OneVM {
    param (
        $vmid
    )
    $rs=Invoke-WorkstationRestRequest -method Get -uri ($REST_URL + "/$($vmid.id)")
    return $rs
}
function Set-Credentials {
    param (
        $username,
        $password
    )

    $pair = "${username}:${password}"
    $bytes = [System.Text.Encoding]::ASCII.GetBytes($pair)
    $base64 = [System.Convert]::ToBase64String($bytes)

    $basicAuthValue = "Basic $base64"
    return $basicAuthValue
}

function New-WorkstationVM {
    param (
        $sourcevmid,
        $newvmname
    )
    $body = @{
        'name' = $newvmname;
        'parentId' = $sourcevmid
    }
    $requestbody = ($body | ConvertTo-Json)
    $rs=Invoke-WorkstationRestRequest -method "POST" -body $requestbody
    return $rs
}

function Invoke-WorkstationRestRequest {
    param (
        $uri=$REST_URL,
        $method,
        $body=$null
    )

    $headers = @{
        'authorization' =  $basicAuthValue;
        'content-type' =  'application/vnd.vmware.vmw.rest-v1+json';
        'accept' = 'application/vnd.vmware.vmw.rest-v1+json';
        'cache-control' = 'no-cache'
    }
    $rs=Invoke-RestMethod -uri $uri -Headers $headers -SkipCertificateCheck -Method $method -Body $body
    return $rs
}

$creds = Set-Credentials -username $user -password $pass
$vmtoclone = Select-VM -vmname $VMToClone 
$result=New-WorkstationVM -sourcevmid $VMToClone.id -newvmname $newvmname
$newvm = select-onevm -vmid $result

return $newvm
```
