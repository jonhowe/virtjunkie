---
title: "Monitor NetApp SAN via Solarwinds Server and Application Monitor"
date: 2013-02-12T21:57:12-05:00
slug: "monitor-netapp-san-via-solarwinds-server-and-application-monitor"
url: /2013/02/12/monitor-netapp-san-via-solarwinds-server-and-application-monitor/
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
  - "/2013/02/12/monitor-netapp-san-via-solarwinds-server-and-application-monitor/feed/"
---

I was unable to find any examples for how to do this online, so I came up with my own solution using the NetApp Data ONTAP toolkit as well as a slight modification of your powershell profile.

<!--more-->

You’ll need to [download the toolkit and install it on your SAM machine](/2013/02/10/install-netapp-dataontap-powershell/ "Install NetApp DataOnTap Powershell") as a prerequisite for this to work.

Additionally, I needed to modify the powershell profile of the user that will execute the script.  The location of the Powershell profile is stored in the variable $profile.  Just make sure that file contains the line

```powershell
import-module dataontap
```

After you get your environment all set, you’ll need to configure a new Application Template within SAM.

To do this, navigate to Admin -> Settings -> SAM Settings -> Create a New Template

The important Fields to fill in are:

Template Name: I recommend giving this a name that identifies the particular filer you’re connecting to

[![template1](/wp-content/uploads/2013/02/template1-300x113.png)](/wp-content/uploads/2013/02/template1.png)

Then Add a component monitor:

[![addComponentMonitor](https://new.virtjunkie.com/wp-content/uploads/2013/02/addComponentMonitor.png)](https://new.virtjunkie.com/wp-content/uploads/2013/02/addComponentMonitor.png)

Select the Windows PowerShell Monitor

[![newPowershellComponent](/wp-content/uploads/2013/02/newPowershellComponent.png)](/wp-content/uploads/2013/02/newPowershellComponent.png)

Paste the script below into the script body, and put the name of the volume in the “Script Arguments” field. As a bonus, you can use a wildcard in the Script Arguments field in order to monitor multiple volumes at the same time.

If you like, you can modify line 28 below to better fit your needs. For example, I have different component that has the line below in place. This allows me more flexibility than what I get by using the script arguments field.

```powershell
$VolArray = get-navol | Where-Object {$_.Name -eq "CIFS0" -or $_.Name \
-eq "CIFS1" -or $_.Name -eq "CIFS2"  -or $_.Name -eq "CIFS3" -or \
$_.Name -eq "CIFS4"}
```

```powershell
param (
[string]$Volume = $( Read-Host "Enter the volume name, please" )
)
############################ BEGIN GetVolumeAlert.ps1 ####################
# Volume Alert Generator ~ v1.0 - Jon Howe
# REQUIRES NETAPP POWERSHELL TOOLKIT / PowerShell 2.0 recommended!
#
# Ensure that the variable ($profile) for the executing user contains the
# following line:
# import-module dataontap
##########################################################################

#Set the credentials for your filer.
$filerpassword = "Enter Your Password Here"

#The value ${IP} will be replaced by the server selected in Solarwinds
$Filername = '${IP}'

##########################################################################
# DO NOT EDIT BELOW THIS LINE
###########################################################################
Import-module DataONTAP
$password = ConvertTo-SecureString $filerpassword -AsPlainText –Force
$cred = New-Object -TypeName System.Management.Automation.PSCredential \
 -ArgumentList "root",$password
$connection = Connect-NaController $Filername -Credential $cred

$VolArray = get-navol -Name $Volume

foreach ($vol in $VolArray)
{
 $name = $vol.Name
 $percent = $vol.Used

 # This is important - Solarwinds requires a "Unique identifier" for
 # each value returned by a script. The line below creates an
 # identifier for each result returned.
 Write-Host "Statistic.$name :" $percent
}

#Solarwinds requires that this be included in a PowerShell script.
exit(0)
```

I’m using this right now to monitor a production environment with a lot of success. If you want to see a different setup, let me know!
