---
title: "Powershell – Provision NetApp Volume as NFS Datastore to vCenter"
date: 2014-04-29T13:48:11-04:00
slug: "powershell-provision-netapp-volume-as-nfs-datastore-to-vcenter"
url: /2014/04/29/powershell-provision-netapp-volume-as-nfs-datastore-to-vcenter/
author:
  - "jhowe"
year: ["2014"]
month: ["2014-04"]
categories:
  - "automation"
  - "netapp"
  - "powershell"
  - "scripting"
  - "vmware"
tags: []
aliases:
  - "/2014/04/29/powershell-provision-netapp-volume-as-nfs-datastore-to-vcenter/feed/"
---

![powercli-icon](/wp-content/uploads/2014/04/powercli-icon.jpg)For anyone that’s ever been through the process of provisioning a new datastore to multiple ESX hosts, you know it can take some time. Below are the steps I use

1. Create Volume on NetApp
2. Set Security Style to Unix
3. Enable Storage Efficiency
4. Set NFS Export permissions to allow Read/Write + Root Permissions to all applicable hosts
5. Mount datastores on ESXi hosts

For a handful of hosts this is fine, but adding it to anything more than 4-5 hosts is reaaally painful in my experience. Below is a script you can use to take care of these steps in one swipe.

<!--more-->

Prerequisites:

[NetApp DataOnTap Toolkit](/2013/02/10/install-netapp-dataontap-powershell/ "Install NetApp DataOnTap Powershell")

[VMware PowerCLI](https://my.vmware.com/web/vmware/details?downloadGroup=VSP510-PCLI-510&productId=285)

The script requires an array of the NFS clients (read ESXi hosts) you want to connect the datastore to.

**Example 1 – assign the array to a variable, and manually add it to a parameter**

```powershell
$ESXHosts = @("10.1.1.100","10.1.1.101","10.1.1.102")
Add-VolumeAndAddToESXi.ps1 -VolName Volume100 -VolSize 1.5T -filerIP 10.1.1.10 -aggrName aggr0 -ExportedHosts $ESXHosts -vCenter vcenter-site1
```

**Example 2 – Create an array, and pipe it to the script**

```powershell
@("10.1.1.100","10.1.1.101") | Add-VolumeAndAddToESXi.ps1 -VolName Volume101 -VolSize 200G -filerIP 10.1.1.10 -aggrName aggr1 -vCenter vcenter-site1
```

Enjoy! Let me know if you have any challenges or questions

[Add-VolumeAndAddToESXi.ps1](https://new.virtjunkie.com/wp-content/uploads/2014/04/Add-VolumeAndAddToESXi.ps1_.zip)

```powershell
<#	
	.NOTES
	===========================================================================
	 Created with: 	SAPIEN Technologies, Inc., PowerShell Studio 2014 v4.1.49
	 Created on:   	4/17/2014 10:39 PM
	 Created by:   	Jon Howe (www.cit3.net)
	 Filename:     	Add-VolumeAndAddToESXi.ps1
	===========================================================================
	.DESCRIPTION
		Create Volume and add to all hosts in a vCenter server
	.PARAMETER VolName
		The  Name of the Volume you want to create
	.PARAMETER VolSize
		The size of the newly created volume. Example: 10G, 1T, 100M
	.PARAMETER filerIP
		The IP Address of the filer
	.PARAMETER aggrName
		The aggregate that will contain the volume
	.PARAMETER ExportedHosts
		An array that contains IP Addresses of the ESXi hosts you want to provide NFS Export permissiosn to
	.PARAMETER vCenter
		The DNS or IP Address of the vCenter Server you want to provision the datastore to
	.LINK
		/2014/04/29/powershell-provision-netapp-volume-as-nfs-datastore-to-vcenter/
	.EXAMPLE
		$ESXHosts = @("10.1.1.100","10.1.1.101","10.1.1.102")
		Add-VolumeAndAddToESXi.ps1 -VolName Volume100 -VolSize 1.5T -filerIP 10.1.1.10 -aggrName aggr0 -ExportedHosts $ESXHosts -vCenter vcenter-site1
	.EXAMPLE
		@("10.1.1.100","10.1.1.101") | Add-VolumeAndAddToESXi.ps1 -VolName Volume101 -VolSize 200G -filerIP 10.1.1.10 -aggrName aggr1 -vCenter vcenter-site1
#>

Param (
	[Parameter(Mandatory=$true)] [string]$VolName,
	[Parameter(Mandatory=$true)] [string]$VolSize,
	[Parameter(Mandatory=$true)] [string]$filerIP,
	[Parameter(Mandatory = $true)] [string]$aggrName,
	[Parameter(Mandatory=$true)] [string]$vCenter,
	[Parameter(Mandatory=$true, ValueFromPipeline=$true)] $ExportedHosts
)

#region Don't edit below here
###
##
#

$path = "/vol/" + $VolName

#Load Prerequisites
Add-PSSnapin VMware.VimAutomation.Core -ErrorAction 'SilentlyContinue'
if (!(Get-Module DataOnTAP)) { Import-Module DataOnTAP }

# Connect to the filer
Write-Host "Enter credentials for the netapp filer"
$controller = Connect-NaController $filerIP -Credential (Get-Credential)

#Create the volume and set security style
New-NaVol -Aggregate $aggrName -Name $VolName -Size $VolSize -Controller $controller
Set-NaQtree -SecurityStyle UNIX -Path $path -Controller $controller

#Enable Storage Efficiency
enable-NaSis -Controller $controller -Volume (Get-NaVol -Name $VolName)

#Set NFS Export Permissions
Set-NaNfsExport -Path $path -ReadWrite $hosts -Root $hosts -Persistent

#Connect to vCenter Server
Write-Host "Enter credentials for the vCenter server"
Connect-VIServer -Credential (Get-Credential) -Server $vCenter

Get-Cluster -Name Production | Get-VMHost | New-Datastore -Nfs -Name $VolName -Path $path -NfsHost $NfsIP

#
##
###
#endregion Don't edit below here
```

– Jon
