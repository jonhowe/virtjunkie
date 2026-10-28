---
title: "PowerCli – Deploy Linked Clone with Static IP"
date: 2019-07-18T22:36:32-04:00
slug: "powercli-linked-clone-static-ip"
url: /2019/07/18/powercli-linked-clone-static-ip/
author:
  - "jhowe"
year: ["2019"]
month: ["2019-07"]
categories:
  - "automation"
  - "powershell"
  - "scripting"
  - "servers"
  - "vmware"
tags: []
aliases:
  - "/2019/07/18/powercli-linked-clone-static-ip/feed/"
---

I’m not sure why it’s been so hard to find a snippet online that gives me the ability to create a linked clone while selecting a static IP address, but it was. I ended up writing a quick function to help.

<!--more-->

It should be pretty self explanatory.. just edit the variables in the parameter section and call the function.  
  
Cheers!

Github: <https://github.com/jonhowe/Virtjunkie.com/blob/master/Deploy-VM.ps1>

```text
function New-VirtJunkieLinkedClone {
    [CmdletBinding()]
    &lt;#
    Github: https://github.com/jonhowe/Virtjunkie.com/blob/master/Deploy-VM.ps1
    Link: /2019/07/18/powercli-linked-clone-static-ip/
    #>
    param (
        #vCenter Info
        $vCenter            = 'vcsa.home.lab',
        $username           = 'administrator@vsphere.local',
        $password           = 'VMWare1!',
        $TemplateCustomSpec = 'WS16to19',

        #Parent VM Info
        $ParentVMName       = 'WS16-GUI',
        $SnapshotName       = "Base",

        #New VM Info
        $VMName             = "vra-iaas-2",
        $VMIP               = "192.168.86.214",
        $VMNetmask          = "255.255.255.0",
        $VMGateway          = "192.168.86.1",
        $VMDNS              = "192.168.86.232"
    )
    
    begin {
        $vc_conn = Connect-VIServer -Server $vCenter -User $username -Password $password
    }
    
    process {
        # Get the OS CustomizationSpec and clone
        $OSCusSpec = Get-OSCustomizationSpec -Name $TemplateCustomSpec | 
            New-OSCustomizationSpec -Name 'tempcustomspec' -Type NonPersistent

        #Update Spec with IP information
        Get-OSCustomizationNicMapping -OSCustomizationSpec $OSCusSpec |
            Set-OSCustomizationNicMapping -IPMode UseStaticIP `
                -IPAddress $VMIP `
                -SubnetMask $VMNetmask  `
                -DefaultGateway $VMGateway `
                -Dns $VMDNS

        $mySourceVM = Get-VM -Name $ParentVMName
        $myReferenceSnapshot = Get-Snapshot -VM $mySourceVM -Name $SnapshotName 
        $Cluster = Get-Cluster 'Cluster'
        $myDatastore = Get-Datastore -Name 'Shared'

        New-VM -Name $VMName -VM $mySourceVM -LinkedClone -ReferenceSnapshot $myReferenceSnapshot -ResourcePool $Cluster `
        -Datastore $myDatastore -OSCustomizationSpec $OSCusSpec
    }
    
    end {
        Get-OSCustomizationSpec -Name $OSCusSpec | Remove-OSCustomizationSpec -Confirm:$false
    }
}
```
