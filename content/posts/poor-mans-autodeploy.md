---
title: "Poor Man’s AutoDeploy Using Custom Kickstart, and Python"
date: 2020-04-09T09:00:00-04:00
slug: "poor-mans-autodeploy"
url: /2020/04/09/poor-mans-autodeploy/
author:
  - "jhowe"
year: ["2020"]
month: ["2020-04"]
categories:
  - "automation"
  - "python"
  - "scripting"
  - "vmware"
tags: []
aliases:
  - "/poor-mans-autodeploy/"
  - "/Poor-Mans-AutoDeploy/"
  - "/2020/04/09/poor-mans-autodeploy/feed/"
---

I recently encountered a situation where I needed to provision hundreds of ESXi hosts. The thing is, there was no vSphere Autodeploy, or HPE Synergy Image Streamer, and no ability to (long story, trust me here) spin them up. No way I’m going to manually provision all of those hosts by hand, so what’s a guy to do?!

This solution will automatically provision ESXi hosts and “get them on the network” so you can add them to vCenter just by using tools that VMware gives us, and a little bit of creativity.

While I designed this solution to work with hundreds of production ESXi hosts, there’s nothing from preventing you from using this method in smaller production environments, or even your own home lab.

<!--more-->

Table of Contents

Toggle

- [Overview](#Overview "Overview")
  - [Diagram](#Diagram "Diagram")
- [Modified Boot.cfg file](#Modified_Bootcfg_file "Modified Boot.cfg file")
  - [boot.cfg code](#bootcfg_code "boot.cfg code")
- [Kickstart file (ks.cfg)](#Kickstart_file_kscfg "Kickstart file (ks.cfg)")
  - [Stage 1](#Stage_1 "Stage 1")
  - [Stage 2](#Stage_2 "Stage 2")
  - [ks.cfg code](#kscfg_code "ks.cfg code")
- [Host Detail Spreadsheet](#Host_Detail_Spreadsheet "Host Detail Spreadsheet")
- [configureHost.py](#configureHostpy "configureHost.py")
  - [configureHost.py code](#configureHostpy_code "configureHost.py code")
- [Web Server](#Web_Server "Web Server")
  - [Docker Container](#Docker_Container "Docker Container")
  - [Directory structure](#Directory_structure "Directory structure")
  - [Web Server In Action](#Web_Server_In_Action "Web Server In Action")
- [Create ISO](#Create_ISO "Create ISO")
- [References](#References "References")

## Overview

At a very high level, the process works as follows.. The physical server boots from an ISO, USB Image, or even CD/DVD, if you’re into that sort of thing. The ESXi image on this media will contain a slightly customized ESXi image that looks for a kickstart file pulls the rest of the install instructions from a kickstart file on a web server. This kickstart fill will handle the silent install of ESXi, reboot into the newly installed OS, set a few settings, then download a CSV that contains ESXi host configuration info (such as host name, IP, and Default Gateway), and a python script that will send esxcli commands to the host in order to configure networking.

### Diagram

![](/wp-content/uploads/2020/04/Poor-Mans-AutoDeploy-2048x823.jpeg)

## Modified Boot.cfg file

First and foremost, I need to emphasize the fact that there are two places you need to put your boot.cfg file. One in the root of the filesystem you have on your media, and one in the efi folder. This file is read during the boot process and instructs ESXi on how to boot. We care about the line that begins with **kernelopt=**. By default, this line tells ESXi to start with the traditional GUI installer which we definitely don’t want. Instead, we’ll modify it to tell the installer to look for a kickstart file on a web server, and will set static networking for the host.

At a high level, the modifications here accomplish the following:

1. Instruct the ESXi host to find a kickstart file on a web server
2. Set a static IP, netmask, default gateway, and nameserver to use prior to automatically configuring the host

### boot.cfg code

[Here’s a link to the code](https://github.com/jonhowe/Virtjunkie.com/tree/master/PoorMansAutoDeploy/esxi-iso)

```text
bootstate=0
title=Loading ESXi installer
timeout=5
prefix=
kernel=/b.b00
#kernelopt=cdromBoot runweasel
kernelopt=ks=http://vmware-ks.home.lab:8123/files/VMware/ks/ks.cfg nameserver=192.168.1.60 ip=192.168.1.5 netmask=255.255.255.0 gateway=192.168.1.1
modules=/jumpstrt.gz --- /useropts.gz --- /features.gz --- /k.b00 --- /chardevs.b00 --- /user.b00 --- /procfs.b00 --- /uc_intel.b00 --- /uc_amd.b00 --- /uc_hygon.b00 --- /vmx.v00 --- /vim.v00 --- /sb.v00 --- /s.v00 --- /ata_liba.v00 --- /ata_pata.v00 --- /ata_pata.v01 --- /ata_pata.v02 --- /ata_pata.v03 --- /ata_pata.v04 --- /ata_pata.v05 --- /ata_pata.v06 --- /ata_pata.v07 --- /block_cc.v00 --- /bnxtnet.v00 --- /bnxtroce.v00 --- /brcmfcoe.v00 --- /char_ran.v00 --- /ehci_ehc.v00 --- /elxiscsi.v00 --- /elxnet.v00 --- /hid_hid.v00 --- /i40en.v00 --- /iavmd.v00 --- /igbn.v00 --- /ima_qla4.v00 --- /ipmi_ipm.v00 --- /ipmi_ipm.v01 --- /ipmi_ipm.v02 --- /iser.v00 --- /ixgben.v00 --- /lpfc.v00 --- /lpnic.v00 --- /lsi_mr3.v00 --- /lsi_msgp.v00 --- /lsi_msgp.v01 --- /lsi_msgp.v02 --- /misc_cni.v00 --- /misc_dri.v00 --- /mtip32xx.v00 --- /ne1000.v00 --- /nenic.v00 --- /net_bnx2.v00 --- /net_bnx2.v01 --- /net_cdc_.v00 --- /net_cnic.v00 --- /net_e100.v00 --- /net_e100.v01 --- /net_enic.v00 --- /net_fcoe.v00 --- /net_forc.v00 --- /net_igb.v00 --- /net_ixgb.v00 --- /net_libf.v00 --- /net_mlx4.v00 --- /net_mlx4.v01 --- /net_nx_n.v00 --- /net_tg3.v00 --- /net_usbn.v00 --- /net_vmxn.v00 --- /nfnic.v00 --- /nhpsa.v00 --- /nmlx4_co.v00 --- /nmlx4_en.v00 --- /nmlx4_rd.v00 --- /nmlx5_co.v00 --- /nmlx5_rd.v00 --- /ntg3.v00 --- /nvme.v00 --- /nvmxnet3.v00 --- /nvmxnet3.v01 --- /ohci_usb.v00 --- /pvscsi.v00 --- /qcnic.v00 --- /qedentv.v00 --- /qfle3.v00 --- /qfle3f.v00 --- /qfle3i.v00 --- /qflge.v00 --- /sata_ahc.v00 --- /sata_ata.v00 --- /sata_sat.v00 --- /sata_sat.v01 --- /sata_sat.v02 --- /sata_sat.v03 --- /sata_sat.v04 --- /scsi_aac.v00 --- /scsi_adp.v00 --- /scsi_aic.v00 --- /scsi_bnx.v00 --- /scsi_bnx.v01 --- /scsi_fni.v00 --- /scsi_hps.v00 --- /scsi_ips.v00 --- /scsi_isc.v00 --- /scsi_lib.v00 --- /scsi_meg.v00 --- /scsi_meg.v01 --- /scsi_meg.v02 --- /scsi_mpt.v00 --- /scsi_mpt.v01 --- /scsi_mpt.v02 --- /scsi_qla.v00 --- /sfvmk.v00 --- /shim_isc.v00 --- /shim_isc.v01 --- /shim_lib.v00 --- /shim_lib.v01 --- /shim_lib.v02 --- /shim_lib.v03 --- /shim_lib.v04 --- /shim_lib.v05 --- /shim_vmk.v00 --- /shim_vmk.v01 --- /shim_vmk.v02 --- /smartpqi.v00 --- /uhci_usb.v00 --- /usb_stor.v00 --- /usbcore_.v00 --- /vmkata.v00 --- /vmkfcoe.v00 --- /vmkplexe.v00 --- /vmkusb.v00 --- /vmw_ahci.v00 --- /xhci_xhc.v00 --- /elx_esx_.v00 --- /btldr.t00 --- /esx_dvfi.v00 --- /esx_ui.v00 --- /esxupdt.v00 --- /weaselin.t00 --- /lsu_hp_h.v00 --- /lsu_inte.v00 --- /lsu_lsi_.v00 --- /lsu_lsi_.v01 --- /lsu_lsi_.v02 --- /lsu_lsi_.v03 --- /lsu_lsi_.v04 --- /lsu_smar.v00 --- /native_m.v00 --- /qlnative.v00 --- /rste.v00 --- /vmware_e.v00 --- /vsan.v00 --- /vsanheal.v00 --- /vsanmgmt.v00 --- /tools.t00 --- /xorg.v00 --- /imgdb.tgz --- /imgpayld.tgz
build=
updated=0
```

## Kickstart file (ks.cfg)

The kickstart file provides the ESXi installer with all the information it needs to perform the installation without manual intervention. We are handling this in two stages by using the firstboot parameter.

### Stage 1

Handles the installation of ESXi to physical hardware. The following tasks are completed:

1. Accept EULA
2. Select disk for ESXi to be installed to
3. Set root password
4. Set IP to be used on first boot (Default is DHCP, but the code to use static is included/commented in the code)

### Stage 2

All of stage two is executed in the newly installed ESXi OS using the firstboot parameter. The following tasks are completed:

1. Enable SSH and ESXi Shell
2. Disable warnings for #1
3. Disable ESXi Firewall so we can use wget
4. Using wget, download the following files
   1. ListOfHosts.csv
   2. configurehost.py
5. Set the execution bit on the python script
6. Execute the python script

### ks.cfg code

[Here’s a link to the code](https://github.com/jonhowe/Virtjunkie.com/blob/master/PoorMansAutoDeploy/ks.cfg)

```text
#__      ___      _       _             _    _      
#\ \    / (_)    | |     | |           | |  (_)     
# \ \  / / _ _ __| |_    | |_   _ _ __ | | ___  ___ 
#  \ \/ / | | '__| __|   | | | | | '_ \| |/ / |/ _ \
#   \  /  | | |  | || |__| | |_| | | | |   &lt;| |  __/
#    \/   |_|_|   \__\____/ \__,_|_| |_|_|\_\_|\___|

#Jon Howe
#https://www.virtjunkie.com/Poor-Mans-AutoDeploy
#https://github.com/jonhowe/Virtjunkie.com/tree/master/PoorMansAutoDeploy

#  _____ _                     __            _____           _        _ _       _   _             
# / ____| |                   /_ |          |_   _|         | |      | | |     | | (_)            
#| (___ | |_ __ _  __ _  ___   | |  ______    | |  _ __  ___| |_ __ _| | | __ _| |_ _  ___  _ __  
# \___ \| __/ _` |/ _` |/ _ \  | | |______|   | | | '_ \/ __| __/ _` | | |/ _` | __| |/ _ \| '_ \ 
# ____) | || (_| | (_| |  __/  | |           _| |_| | | \__ \ || (_| | | | (_| | |_| | (_) | | | |
#|_____/ \__\__,_|\__, |\___|  |_|          |_____|_| |_|___/\__\__,_|_|_|\__,_|\__|_|\___/|_| |_|
#                  __/ |                                                                          
#                 |___/                                                                           

# Accept the VMware End User License Agreement
vmaccepteula

# The install media is in the CD-ROM drive
#   This was the hardest part for some reason. I was installing from a USB drive TO a separate USB drive.
#   https://docs.vmware.com/en/VMware-vSphere/6.7/com.vmware.esxi.upgrade.doc/GUID-61A14EBB-5CF3-43EE-87EF-DB8EC6D83698.html
#   https://docs.vmware.com/en/VMware-vSphere/6.7/com.vmware.esxi.upgrade.doc/GUID-E7274FBA-CABC-43E8-BF74-2924FD3EFE1E.html
#   If you find the wrong device is being selected, you can hit CTRL+F1 during the install, log in (root/&#91;no password]) and enter
#   the following command to get a list of the available devices:
#   localcli storage core device list
install --disk=/vmfs/devices/disks/mpx.vmhba33:C0:T0:L0 --overwritevmfs --novmfsondisk

# Set the root password for the DCUI and Tech Support Mode
rootpw VMware1!

### Temporary Network Configuration
#   Keep in mind, this is temporary. The actual IP address will be set in Stage 2
#   We don't even technically need this, but I wanted to include it in case we need network connectivity in Stage 1

# Set the network to DHCP on the first network adapter
network --bootproto=dhcp --device=vmnic0
# ... or if you want, you can set this to static
# network --bootproto=static --ip=192.168.30.13 --netmask=255.255.255.0 --gateway=192.168.30.1 --hostname=esxi1-mgmt.home.lab --nameserver=192.168.0.1 --addvmportgroup=1

reboot

#  _____ _                     ___              _____ _                 _         _____             __ _       
# / ____| |                   |__ \            / ____(_)               | |       / ____|           / _(_)      
#| (___ | |_ __ _  __ _  ___     ) |  ______  | (___  _ _ __ ___  _ __ | | ___  | |     ___  _ __ | |_ _  __ _ 
# \___ \| __/ _` |/ _` |/ _ \   / /  |______|  \___ \| | '_ ` _ \| '_ \| |/ _ \ | |    / _ \| '_ \|  _| |/ _` |
# ____) | || (_| | (_| |  __/  / /_            ____) | | | | | | | |_) | |  __/ | |___| (_) | | | | | | | (_| |
#|_____/ \__\__,_|\__, |\___| |____|          |_____/|_|_| |_| |_| .__/|_|\___|  \_____\___/|_| |_|_| |_|\__, |
#                  __/ |                                         | |                                      __/ |
#                 |___/                                          |_|                                     |___/ 

%firstboot --interpreter=busybox

# enable &amp; start SSH
vim-cmd hostsvc/enable_ssh
vim-cmd hostsvc/start_ssh

# enable &amp; start ESXi Shell
vim-cmd hostsvc/enable_esx_shell
vim-cmd hostsvc/start_esx_shell

# Suppress ESXi Shell warning
esxcli system settings advanced set -o /UserVars/SuppressShellWarning -i 1

#Temporarily disable the firewall so we can grab a couple files using wget
esxcli network firewall set --enabled false

# Download Host Config CSV, host configuration script, and execute the host configuration script
wget -O ListOfHosts.csv http://jondesktop.home.lan:8123/files/VMware/ks/ListOfHosts.csv
wget -O configurehost.py http://jondesktop.home.lan:8123/files/VMware/ks/configurehost.py
chmod u+x configurehost.py
/bin/python configurehost.py

#Re-enable the firewall
esxcli network firewall set --enabled true
```

## Host Detail Spreadsheet

I like to have all, or as much configuration as possible defined in a document, and consume that as a part of the provisioning process. In this case, since I’m executing this on an ESXi host using the version of python that is available to the host, I’m simply using a CSV file. This strikes a healthy balance between usability and functionality.  
  
[Here’s a link to the CSV on my github account](https://github.com/jonhowe/Virtjunkie.com/blob/master/PoorMansAutoDeploy/ListOfHosts.csv)

The columns are as follows:

|  |  |
| --- | --- |
| Column A | ESXi Hostname |
| Column B | MAC Address of vmnic0 |
| Column C | Desired Management IP Address (vmk0) |
| Column D | Subnet Mask for vmk0 |
| Column E | Default Gateway for vmk0 |
| Column F | VLAN Assigned to vmk0 |

Note: Columns have been converted to rows in this table. The actual representation is shown in the image below.

![](/wp-content/uploads/2020/04/image-768x124.png)

## configureHost.py

Here’s where the magic comes in… Since ESXi is deployed with python, we can use it to parse a CSV file that has a list of all details for an ESXi host, and set the relevant details for the host.  
[Here’s a link to the code](https://github.com/jonhowe/Virtjunkie.com/blob/master/PoorMansAutoDeploy/configurehost.py)

In this very basic example, we are doing the following based on input in the CSV file:

1. Set the hostname
2. Set the IP Address and Netmask of vmk0
3. Set the default gateway for the host
4. Set the VLAN for the management port group on vSwitch0

### configureHost.py code

```text
#__      ___      _       _             _    _      
#\ \    / (_)    | |     | |           | |  (_)     
# \ \  / / _ _ __| |_    | |_   _ _ __ | | ___  ___ 
#  \ \/ / | | '__| __|   | | | | | '_ \| |/ / |/ _ \
#   \  /  | | |  | || |__| | |_| | | | |   &lt;| |  __/
#    \/   |_|_|   \__\____/ \__,_|_| |_|_|\_\_|\___|
                                                  
#Jon Howe
#https://www.virtjunkie.com/Poor-Mans-AutoDeploy
#https://github.com/jonhowe/Virtjunkie.com/tree/master/PoorMansAutoDeploy

import os, csv, subprocess

CSVPATH = '/ListOfHosts.csv'

#Gets all mac addresses of interfaces
MAC=subprocess.check_output("esxcli network ip interface list |grep MAC | cut -d ' ' -f 6",shell=True)
                                                                                                                                                                                                                                                                                    
MACADDR = MAC.split()
print("MAC Addresses:")
print(MACADDR)

#Open the CSV file
with open(CSVPATH, 'rt') as csvFile:
        csvReader = csv.reader(csvFile)
        #Process the CSV file, row by row
        for csvRow in csvReader:
                #Check to see if the Mac Address of vmnic0 (IE: MACADDR&#91;0]) matches the row in the CSV we are looking at
                if ((MACADDR&#91;0]).decode('utf-8')) == csvRow&#91;1]:
                        #print("esxcli system hostname set --fqdn=" + csvRow&#91;0])
                        #print("esxcli network ip interface ipv4 set --interface-name=vmk0 --ipv4=" + csvRow&#91;2] + " --netmask=" + csvRow&#91;3] + " --type=static")
                        
                        #Set the hostname to the value in the CSV
                        os.system("esxcli system hostname set --fqdn=" + csvRow&#91;0])
                        
                        #Set the IP Address and Netmask of vmk0
                        os.system("esxcli network ip interface ipv4 set --interface-name=vmk0 --ipv4=" + csvRow&#91;2] + " --netmask=" + csvRow&#91;3] + " --type=static")
                        
                        #Add the default gateway
                        os.system("esxcfg-route " + csvRow&#91;4])
                        
                        #Add the desired VLAN for the Management Network on the vSwitch that gets created by default (vSwitch0)
                        os.system("esxcfg-vswitch -p 'Management Network' -v " + csvRow&#91;5] + " vSwitch0")
```

## Web Server

Since none of this works without a web server, we’ll need to make sure we have one available. My goal in creating this was to have the whole project be as portable as possible. To that effort, I use a small docker container I can start/stop on my laptop or workstation that hosts the required files, but there’s nothing preventing you from doing this on a production server as well. I’m using a container that has a nice graphical directory browser, but also allows for direct downloading of files. [Here’s a link to more information about this container](https://hub.docker.com/r/mohamnag/nginx-file-browser)

As a side note, in a [previous blog post, I spoke about deploying VCSA](/deploy-vcsa-via-powershell/) based on properties in an Excel file. One of the prerequisites for this to work is to have a web server that hosts the ISO file. I use this same container to serve the files for that project.

### Docker Container

The following snippet can be used to create a docker container to host the files required by this project.

```text
docker run -p 8123:80 -v /storage/poormansautodeploy/ks/:/opt/www/files --name=filebrowser -d --restart unless-stopped --log-opt max-size=15m --log-opt max-file=2 mohamnag/nginx-file-browser
```

### Directory structure

```text
ks
├── configurehost.py
├── ks.cfg
└── ListOfHosts.csv
```

### Web Server In Action

![](/wp-content/uploads/2020/04/image-1.png)

## Create ISO

This is the process to create a custom ISO

```text
genisoimage -relaxed-filenames -J -R -o &#91;yourisoname].iso -b isolinux.bin -c boot.cat -no-emul-boot -boot-load-size 4 -boot-info-table -eltorito-alt-boot -e efiboot.img -no-emul-boot &#91;path to extracted iso]
```

## References

- I owe a big thank you to Andrew Dauncey ([twitter](https://twitter.com/daunce_), [blog](https://theoddangryshot.com/), [github](https://github.com/daunce)). He created [a post](https://theoddangryshot.com/2016/09/07/esxi-kickstart-with-python/) back in 2016 that accomplished something similar to this, but was no longer working with modern versions of vSphere. I updated the code to work with vSphere, and added some additional functionality. Thanks again Andrew!
- As always, the VMware documentation is a good place to start. Here’s the documentation for 6.7 ([link](https://docs.vmware.com/en/VMware-vSphere/6.7/com.vmware.esxi.upgrade.doc/GUID-870A07BC-F8B4-47AF-9476-D542BA53F1F5.html)) and here’s the documentation for 7.0 ([link](https://docs.vmware.com/en/VMware-vSphere/7.0/com.vmware.esxi.upgrade.doc/GUID-870A07BC-F8B4-47AF-9476-D542BA53F1F5.html))
