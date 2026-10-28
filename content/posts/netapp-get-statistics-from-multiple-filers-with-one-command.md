---
title: "NetApp: Get Statistics from Multiple Filers With One Command"
date: 2013-07-11T22:05:56-04:00
slug: "netapp-get-statistics-from-multiple-filers-with-one-command"
url: /2013/07/11/netapp-get-statistics-from-multiple-filers-with-one-command/
author:
  - "jhowe"
year: ["2013"]
month: ["2013-07"]
categories:
  - "netapp"
  - "powershell"
  - "scripting"
  - "automation"
  - "servers"
tags: []
aliases:
  - "/2013/07/11/netapp-get-statistics-from-multiple-filers-with-one-command/feed/"
---

Does anyone actually find NetApp OnCommand System Commander to be fast enough for normal operation? I’ll admit, I still create a good amount of Volumes and LUNs using it, but it leaves a lot to be desired in the performance category.  If you follow my blog at all, you know that I’m in the middle of a migration from a non-ha exchange environment to a DAG. Being the sensible admin that I am, I have multiple copies of my Exchange databases on different storage arrays, controlled by different NetApp filers. Using System Manager to monitor the space usage of the Volumes hosting my mailbox databases is way to slow for my comfort.

<!--more-->

While I could use PowerShell to get the status of volumes from only each individual filer replacing  using the following snippet:

```powershell
if (!(Get-Module dataontap)) { Import-Module DataOnTAP }
$filer1 = Connect-NaController filer1 -Credential (Get-Credential)
$filer2 = Connect-NaController filer2 -Credential (Get-Credential)
Get-NaVol -controller $filer1
Get-NaVol -controller $filer2
```

But that’s two commands… why would you want to enter two commands when you can enter one?!  Assuming you set up the controller objects in lines 2 and 3 above, you can simply run the command below to get all volumes from both Filer1 and Filer2:

```powershell
($filer1,$filer2) | % { Get-NaVol -Controller $_ }
```

While this gets volumes from all controllers, why on EARTH would you want to see the size in bytes?? Seriously…

Below is a finished script that gathers volume information from multiple filers, but also formats the output in a human readable format. If you have uniform naming convention for volumes in your filers, you can un-comment (remove the <# and #> ) and enter the prefix of your volume on line 15.

```powershell
# ========================================================================
# Created on:	7/11/2013 9:10 PM
# Created by:	Jon Howe
# URL: http://45.63.13.214/?p=510
# Filename:		Get-MultipleFilerVolStats.ps1
# ========================================================================

if (!(Get-Module dataontap)) { Import-Module DataOnTAP }

$filer1 = Connect-NaController filer1 -Credential (Get-Credential)
$filer2 = Connect-NaController filer2 -Credential (Get-Credential)
#$filer3 = Connect-NaController filer3 -Credential (Get-Credential)

($filer1,$filer2) | 
Foreach-object { Get-NaVol <#-name volPrefix #> -Controller $_ } | 
Select-Object Name,Used,Available | 
Format-Table -AutoSize -Property <code>
@{label="Volume";Expression={$_.Name}}, 
@{label="Percent Used";expression={$_.Used}}, `
@{label="Available";expression={[math]::round($_.Available / 1gb, 2)}
}
```
