---
title: "Deploy VCSA via PowerShell"
date: 2020-03-16T09:00:00-04:00
slug: "deploy-vcsa-via-powershell"
url: /2020/03/16/deploy-vcsa-via-powershell/
author:
  - "jhowe"
year: ["2020"]
month: ["2020-03"]
categories:
  - "automation"
  - "powershell"
  - "scripting"
  - "vmware"
tags: []
aliases:
  - "/deploy-vcsa-via-powershell/"
  - "/2020/03/16/deploy-vcsa-via-powershell/feed/"
---

![](/wp-content/uploads/2014/04/powercli-icon.jpg)

I’ve been spending a lot of time lately thinking about how organizations can provide services can operationalize the principles behind Infrastructure as Code in a way that’s accessible. In my experience, if a tool isn’t easy to use, it won’t be used. This is one of the biggest barriers to organizations (and companies that provide services, like mine) benefiting from IaC. It’s my intention that this script will achieve a high level of usability and will also generate and consume reusable code for future use.

<!--more-->

Table of Contents

Toggle

- [Recap](#Recap "Recap")
- [Background](#Background "Background")
- [Demo](#Demo "Demo")
- [Features](#Features "Features")
- [Requirements](#Requirements "Requirements")
- [Code Review](#Code_Review "Code Review")
- [Code](#Code "Code")
- [What’s next?](#Whats_next "What’s next?")

## Recap

### Challenge

You want to use Infrastructure as Code principles to deploy your vCenter Server, but you want to ensure that your solution is accessible without code as well.

### Solution

Create a script that gathers all relevant information for a VCSA deployment via the the [vcsa-deploy](https://docs.vmware.com/en/VMware-vSphere/6.7/com.vmware.vcenter.install.doc/GUID-4CCC26AB-D2E4-40D0-97A8-804FB6274009.html) and generates the JSON file that the utility consumes, while also allowing for the download of the VCSA ISO from a web server.

## Background

In order for this to fit my definition of infrastructure as code, we should be able to define all details of the vCenter in a structured format. Additionally, we should not assume that the vCenter installer is local, and should pull it from an external location if we need it to. While the vcsa-deploy utility can handle the installation of the vCenter, I’ve found most people don’t like it.

With this script, I allow a VI admin to fill out all relevant details of the vCenter in a spreadsheet. The script will then access the spreadsheet directly, and generate the JSON file used by vcsa-deploy. As a bonus, it will call the vcsa-deploy utility and kick off the actual deployment.

![](/wp-content/uploads/2020/03/2020-03-15_12-07-1024x233.png)

Screenshot of the excel file [on my GitHub account](https://github.com/jonhowe/Virtjunkie.com/tree/master/VCSA-AutoDeploy).

## Demo

![](/wp-content/uploads/2020/03/image-1024x726.png)

Quick demo – the installer up to where it deploys the VCSA

## Features

- Validate Password Complexity
- Provide Input via Excel Spreadsheet or JSON file
- Download ISO, extract contents
- Deploy vCenter to either ESXi or vCenter

## Requirements

- [ImportExcel module](https://github.com/dfinke/ImportExcel)
- 7-zip
- URL to a vCenter Server 6.7 Appliance ISO
- Standard vCenter Prerequisites (forward/reverse DNS, space, networking, etc) ([link](https://docs.vmware.com/en/VMware-vSphere/6.7/com.vmware.vcenter.upgrade.doc/GUID-752FCA83-1A9B-499E-9C65-D5625351C0B5.html))

## Code Review

The code can be located on my [github account](https://github.com/jonhowe/Virtjunkie.com/tree/master/VCSA-AutoDeploy). As per usual, let’s go through the code.  
  
**Lines 1-31**  
Documentation  
  
**Lines 32-58**  
Define parameters  
  
**Lines 66-91**  
Download and install the ISO  
  
**Lines** **93-130**  
Extract the ISO using 7-zip  
  
**Lines 133-139**  
Use import-excel to grab sections of the spreadsheet. There’s a bit of overhead, but my goal here was for the spreadsheet to look good.  
  
**Lines 141-152**  
Validate the password specified meets VMware’s requirements for the VCSA  
  
**Lines 154-172**  
Detect the OS  
  
**Lines 176-224**  
Determine whether we are deploying to a vCenter or an ESXi host and create the respective JSON. This is the only difference between deploying to a vCenter or an ESXi host.  
  
**Lines 226-298**  
Create a hashtable used for to create the rest of parameters common to a the json used by vcsa-deploy.  
  
**Lines 300-312**  
Write the JSON file to disk  
  
**Lines 314-333**  
Begin the install  
  
**Lines 335-343**  
Determine if the install was successful. If it failed, print out the error messages.

## Code

```text
#Github: https://github.com/jonhowe/Virtjunkie.com/tree/master/VCSA-AutoDeploy
#Blog Post: http://www.virtjunkie.com/deploy-vcsa-via-powershell/

&lt;#
.SYNOPSIS
Install the VMware vCenter Server Appliance based on input from a Microsoft Excel File

.DESCRIPTION
This script will install the VMware vCenter Server Appliance based on input from a Microsoft Excel File.

.PARAMETER ForceDownload
Switch parameter that will force a (re) download and extract of the ISO

.PARAMETER URI
This is the URL of the vCenter Installer ISO

.PARAMETER Workspace
Absolute path to the directory that will be used as a workspace. The vCenter ISO will be downloaded there, and will be
extracted there as well.

.PARAMETER DeploymentTarget
Location that the new VCSA will be deployed to.
Valid options are: ESXi, vCenter

.PARAMETER ExcelFile
Absolute path to the Excel file that contains the parameters required for vCenter to be built

.PARAMETER 7z
Absolute path path to the 7z binary
#>
#Requires -modules Microsoft.powershell.archive,importexcel
[CmdletBinding()]
param (
    [switch]$ForceDownload
    ,
    $URI = "http://jondesktop.home.lan:8123/files/VMware/VSMRepo/dlg_VC67U3B/VMware-VCSA-all-6.7.0-15132721.iso"
    ,
    [Parameter(Mandatory=$true)]
    [ValidateScript( {
            if ( -Not ($_ | Test-Path) ) {
                throw "File or folder does not exist"
            }
            return $true
        })]
    $Workspace
    ,
    [validateset("vCenter", "ESXi")]
    $deploymentTarget
    ,
    [ValidateScript( { Test-Path $_ })]
    [string]
    $ExcelFile = "/home/jhowe/git/Personal/AutomatedLab/JonAutoLab/HostDetails.xlsx"
    ,
    [Parameter(Mandatory=$true)]
    [ValidateScript( { Test-Path $_ })]
    [string]
    $7z = '/usr/bin/7z'
)
$ErrorActionPreference = 'Stop'

#region Download and Extract the ISO
$VCSA_Installer_Archive = $workspace + ($uri.Split('/')[-1])
$VCSA_Extracted_Directory = ($VCSA_Installer_Archive.Split(".iso")[0])
$VCSA_CLI_Installer_Path = ($VCSA_Extracted_Directory + "/vcsa-cli-installer/")

#Download the VCSA only if it doesn't already exist
if ((Test-Path $VCSA_Installer_Archive) -eq $false -or $forcedownload) {
    $filesize = (Invoke-WebRequest $uri -Method Head).Headers.'Content-Length'
    [int]$WebServerFileSize = ([convert]::ToInt64($filesize, 10)) / 1024

    Write-Output "Downloading VCSA Installer"
    $wc = New-Object System.Net.WebClient
    $wc.DownloadFileAsync($uri, $VCSA_Installer_Archive)

    #The following loop will print the progressof the download every 15 seconds
    $incomplete = $true
    while ($incomplete) {
        $CurrentSize = ((Get-Item $VCSA_Installer_Archive).length) / 1024
    
        if ($CurrentSize -eq $WebServerFileSize) {
            $incomplete = $false
        }
        else {
            Write-Output "File Download Size is $([math]::round($CurrentSize,0)) / $($WebServerFileSize) ($(($CurrentSize / $WebServerFileSize).ToString("P") )%)"
            Start-Sleep -Seconds 15
        }
    }
}
else {
    Write-Output "VCSA Installer already exists"    
}

#Extract the VCSA only if the directory it should be extracted to doesn't already exist
if ((Test-Path ($VCSA_Extracted_Directory)) -eq $false -or $forcedownload) {
    Write-Output "Unzipping VCSA"
    #Expand-Archive -LiteralPath $VCSA_Installer_Archive -destinationpath $workspace

    Write-Output "Extracting the ISO now..."
    $arguments = "x -bb0 -bd -y -o$($VCSA_Extracted_Directory) $($VCSA_Installer_Archive)"
    Write-Verbose -Message ($7z + " " + $arguments)

    $pinfo = New-Object System.Diagnostics.ProcessStartInfo
    $pinfo.FileName = $7z
    $pinfo.RedirectStandardError = $true
    $pinfo.RedirectStandardOutput = $true
    $pinfo.UseShellExecute = $false
    $pinfo.Arguments = $arguments
    $p = New-Object System.Diagnostics.Process
    $p.StartInfo = $pinfo
    $p.Start() | Out-Null
    $p.WaitForExit()
    $7z_stdout = $p.StandardOutput.ReadToEnd()
    $7z_stderr = $p.StandardError.ReadToEnd()

    $7z_stdout | out-file -Path ($workspace + "7z-stdout.txt")
    $7z_stderr | out-file -Path ($workspace + "7z-stderr.txt")

    if ($p.ExitCode -ne 0) {
        Write-Output "There was an error..."
        Write-Output "Process finished with exit code $($p.ExitCode)"
        Write-Output "Log data written to: $($workspace)7z-stdout.txt and $($workspace)7z-stderr.txt"
        $7z_stderr
    }
    else {
        Write-Output "Extraction completed successfully."
    }
}
else {
    Write-Output "VCSA has already been unzipped"
}
#endregion Download and Extract the ISO

#region import excel file into sections and validate input
$targettype = Import-Excel $excelfile -WorksheetName vCenter -StartRow 1 -EndRow 2 -StartColumn 1 -EndColumn 1
$targetinfo = Import-Excel $excelfile -WorksheetName vCenter -StartRow 1 -EndRow 2 -StartColumn 2 -EndColumn 8
$applianceinfo = Import-Excel $excelfile  -WorksheetName vCenter -StartRow 4 -EndRow 5 -StartColumn 1 -EndColumn 3
$networkinfo = Import-Excel $excelfile  -WorksheetName vCenter -StartRow 7 -EndRow 8 -StartColumn 1 -EndColumn 7
$os = Import-Excel $excelfile  -WorksheetName vCenter -StartRow 10 -EndRow 11 -StartColumn 1 -EndColumn 3 
$sso_ciep = Import-Excel $excelfile  -WorksheetName vCenter -StartRow 13 -EndRow 14 -StartColumn 1 -EndColumn 3

#Ensure the password specified has the appropriate complexity based on vCenter's requirements
$input = ($os."vCenter Root Password")
if (($input -cmatch '[a-z]') `
        -and ($input -match '\d') `
        -and ($input.length -ge 8) `
        -and ($input -match '!|@|#|%|^|&amp;|$')) {
    Write-Output "Password complexity is sufficient. Continuing."
}
else {
    Write-Output "$input does not meet complexity requirements. Password must be at least 8 characters, include one numeric, and one special character."
    exit
}

$deploymentTarget = $targettype.'vCenter or ESXi'

#endregion import excel file into sections and validate input

#region Detect the OS (Windows, Linux, OSX)
if ($IsWindows -or $ENV:OS) {
    $installer_dir = ($VCSA_CLI_Installer_Path + "win32/")
    $installer = ($installer_dir + "vcsa-deploy.exe")
} 
elseif ($IsLinux) {
    $installer_dir = ($VCSA_CLI_Installer_Path + "lin64/")
    $installer = ($installer_dir + "vcsa-deploy")
    chmod -R +x $workspace
}
elseif ($IsMacOS) {
    $installer_dir = ($VCSA_CLI_Installer_Path + "mac/")
    $installer = ($installer_dir + "vcsa-deploy")
}
#endregion Detect the OS (Windows, Linux, OSX)

#region Create and format the JSON

#Detect whether we are deploying to vCenter or ESXi
switch ($deploymentTarget) {
    'vCenter' {
        Write-Output "Deploying to vCenter"
        $target = [ordered] @{
            vc = [ordered]@{
                __comments         = @("'datacenter' must end with a datacenter name, and only with a datacenter name. ",
                    "'target' must end with an ESXi hostname, a cluster name, or a resource pool name. ",
                    "The item 'Resources' must precede the resource pool name. ",
                    "All names are case-sensitive. ",
                    "For details and examples, refer to template help, i.e. vcsa-deploy {install|upgrade|migrate} --template-help")
                hostname           = $targetinfo."Target Host or vCenter"
                username           = $targetinfo."Username"
                password           = $targetinfo."Password"
                deployment_network = $targetinfo."PortGroup"

                &lt;#
                datacenter         = @("Folder 1 (parent of Folder 2)",
                                        "Folder 2 (parent of Your Datacenter)",
                                        "Your Datacenter")
                #>
                datacenter         = $targetinfo."Datacenter (vCenter Only)"
                datastore          = $targetinfo."Datastore"
                &lt;#
                target             = @( "Folder A (parent of Folder B)",
                                        "Folder B (parent of Your ESXi Host, or Cluster)",
                                        "Your ESXi Host, or Cluster")
                #>
                target             = $targetinfo."Cluster Name (vCenter Only)"
            }
        }
    }
    'ESXi' {
        Write-Output "Deploying to ESXi"
        $target = [ordered] @{
            esxi = [ordered]@{
                hostname           = $targetinfo."Target Host or vCenter"
                username           = $targetinfo."Username"
                password           = $targetinfo."Password"
                deployment_network = $targetinfo."PortGroup"
                datastore          = $targetinfo."Datastore"
            }
        }
    }
    Default {
        Write-Error "Invalid Deployment Target Specified. Exiting."
        exit
    }
}

&lt;#
I'm aware that others have imported the json file provided by the installer...
I don't have a great reason that I didn't do that.. maybe I'm just different :-)
Either way - we are simply generating a hashtable here, and then writing it to a file.
#>
$common_properties = @{
    appliance = [ordered]@{
        __comments        = @("You must provide the 'deployment_option' key with a value, which will affect the VCSA's configuration parameters, such as the VCSA's number of vCPUs, the memory size, the storage size, and the maximum numbers of ESXi hosts and VMs which can be managed. For a list of acceptable values, run the supported deployment sizes help, i.e. vcsa-deploy --supported-deployment-sizes")
        thin_disk_mode    = $applianceinfo."Thin Disk?"
        deployment_option = $applianceinfo."vCenter Size"
        name              = $applianceinfo."VM Name"
    }
    network   = [ordered]@{
        ip_family   = $networkinfo."IP v4 or v6"
        mode        = $networkinfo."IP Allocation Mode"
        ip          = $networkinfo."IP Address"
        dns_servers = @($networkinfo.'DNS Server List').split(",")
        prefix      = ($networkinfo."CIDR Block").tostring()
        gateway     = $networkinfo."Default Gateway"
        system_name = $networkinfo."vCenter Hostname"
    }
    os        = [ordered]@{
        password    = $os."vCenter Root Password"
        ntp_servers = $os."NTP Servers"
        ssh_enable  = $os."Enable SSH By Default?"
    }
    sso       = [ordered]@{
        password    = $sso_ciep."SSO Password"
        domain_name = $sso_ciep."SSO Domain Name"
    }
}

$combined = [ordered]@{
    __version  = "2.13.0"
    __comments = "Sample template to deploy a vCenter Server Appliance with an embedded Platform Services Controller on an ESXi host."
    new_vcsa   = $target + $common_properties
    ceip       = [ordered]@{
        description = @{
            __comments = @("++++VMware Customer Experience Improvement Program (CEIP)++++",
                "VMware's Customer Experience Improvement Program (CEIP) ",
                "provides VMware with information that enables VMware to ",
                "improve its products and services, to fix problems, ",
                "and to advise you on how best to deploy and use our ",
                "products. As part of CEIP, VMware collects technical ",
                "information about your organization's use of VMware ",
                "products and services on a regular basis in association ",
                "with your organization's VMware license key(s). This ",
                "information does not personally identify any individual. ",
                "",
                "Additional information regarding the data collected ",
                "through CEIP and the purposes for which it is used by ",
                "VMware is set forth in the Trust &amp; Assurance Center at ",
                "http://www.vmware.com/trustvmware/ceip.html . If you ",
                "prefer not to participate in VMware's CEIP for this ",
                "product, you should disable CEIP by setting ",
                "'ceip_enabled': false. You may join or leave VMware's ",
                "CEIP for this product at any time. Please confirm your ",
                "acknowledgement by passing in the parameter ",
                "--acknowledge-ceip in the command line.",
                "++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")       
        }
        
        settings    = @{ 
            #TODO I believe an extra member is needed if this is enabled
            ceip_enabled = $sso_ciep."Enable CIEP?"
        }
    }
}

$json = $combined | ConvertTo-Json -Depth 99
$fixtrue = $json.replace("`"true`"", "true")
$FinalJSON = $fixtrue.replace("`"false`"", "false")
#endregion Create and format the JSON

#region Write the json file to disk
switch ($deploymentTarget) {
    'vCenter' {  
        $FinalConfigFile = $workspace + "$(($FinalJSON | convertfrom-json).new_vcsa.vc.hostname).json"
    }
    'ESXi' {  
        $FinalConfigFile = $workspace + "$(($FinalJSON | convertfrom-json).new_vcsa.esxi.hostname).json"
    }
    Default { }
}
$FinalJSON | out-file -FilePath $FinalConfigFile
Write-Output ("JSON file written to: " + $FinalConfigFile)
#endregion Write the json file to disk

#region Start the install
Write-Output "Beginning install now.. this will take a few minutes. Please wait."
$arguments = "install --accept-eula --no-ssl-certificate-verification --log-dir $($VCSA_CLI_Installer_Path) $($FinalConfigFile)"

$pinfo = New-Object System.Diagnostics.ProcessStartInfo
$pinfo.FileName = $installer
$pinfo.RedirectStandardError = $true
$pinfo.RedirectStandardOutput = $true
$pinfo.UseShellExecute = $false
$pinfo.Arguments = $arguments
$p = New-Object System.Diagnostics.Process
$p.StartInfo = $pinfo
$p.Start() | Out-Null
$p.WaitForExit()
$stdout = $p.StandardOutput.ReadToEnd()
$stderr = $p.StandardError.ReadToEnd()

$stdout | out-file -Path ($VCSA_CLI_Installer_Path + "stdout.txt")
$stderr | out-file -Path ($VCSA_CLI_Installer_Path + "stderr.txt")
#endregion Start the install

if ($p.ExitCode -ne 0) {
    Write-Output "There was an error..."
    Write-Output "Process finished with exit code $($p.ExitCode)"
    Write-Output "Log data written to: $($VCSA_CLI_Installer_Path)stdout.txt and $($VCSA_CLI_Installer_Path)stderr.txt"
    $stderr
}
else {
    Write-Output "Install completed successfully."
}
```

## What’s next?

Good question! vSphere 7 is releasing vCenter Server Profiles and Image Cluster Management. Creating tools that can consume these new features will be helpful.  
  
I’m working on template management using [Hashicorp’s Packer](https://packer.io/) and will be posting some of my work on that soon. In addition, I have done some work on [Hashicorp’s Terraform](https://www.terraform.io/) for deploying lab VMs that I’ll share too. Finally – I’ve got a few skeleton [Ansible Playbooks](https://www.ansible.com/) that I’m working on for configuration of the lab VMs, as well as a playbook for doing high level configuration of a bare vCenter. So in short – lots more coming!

Thanks for viewing,  
Jon
