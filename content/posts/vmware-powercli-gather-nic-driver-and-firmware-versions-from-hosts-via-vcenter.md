---
title: "VMware Powercli – Gather NIC Driver and Firmware Versions from Hosts via vCenter"
date: 2014-10-20T15:46:58-04:00
slug: "vmware-powercli-gather-nic-driver-and-firmware-versions-from-hosts-via-vcenter"
url: /2014/10/20/vmware-powercli-gather-nic-driver-and-firmware-versions-from-hosts-via-vcenter/
author:
  - "jhowe"
year: ["2014"]
month: ["2014-10"]
categories:
  - "automation"
  - "powershell"
  - "scripting"
  - "vmware"
tags: []
aliases:
  - "/2014/10/20/vmware-powercli-gather-nic-driver-and-firmware-versions-from-hosts-via-vcenter/feed/"
---

I recently encountered an issue in vSphere 5.5 where I wasn’t able to change the interface speed on an ESXi host from auto-negotiate to anything else. After a good amount of troubleshooting I was able to determine that this issue was occurring due to the fact that the NIC firmware version and driver version on a blade server was out of date. VMware has a [good KB article](http://kb.vmware.com/kb/1027206) on how to grab the firmware and driver versions that I followed. However, the problem is that even on the most modest ESXi host that isn’t running 10G to it, you’ll likely have a minimum of 4 NICs on it. This means that you’ll have to enable SSH on every host you want to check, run one command per NIC each of them (or run a one line script that loops through them, but will that really save you time..?). It doesn’t take a very large cluster for that to become a very large endeavor.

This PowerShell script will connect to a vCenter server, allow you to scan all ESXi hosts, or only hosts within a particular cluster, and output the results in object format so that you can manipulate them how you wish.

<!--more-->

As a refresher, the esxcli command you’ll run to list the required information is below. Substitute [#IFINDEX] with the interface index you want to look at (ie, vmnic1)

**esxcli network nic get -n vmnic[#IFINDEX]**

Which will output something like this:

Advertised Auto Negotiation: true  
Advertised Link Modes: 1000baseT/Full, 2500baseT/Full, 10000baseT/Full  
Auto Negotiation: true  
Cable Type: FIBRE  
Current Message Level: 0  
**Driver Info:**  
**Bus Info: 0000:02:00.0**  
 **Driver: bnx2x**  
 **Firmware Version: bc 6.2.28 phy baa0.105**  
 **Version: 2.710.39.v55.2**  
Link Detected: true  
Link Status: Up  
Name: vmnic0  
PHYAddress: 16  
Pause Autonegotiate: true  
Pause RX: true  
Pause TX: true  
Supported Ports: FIBRE  
Supports Auto Negotiation: true  
Supports Pause: true  
Supports Wakeon: true  
Transceiver: internal  
Wakeon: MagicPacket(tm)

The key info is bold above. The Version: line is referring to the Driver version.

Now, what if you could gather the same information for every host in attached to a vCenter server by simply running a single command specifying your VirtualCenter server and the cluster name. The script below will do exactly that. See comment based help for more info.

```powershell
<#	
	.NOTES
	===========================================================================
	 Created with: 	SAPIEN Technologies, Inc., PowerShell Studio 2014 v4.1.65
	 Created on:   	10/17/2014 10:43 AM
	 Created by:   	Jon Howe
	 Filename:     	Get-NICAndFirmware.ps1
	===========================================================================
	.SYNOPSIS
		Connects to VirtualCenter and lists pertinent NIC driver and version information
	.DESCRIPTION
		Connects to VirtualCenter and lists pertinent NIC driver and version information
	.PARAMETER $VirtualCenterServer
		Required String Parameter. The fully qualified domain name of the virtualcenter server
	.PARAMETER $cluster
		Optional StringParameter. The name of the cluster you want to filter by.
	.PARAMETER $asLocalUser
		Optional Boolean Parameter. Do you want to connect to vC as you, or do you want to manually 
		authenticate as a different user
	.EXAMPLE
		Get-NicDriverAndFirmware -VirtualCenterServer vc-tst-1.test.in
		Actions Taken:
		This will connect to the specified virtualcenter server and list the driver name, version, 
		and firmware version for every NIC in every host attached to your vCenter server. The script will
		authenticate to vCenter as your locally logged in user.
		Results:
		Host_Name                VMNic_Name DriverName DriverVersion FirmwareVersion
		---------                ---------- ---------- ------------- ---------------
		ESXi-1.test.in.parata.local vmnic0     bnx2x      1.72.56.v55.2 bc 5.2.7 phy baa0.105
		ESXi-1.test.in.parata.local vmnic1     bnx2x      1.72.56.v55.2 bc 5.2.7 phy baa0.105
		ESXi-1.test.in.parata.local vmnic2     e1000e     1.1.2-NAPI    5.12-6
		ESXi-1.test.in.parata.local vmnic3     e1000e     1.1.2-NAPI    5.12-6
		ESXi-1.test.in.parata.local vmnic4     e1000e     1.1.2-NAPI    5.12-6
		ESXi-1.test.in.parata.local vmnic5     e1000e     1.1.2-NAPI    5.12-6
	.EXAMPLE
		Get-NicDriverAndFirmware -VirtualCenterServer vc-tst-1.test.in -ClusterName Production -asLocalUser $False | Format-Table -AutoSize
		Actions Taken:
		This will connect to the specified virtualcenter server and list the driver name, version,
		and firmware version for each NIC in every host in the cluster "Production", and will prompt for a username and password.
		Resuts:
		Same as example 1
	.EXAMPLE
		Get-NicDriverAndFirmware -VirtualCenterServer vc-tst-1.test.in -ClusterName Production -asLocalUser $False | c:\temp\vCenterInterfaceDriverandFirmware.csv -notypeinformation
		Actions Taken:
		This script outputs an object, so you can do anything you want with the output, such as create a CSV, sort, etc.
		Results:
		Sames as example 1

	.LINK
		Original Published Location
		http://45.63.13.214/vmware-powercli-gather-nic-driver-and-firmware-versions-from-hosts-via-vcenter
	.LINK
		VMware KB for gathering NIC Driver and Firmware versions
		http://kb.vmware.com/kb/1027206
	.LINK
		VMware Documentation on PowerCLI's Get-EsxCli commandlet
		http://pubs.vmware.com/vsphere-55/topic/com.vmware.powercli.cmdletref.doc/Get-EsxCli.html
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
	$asLocalUser = $true
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
		Write-Debug "Logging in as local user to vc: $VirtualCenterServer"
	}
	else
	{
		Connect-VIServer -Server $VirtualCenterServer -Credential (Get-Credential) | Out-Null
		Write-Debug "Logging in as manually selected user to vc: $VirtualCenterServer"
	}
}
else
{
	Write-Debug "Looks like we're already connected to: $VirtualCenterServer in this session"
}
#endregion Add Snapin and Connect to vC

#region Get List of Hosts
if ($ClusterName)
{
	$VMHosts = Get-Cluster -Name $ClusterName | Get-VMHost | Where-Object { $_.ConnectionState -eq "Connected" }
}
else
{
	$VMhosts = Get-VMHost | Where-Object { $_.ConnectionState -eq "Connected" }
}
#endregion Get List of Hosts

$results = @()
foreach ($VMHost in $VMHosts)
{
	#Get list of network interfaces on host
	$VMHostNetworkAdapters = Get-VMHost $VMHost | Get-VMHostNetworkAdapter | Where-Object { $_.Name -like "vmnic*" }
	
	$esxcli = Get-VMHost $VMHost | Get-EsxCli
	
	$arrNicDetail = @()
	foreach ($VMNic in $VMHostNetworkAdapters)
	{
		$objOneNic = New-Object System.Object
		$objDriverInfo = ($esxcli.network.nic.get($VMNic.Name)).DriverInfo
		
		$objOneNic | Add-Member -type NoteProperty -name Host_Name -Value $VMHost.Name
		$objOneNic | Add-Member -type NoteProperty -name VMNic_Name -Value $VMNic.Name
		$objOneNic | Add-Member -type NoteProperty -name DriverName -Value $objDriverInfo.Driver
		$objOneNic | Add-Member -type NoteProperty -name DriverVersion -Value $objDriverInfo.Version
		$objOneNic | Add-Member -type NoteProperty -name FirmwareVersion -Value $objDriverInfo.FirmwareVersion
		$arrNicDetail += $objOneNic
	}
	
	$results += $arrNicDetail
}

$results
Disconnect-VIServer -Server $VirtualCenterServer -Confirm:$false
Remove-PSSnapin VMware.VimAutomation.Core
```
