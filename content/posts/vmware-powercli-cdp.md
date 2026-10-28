---
title: "Use VMware PowerCLI to Pull CDP information from ESXi Hosts"
date: 2014-07-25T16:48:21-04:00
slug: "vmware-powercli-cdp"
url: /2014/07/25/vmware-powercli-cdp/
author:
  - "jhowe"
year: ["2014"]
month: ["2014-07"]
categories:
  - "automation"
  - "powershell"
  - "scripting"
  - "vmware"
tags: []
aliases:
  - "/2014/07/25/vmware-powercli-cdp/feed/"
---

I like having documentation, but I hate creating documentation.  I’ll be the first to admit that I’m *slightly* lazy at times, however, my own personal preferences for what I’ll call “Effort Allocation”, are not the root of my dislike for creating documentation.  The issue really stems from the fact that creating it is very time consuming, tedious, and usually lower on the priority list.

However, sometimes it’s not you that failed to create the documentation. Consultants frequently fall into this category.

The issue I’m handling here is documenting CDP information from the perspective of ESXi hosts using PowerCLI.

<!--more-->

Rather than navigating to each host and grabbing the CDP info from each host in a cluster like the screenshot below, you can run the commandlet I’m publishing in this article.

![](http://kb.vmware.com/Platform/Publishing/images/1007069_cdp_gui_vc_3.jpg)

[Download the PS1 file](https://new.virtjunkie.com/wp-content/uploads/2014/07/Get-CDP.zip), and check out examples in the comment based help below.

References: [VMware KB 1007069](http://kb.vmware.com/kb/1007069)

```powershell
<#
	.NOTES
	===========================================================================
	 Created with: 	SAPIEN Technologies, Inc., PowerShell Studio 2014 v4.1.61
	 Created on:   	7/25/2014 1:00 PM
	 Created by:   	Jon Howe
	 Filename:     	Get-CDP.ps1
	===========================================================================
	.SYNOPSIS
		Connects to VirtualCenter and lists pertinent CDP information
	.DESCRIPTION
		Connects to VirtualCenter and lists pertinent CDP information
	.PARAMETER $VirtualCenterServer
		Required String Parameter. The fully qualified domain name of the virtualcenter server
	.PARAMETER $cluster
		Optional StringParameter. The name of the cluster you want to filter by.
	.PARAMETER $asLocalUser
		Optional Boolean Parameter. Do you want to connect to vC as you, or do you want to manually
		authenticate as a different user.
	.EXAMPLE
		Get-CDP -VirtualCenterServer vc-tst-1.test.in
		Actions Taken:
		This will connect to the specified virtualcenter server and list the CDP Information
		Results:
		ESXi_HostName  : ESXi-1.test.in
		VMnic          : vmnic1
		SwitchIdentity : test-3750.test.in
		ManagementIP   : 10.1.1.1
		SwitchPort     : GigabitEthernet1/0/1
		SwitchPlatform : cisco WS-C3750G-48TS
		Interfce_Vlan  : 999

		ESXi_HostName  : ESXi-1.test.in
		VMnic          : vmnic2
		SwitchIdentity : test-3750.test.in
		ManagementIP   : 10.1.1.1
		SwitchPort     : GigabitEthernet1/0/2
		SwitchPlatform : cisco WS-C3750G-48TS
		Interfce_Vlan  : 999
	.EXAMPLE
		Get-CDP -VirtualCenterServer vc-tst-1.test.in -cluster testCluster -asLocalUser $false
		Actions Taken:
		This will connect you to the specified VirtualCenter server and only search hosts specified in
		the cluster. It will prompt you to enter your username and password.
		Results:
		Same as example 1
	.EXAMPLE
		Get-CDP -VirtualCenterServer vc-tst-1.test.in | export-csv -path c:\temp\cdp_information.csv -notypeinformation
		Actions Taken:
		This script outputs an object, so you can do anything you want with the output, such as create a CSV, sort, etc.
		Results:
		Sames as example 1
	.LINK
		/2014/07/25/vmware-powercli-cdp/
	.LINK
		http://kb.vmware.com/kb/1007069
#>
[CmdletBinding()]
param (
	[Parameter(Position = 0, Mandatory = $true)]
	[System.String]
	$VirtualCenterServer,
	[Parameter(Position = 1)]
	[System.String]
	$ClusterName,
	[Parameter(Position = 2)]
	[System.Boolean]
	$asLocalUser=$true
)

#region Add Snapin and Connect to vC
#Check to see if the VMware.VimAutomation.Core snapin is loaded - load it if it's not
if ((Get-PSSnapin -Name VMware.VimAutomation.Core -ErrorAction SilentlyContinue) -eq $null)
{
	Add-PsSnapin VMware.VimAutomation.Core
}

#Check to see if we're already connected to the correct VC Server
if ($DefaultVIServers.name -ne $VirtualCenterServer)
{
	#Determine if we're logging in to VirtualCenter as a local user or if we should prompt for credentials
	if ($asLocalUser)
	{
		Connect-VIServer -Server $VirtualCenterServer | Out-Null
		Write-Debug &quot;Logging in as local user to vc: $VirtualCenterServer&quot;
	}
	else
	{
		Connect-VIServer -Server $VirtualCenterServer -Credential (Get-Credential) | Out-Null
		Write-Debug &quot;Logging in as manually selected user to vc: $VirtualCenterServer&quot;
	}
}
else
{
	Write-Debug &quot;Looks like we're already connected to: $VirtualCenterServer in this session&quot;
}
#endregion Add Snapin and Connect to vC

$cdpDetails = @()

#Get List of Hosts
if ($ClusterName)
{
	$hosts = Get-Cluster -Name $ClusterName | Get-VMHost | Where-Object { $_.ConnectionState -eq &quot;Connected&quot; }
}
else
{
	$hosts = Get-VMHost | Where-Object { $_.ConnectionState -eq &quot;Connected&quot; }
}

#Get the Network Config information from each host
$hosts | % { Get-View $_.ID } | % { $esxname = $_.Name; Get-View $_.ConfigManager.NetworkSystem } |
% {
	foreach ($physnic in $_.NetworkInfo.Pnic)
	{
		#Get detailed CDP information for all interfaces
		$result = ($_.QueryNetworkHint($physnic.Device)).ConnectedSwitchPort
		if ($result)
		{
			$objOneHost = New-Object System.Object
			$objOneHost | Add-Member -type NoteProperty -name ESXi_HostName -Value $esxname
			$objOneHost | Add-Member -type NoteProperty -name VMnic -Value $physnic.Device
			$objOneHost | Add-Member -type NoteProperty -name SwitchIdentity -Value $result.DevId
			$objOneHost | Add-Member -type NoteProperty -name ManagementIP -Value $result.Address
			$objOneHost | Add-Member -type NoteProperty -name SwitchPort -Value $result.PortID
			$objOneHost | Add-Member -type NoteProperty -name SwitchPlatform -Value $result.HardwarePlatform
			$objOneHost | Add-Member -type NoteProperty -name Interfce_Vlan -Value $result.Vlan
			$cdpDetails += $objOneHost
		}
	}
}

$cdpDetails

Disconnect-VIServer -Server $VirtualCenterServer | Out-Null
```
