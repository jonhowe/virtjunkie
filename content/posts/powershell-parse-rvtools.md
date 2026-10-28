---
title: "RVTools: Parse Multiple Outputs Using Powershell"
date: 2019-08-11T11:00:14-04:00
slug: "powershell-parse-rvtools"
url: /2019/08/11/powershell-parse-rvtools/
author:
  - "jhowe"
year: ["2019"]
month: ["2019-08"]
categories:
  - "automation"
  - "powershell"
  - "scripting"
  - "vmware"
tags: []
aliases:
  - "/powershell-parse-rvtools/"
  - "/2019/08/11/powershell-parse-rvtools/feed/"
---

If you haven’t used [RVTools](https://www.robware.net/rvtools/) before, I’d definitely suggest taking a look. In case you’re one of the few that has not used it, it’s a quick tool to generate a point-in-time report of the inventory/configuration/health of a vSphere environment. While it’s one of the best tools out there for a quick and dirty report of an environment, the challenge I often face is that it outputs *too much* data. The other challenge I’ve faced is that it’s incredibly difficult to combine and analyze data from multiple outputs.

<!--more-->

I created a PowerShell script to help with this. The end result is a PowerShell object that can be consumed in any way you like. In a future post, I’ll show how to take this output and create a new Excel spreadsheet.

The image below is an example of what the script below generates.

![](/wp-content/uploads/2019/08/image-4-1024x366.png)

Example Output

As an FYI, we’ll need to install the [ImportExcel modul](https://www.powershellgallery.com/packages/ImportExcel)[e](https://www.powershellgallery.com/packages/ImportExcel) in order to parse the excel file. If you want more information, check out the [GitHub repository](https://github.com/dfinke/ImportExcel) for ImportExcel.

To run this script, at a minimum, you’ll need to modify the `$spreadsheetdir` variable to point to a directory that contains your RVTools outputs. This is a parameter, so it can be done by adding the `-spreadsheetdir "[path to my RVTools directory]"` if you like, or just feel free to modify the script.

**Lines 12-45**  
Define column headers to be pulled for each spreadsheet  
  
**Line 50**  
Get the contents of the spreadsheet directory  
  
**Line 54**  
Loop through each spreadsheet in the spreadsheet directory  
  
**Lines 58**  
Get a distinct list of all clusters in the particular RVTools file. This will allow us to present the results one cluster at a time  
  
**Lines 68-82**  
Import the properties defined in lines 10-44 from the vInfo, vHost, and vDisk worksheet for later consumption  
  
**Lines 84-101**  
Do some math/formatting/voodoo to convert the values from RVTools into something useful  
  
**Lines 63,64 and 103-110**  
Take values from RVTools and calculations (from lines 84-101) and put them into a custom PowerShell object.

You can find the script in the public GitHub repository I keep all of the scripts for this site in:  
<https://github.com/jonhowe/Virtjunkie.com>

```text
&lt;#
.LINK /2019/08/11/powershell-parse-rvtools/
.LINK https://github.com/jonhowe/Virtjunkie.com/blob/master/Parse-RVTools-Generic.ps1
#>
param(
    # Migrate Powered Off VMs?
    [switch]$IncludePoweredOffVMs,

    # Directory that contains RVTools Exports
    $spreadsheetdir = "/path/to/directory/",
    
    # Array that contains column headers to be gathered from the vHost worksheet
    $vHostProperties = @(
        'Host', 
        "CPU usage %",
        "Memory usage %",
        'model',
        "Service Tag",
        "Current EVC",
        "Max EVC",
        "# VMs",
        "# Memory",
        "# Cores",
        "HT Active",
        "vCPUs per Core"
    ),

    # Array that contains column headers to be gathered from the vInfo worksheet
    $vInfoProperties = @(
        'VM',
        'Template',
        "HW version",
        "Provisioned MB",
        "In Use MB",
        "OS according to the VMware Tools",
        'memory'
    ),

    # Array that contains column headers to be gathered from the vDisk worksheet
    $vDiskProperties = @(
        "vm",
        "Raw LUN ID",
        "Raw Comp. Mode",
        "Shared Bus"
    )

)

# Get all spreadsheets in the spreadsheet directory
$spreadsheets = $spreadsheetdir | Get-ChildItem

$rs = @()
# Loop through all spreadsheets in the spreadsheet dir
foreach ($sheet in $SpreadSheets)
{
    # Use the importexcel module to import the vCluster Worksheet
    # We do this as an easy way to get the 
    $vCluster = Import-Excel -Path $sheet -Sheet vCluster
    
    foreach ($cluster in $vCluster)
    {
        $ClusterDetails = New-Object System.Object
        $ClusterDetails | Add-Member -type NoteProperty -name vCenter -Value ($cluster."VI SDK Server")
        $ClusterDetails | Add-Member -type NoteProperty -name Cluster -Value $cluster.name 
       
        # Parse and store the properties defined in the $vInfoProperties array
        #   from the vInfo tab
        $vInfo = Import-Excel -Path $sheet -WorksheetName vInfo | 
            Where-Object { $_.Cluster -eq $cluster.name } | 
            Select-Object $vInfoProperties

        # Parse and store the properties defined in the $vHostProperties array
        #   from the vHost tab
        $vHost = Import-Excel -Path $sheet -WorksheetName vHost | 
            Where-Object { $_.Cluster -eq $cluster.name } | 
            Select-Object $vHostProperties

        # Parse and store the properties defined in the $vDiskProperties array
        #   from the vDisk tab
        $vDisk = Import-Excel -Path $sheet -WorksheetName vDisk | 
            Where-Object {$_.Cluster -eq $cluster.name } | 
            Select-Object $vDiskProperties

        # Calculate the sum of the column Provisioned MB from all rows in the vInfo tab, convert to GB, and round
        $TotalProvisionedGB = [math]::round(($vInfo | Measure-Object -Sum "Provisioned MB").Sum / 1024, 2)
        $ClusterDetails | Add-Member -type NoteProperty -name TotalProvisionedGB -Value $TotalProvisionedGB        

        # Calculate the sum of the column In Use MB from all rows in the vInfo tab, convert to GB, and round
        $TotalInUseGB = [math]::round(($vInfo | Measure-Object -Sum "In Use MB").Sum / 1024, 2)
        $ClusterDetails | Add-Member -type NoteProperty -name TotalInUseGB -Value $TotalInUseGB
        
        # Calculate average vCPU to PCPU, the total RAM in the cluster, and the average RAM Usage
        $vCPUtoPCPU = [math]::round(($vHost | Measure-Object -Average "vCPUs per Core").average, 2)
        $clusterRAM = [math]::round(($vHost | Measure-Object -Sum "# Memory").Sum / 1024, 2)
        $AvgClusterRamUsage = [math]::round(($vHost | Measure-Object -Average "Memory Usage %").average, 2)

        #Detect RDMs and VMs with Shared Bus based on info in the vDisk sheet
        $RDMs = ($vDisk | ? { $_."Raw LUN ID" -ne $null})
        $SharedBusVMs = ($vDisk | ? { $_."Shared Bus" -ne $null -and $_."Shared Bus" -ne "noSharing" -and $_."Shared Bus" -ne 0})

        $clusterCoreCount = [math]::round(($cluster | Measure-Object -Sum "NumCpuCores").sum,0)

        $ClusterDetails | Add-Member -type NoteProperty -name AvgClusterRamUsage -Value $AvgClusterRamUsage
        $ClusterDetails | Add-Member -type NoteProperty -name ClusterRamGB -Value $clusterRAM
        $ClusterDetails | Add-Member -type NoteProperty -name ClusterVMCount -Value $vInfo.count
        $ClusterDetails | Add-Member -type NoteProperty -name ClusterHostCount -Value ($vHost.count)
        $ClusterDetails | Add-Member -type NoteProperty -name TotalClusterCores -Value $clusterCoreCount
        $ClusterDetails | Add-Member -type NoteProperty -name vCPUtoPCPU -Value ($vCPUtoPCPU)
        $ClusterDetails | Add-Member -type NoteProperty -name RDMCount -Value ($RDMs.count)
        $ClusterDetails | Add-Member -type NoteProperty -name SharedBusVMs -Value ($SharedBusVMs.count)
        
        $rs += $ClusterDetails
    }
}

$rs
```
