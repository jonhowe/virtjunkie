---
title: "Validate Network Connectivity Across A VMware Cluster"
date: 2019-10-21T19:45:26-04:00
slug: "vsphere-test-cluster-connectivity"
url: /2019/10/21/vsphere-test-cluster-connectivity/
author:
  - "jhowe"
year: ["2019"]
month: ["2019-10"]
categories:
  - "automation"
  - "powershell"
  - "scripting"
  - "vmware"
tags: []
aliases:
  - "/vsphere-test-cluster-connectivity/"
  - "/2019/10/21/vsphere-test-cluster-connectivity/feed/"
---

> It’s the network team’s fault…

## The Scenario

Imagine you have an environment that has hundreds of VLANs. When you build a new cluster, there’s a real possibility that one host out of many is mis-configured on just a single port group or VLAN. It’s a pretty simple issue, but it’s like finding a needle in a haystack. Because of that, it’s incredibly difficult to troubleshoot, so I wrote a script to run through every ESXi host, and test connectivity on each port group.

<!--more-->

## How do we achieve this?

To recap, the goal here is to test network connectivity on all VLANs on all ESXi hosts in a cluster. The best way to do this is by creating a VMKernel port on each Port Group, and pinging a separate IP on the network *from* that VMKernel port. Once the ping results are recorded, the VMKernel port is deleted. Rinse and repeat for every VLAN on every ESXi host. The script will pull all info required for creating the VMKernel ports from a CSV file.

## Example Output

![](/wp-content/uploads/2019/10/image-1.png)

This is an example of the output you will get from running this script

## CSV File Details

The CSV file will contain the following fields: IP, GW, PG, NetMask, VLAN. Each row in the CSV will contain deails for a single VMKernel port. Here’s an example:

![](/wp-content/uploads/2019/10/image-300x44.png)

In the example above, three VMKernel ports will be created on every ESXi host in the cluster, and a ping attempt will occur to the IP listed in the “gw” column from the entry in the “IP” column.

## The Script

