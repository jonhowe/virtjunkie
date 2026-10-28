---
title: "Monitor NetApp SnapMirror via Solarwinds Server and Application Monitor"
date: 2013-02-13T21:39:35-05:00
slug: "monitor-netapp-snapmirror-via-solarwinds-server-and-application-monitor"
url: /2013/02/13/monitor-netapp-snapmirror-via-solarwinds-server-and-application-monitor/
author:
  - "jhowe"
year: ["2013"]
month: ["2013-02"]
categories:
  - "featured"
  - "netapp"
  - "powershell"
  - "scripting"
  - "automation"
  - "solarwinds"
tags: []
aliases:
  - "/2013/02/13/monitor-netapp-snapmirror-via-solarwinds-server-and-application-monitor/feed/"
---

So [yesterday I talked about](/2013/02/12/monitor-netapp-san-via-solarwinds-server-and-application-monitor/ "Monitor NetApp SAN via Solarwinds Server and Application Monitor") using a Powershell script with in Solarwinds to monitor volume sizes. Using the [NetApp Data ONTAP Toolkit](/2013/02/10/install-netapp-dataontap-powershell/ "Install NetApp DataOnTap Powershell"), we have the ability to do monitor a lot of different things, and track the information using Solarwinds. In this post I will show how to monitor SnapMirror relationships using Solarwinds.

<!--more-->

Since my last post, I was able to find a document that gives a bit more… official insight into what Solarwinds expects in terms of Powershell script output. I’ve attached the PDF to the bottom of this post.

A big change from the last script, is that this one utilizes the “Message” field within solarwinds, whereas the old post only references the “Statistic” post.  This allows us to give more information as to why an issue might be occurring.

For example, let’s say a SnapMirror relationship is considered to be in  “critical” status if it has not been replicated in 480 minutes (or 4 hours), but you would like to know why this failure is occurring, without connecting to the CLI on your filer or NetApp System Manager (NSM). You can configure your Powershell to output important information in case of a failure. This script does just that. See an example screenshot below:

[![solarwinds-snapmirror-component](/wp-content/uploads/2013/02/solarwinds-snapmirror-component.png)](/wp-content/uploads/2013/02/solarwinds-snapmirror-component.png)

Important things to note about this script:

1. The filer that you will be connecting to is determined by how you have the Application Template / Component config.
2. The Snapmirror relationship you insert in the “script argument” field should appear just like the output of the source field output of a Get-NaSnapmirror command run directly from powershell.

[Configuring\_and\_Integrating\_PowerShell](https://new.virtjunkie.com/wp-content/uploads/2013/02/Configuring_and_Integrating_PowerShell.pdf) ([Alternate link](http://www.solarwinds.com/documentation/apm/docs/Configuring_and_Integrating_PowerShell.pdf))

The script is below:

```powershell
param (
    [string]$Location = $( Read-Host "The source location or destination \
    location of the SnapMirror pair" )
)
#***
# The Variable $location is filled in by Solarwinds. It accepts wildcards.
#***

############################ BEGIN GetVolumeAlert.ps1 ####################
# SnapMirror Alert Generator ~ v1.0 - Jon Howe
# REQUIRES NETAPP POWERSHELL TOOLKIT / PowerShell 2.0 recommended!
#
# Ensure that the variable ($profile) for the executing user contains the
# following line:
# import-module dataontap
##########################################################################

#Set the credentials for your filer.
$filerpassword = "[Enter Your Password Here]"

#The value ${IP} will be replaced by the server selected in Solarwinds
$Filername = '${IP}'

##########################################################################
# DO NOT EDIT BELOW THIS LINE
###########################################################################
Import-module DataONTAP
$password = ConvertTo-SecureString $filerpassword -AsPlainText –Force
$cred = New-Object -TypeName System.Management.Automation.PSCredential \
 -ArgumentList "root",$password
$connection =  Connect-NaController $Filername -Credential $cred

$SM_List = Get-NaSnapmirror -Location $Location

Foreach ($SM in $SM_List)
{
	$smError = $SM.CurrentTransferError
	$status = $SM.Status

	$rawSrc = $SM.Source
	# Apparently solarwinds freaks out when there's a colon in the
	$srcSplit = $rawSrc.Split(":")
	$srcFiler = $srcSplit[0]
	$srcVolume = $srcSplit[1]
	$src = "$srcVolume@$srcFiler"

	Write-Host "Statistic.$srcVolume :" $lag
	if ($smError)
	{
		Write-Host "Message.$srcVolume :" $status "-" $smError
	}
	Else
	{
		Write-Host "Message.$srcVolume :" $status
	}
}

exit(0)
```

As usual, if you have any questions about this, let me know!