Now to the fun part, and why you’re actually here. First and foremost, you can see a copy of [GitHub Repository](https://github.com/jonhowe/Virtjunkie.com).

To run this script, you’ll need to pass variables as parameters or modify the default values. For example, you can run the script like this:

```text
PS> Test-ClusterNetworkConnectivity -vcenterserver "myvcenterserver.local" -vswitch "distributed switch name" -clustername "my special cluster" -csvpath c:\path\to\my.csv -verbose
```

- vCenter Server (-vcenterserver)
- The VDS in use (-vswitch)
- The desired cluster you want to focus on (-clustername)
- The CSV that contains info for the VMKernel ports (-csvpath)
- If you want verbose output printed to the screen (-verbose:$true/$false)

## Code Overview (and code)

**Lines 1-17**  
Documentation and parameters  
  
**Lines 18-30**  
Set up the environment, connect to vCenter, import the CSV, get the list of ESXi hosts to work with  
  
**Lines 31–33**  
Begin loop that goes through all ESXi hosts  
  
**Lines 34-36**  
Begin loop for each VMKernel port  
  
**Lines 37-50**  
Create splatting for variables  
Instantiate object  
  
**Lines 51-70**  
Create the VMKernel adapter, test the ping, optionally print verbose logging  
  
**Lines 71-80**  
Add results to an array  
  
**Lines 81-82**  
Remove the VMKernel port  
  
**Line 85-97**  
This block exists to handle an error with creating the VMKernel port.  
  
**Line 100**  
Add the results of the ping test to an array  
  
**Line 105-107**  
Output the array of results and disconnect from the vcenter server

```text
&lt;#
.LINK /2019/10/21/vsphere-test-cluster-connectivity/
.LINK https://github.com/jonhowe/Virtjunkie.com/blob/master/Test-ClusterNetworkConnectivity.ps1
#>
param(
	$vcenterserver = "vcenter67.pcm.net",
	$vswitch = "UCS-vDS001",
	$clustername = "UCS Cluster",
	$verbose = $false,
	$csvpath = "C:\powershell\PCMlab_test_csv.csv"
)

&lt;#
***Fields in the CSV***
IP, GW, PG, netmask, vlan
#>

#1.) connect to the vcenter
$credential = get-credential
$conn = connect-viserver -server $vcenterserver -credential $credential | out-null

#2.) Get a list of all VMhosts attached to the specified Switch and cluster
$vmhosts = get-vdswitch -name $vswitch | get-vmhost | Where-Object { $_.parent.name -eq $clustername }

#3.) Import the CSV file that has the IP, Gateway, Port Group, NetMask, and vLAN
$ALL_VMK_CSV_Rows = import-csv -path $csvpath

#Create array that stores results
$RS = @()

#3a.) Loop through each VMhost one at a time
foreach ($vmhost in $vmhosts)
{
	#Loop through each VMkernel in the CSV one at a time
	foreach ($ONE_VMK_CSV_ROW in $ALL_VMK_CSV_Rows)
	{
		#Splatting for parameters for new-vmhostnetworkadapter
		$NewVMKParams = @{
			VMHost = $vmhost
			PortGroup = $ONE_VMK_CSV_ROW.pg
			VirtualSwitch = $vswitch
			IP = $ONE_VMK_CSV_ROW.ip
			SubnetMask = $ONE_VMK_CSV_ROW.netmask
		}
		#Optional logging - disabled by default
		Write-Verbose -vb:$true -Message ($NewVMKParams | Out-String)
		
		#create new object to contain results
		$PingResults = New-Object System.Object

		#Test to see if the vmkernel port is created successfully.. if so, continue to test connectivity
		if ($vmkernel = new-vmhostnetworkadapter @NewVMKParams -ErrorAction SilentlyContinue)
		{
			#Get the newly created VMKernel adapter
			$vmkobj = Get-VMHostNetworkAdapter -VMHost $vmhost -VirtualSwitch (Get-VDSwitch -Name $vswitch) -VMKernel | 
				Where-Object { $_.devicename -eq $vmkernel.devicename }
		
			#Use ESXCli to emulate this command: vmkping -I [newly created vmkernel IP] TO: [Gateway IP Specified in the CSV]
			$esxcli = Get-EsxCli -VMHost $vmhost -V2
			$params = $esxcli.network.diag.ping.CreateArgs()
			$params.host = $ONE_VMK_CSV_ROW.GW
			$params.interface = $vmkobj.devicename
			#the $res variable contains the results of the ping.. if you want, you can see all of the result info by printing $res.summary
			$res = $esxcli.network.diag.ping.Invoke($params)
			
			#optional logging - disabled by default
			write-verbose -vb:$verbose -Message ($res.summary | Out-String)
			$output = ("[$($vmhost.name)]: $($res.summary.Recieved / $res.summary.transmitted * 100)% success. Source: $($ONE_VMK_CSV_ROW.ip) Target: $($res.summary.hostaddr) || PG $($ONE_VMK_CSV_ROW.pg) (VLAN: $($ONE_VMK_CSV_ROW.vlan))")
			Write-Verbose -vb:$verbose -Message $output

			#Add properties to the object
			$PingResults | Add-Member -type NoteProperty -name Cluster -Value $clustername        
			$PingResults | Add-Member -type NoteProperty -name VMHost -Value $vmhost.name
			$PingResults | Add-Member -type NoteProperty -name SourceIP -Value $ONE_VMK_CSV_ROW.ip
			$PingResults | Add-Member -type NoteProperty -name TargetIP -Value $res.summary.hostaddr
			$PingResults | Add-Member -type NoteProperty -name PortGroup -Value $ONE_VMK_CSV_ROW.pg
			$PingResults | Add-Member -type NoteProperty -name VLAN -Value $ONE_VMK_CSV_ROW.vlan
			$PingResults | Add-Member -type NoteProperty -name PercentSuccess -Value ($res.summary.Recieved / $res.summary.transmitted * 100)
			$PingResults | Add-Member -type NoteProperty -name vSwitch -Value $vswitch
			
			#3d.) Remove vmkernel port
			remove-vmhostnetworkadapter -nic $vmkobj -confirm:$false
		}
		#if the vmkernel adapter is not created successfully, report the failure
		Else
		{
			#Optional Logging - disabled by default
			$output = ("[$($vmhost.name)]: ERROR || PG $($ONE_VMK_CSV_ROW.pg) (VLAN: $($ONE_VMK_CSV_ROW.vlan)) does not exist on $($vswitch)")
			write-verbose -verbose:$verbose $output

			#Add properties to the object
			$PingResults | Add-Member -type NoteProperty -name Cluster -Value $clustername
			$PingResults | Add-Member -type NoteProperty -name VMHost -Value $vmhost.name
			$PingResults | Add-Member -type NoteProperty -name SourceIP -Value "ERROR"
			$PingResults | Add-Member -type NoteProperty -name TargetIP -Value "ERROR"
			$PingResults | Add-Member -type NoteProperty -name PortGroup -Value $ONE_VMK_CSV_ROW.pg
			$PingResults | Add-Member -type NoteProperty -name VLAN -Value $ONE_VMK_CSV_ROW.vlan
			$PingResults | Add-Member -type NoteProperty -name vSwitch -Value $vswitch
			$PingResults | Add-Member -type NoteProperty -name PercentSuccess -Value "ERROR"
		}

		#add object to array
		$RS += $PingResults

	} # end foreach ($ONE_VMK_CSV_ROW in $ALL_VMK_CSV_Rows)
} # end foreach ($vmhost in $vmhosts)

Write-Output $RS
#3e.) Disconnect from all vCenters
disconnect-viserver -server * -confirm:$false
```
