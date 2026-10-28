---
title: "VMware Template Management using Hashicorp Packer"
date: 2020-03-23T09:00:00-04:00
slug: "vmware-template-packer"
url: /2020/03/23/vmware-template-packer/
author:
  - "jhowe"
year: ["2020"]
month: ["2020-03"]
categories:
  - "automation"
  - "packer"
  - "hashicorp"
  - "scripting"
  - "vmware"
tags: []
aliases:
  - "/vmware-template-packer/"
  - "/2020/03/23/vmware-template-packer/feed/"
---

VMware Templates: they make life amazing, don’t they? Creating a your first vSphere template is easy, but there are limitations when using them in enterprise environments. In this article, I will talk about the downsides of traditional enterprise template management, how Packer can help, and give examples (and code!) for creating Windows and Linux templates in VMware vCenter using Packer.

Table of Contents

Toggle

- [Traditional Enterprise Template Management](#Traditional_Enterprise_Template_Management "Traditional Enterprise Template Management")
- [Enterprise Template Management With Packer](#Enterprise_Template_Management_With_Packer "Enterprise Template Management With Packer")
- [Source Code](#Source_Code "Source Code")
- [Packer Intro](#Packer_Intro "Packer Intro")
- [Packer Template File & User Variables](#Packer_Template_File_User_Variables "Packer Template File & User Variables")
  - [Builders](#Builders "Builders")
  - [Attaching ISOs and Floppy Images](#Attaching_ISOs_and_Floppy_Images "Attaching ISOs and Floppy Images")
    - [ISOs](#ISOs "ISOs")
    - [Floppy Images](#Floppy_Images "Floppy Images")
  - [Communicators](#Communicators "Communicators")
  - [Provisioners](#Provisioners "Provisioners")
- [Linux Templates](#Linux_Templates "Linux Templates")
- [Windows Templates](#Windows_Templates "Windows Templates")
  - [Autounattend.xml](#Autounattendxml "Autounattend.xml")
    - [windowsPE](#windowsPE "windowsPE")
    - [offlineServicing](#offlineServicing "offlineServicing")
    - [generalize](#generalize "generalize")
    - [specialize](#specialize "specialize")
    - [oobeSystem](#oobeSystem "oobeSystem")
- [Examples](#Examples "Examples")
  - [Windows](#Windows "Windows")
    - [In Action](#In_Action "In Action")
  - [Linux](#Linux "Linux")
    - [In Action](#In_Action-2 "In Action")
- [References](#References "References")

## Traditional Enterprise Template Management

1. Templates Across Multiple Sites – create a master template and replicate to ensure the same state exists
   1. Introduces operational complexity
   2. Extends the total amount of time it takes to patch all templates
2. OS and Application updates need to be performed for every application on every template
   1. Repetition sucks!
   2. Introduces risk due to [C2K errors](https://www.lifewire.com/have-you-been-the-butt-of-a-tech-joke-2619218)
3. Template creation ends up being a work of art.
   1. Individuals sometimes spend years fine-tuning all of the customization in a windows template.
   2. On-boarding time is significantly increased
   3. Projects delivered by third parties will take extra time to complete projects, as reverse engineering will need to occur in templates
4. Documentation? Do you have it for your Windows and Linux Template?

<!--more-->

## Enterprise Template Management With Packer

1. You are no longer limited to VMware! The effort used to create the template code can be used to create templates in other hypervisors, and in the cloud
2. Create net-new templates consistently, eliminating the old method of creating one template, and copying that to data-centers over the world.
3. Packer defines every configured setting and change for templates in code. Documentation: Check!
4. Changes to your templates make it into the wild faster and with zero configuration drift.

## Source Code

You can find source code for Windows 2019, Windows 2016, and Ubuntu 18 in my GitHub repository: <https://github.com/jonhowe/Virtjunkie.com/tree/master/Packer>

The remainder of this post will explain how this code works.

## Packer Intro

First and foremost, this is not a packer tutorial. Packer actually [provides an excellent getting started guide](https://packer.io/intro/getting-started/install.html). I’d actually recommend you start there if you have no background with packer. That said, I will blaze through a few concepts.

## Packer Template File & User Variables

Packer stores it’s configuration in JSON files and calls them Packer Templates. There are two types of files. Master packer templates, and user variable files. Both are stored in JSON. The easiest way to think of this is the master packer template file contains properties that will be used as a part of the build. The user variable file (that is specified when you actually execute the build.. more on this later) in JSON format provides the values to the properties.

### Builders

Hashicorp defines builders as:

> *Builders are responsible for creating machines and generating images from them for various platforms. For example, there are separate builders for EC2, VMware, VirtualBox, etc. Packer comes with many builders by default, and can also be extended to add new builders.*

We will be using the builder called [VSphere-ISO](https://packer.io/docs/builders/vsphere-iso.html). This builder communicates directly with the vCenter API, which also makes this relevant for [VMC on AWS](https://cloud.vmware.com/vmc-aws).

### Attaching ISOs and Floppy Images

Packer allows us to attach both [ISOs](https://packer.io/docs/builders/vsphere-iso.html#iso_paths) and [Floppy images](https://packer.io/docs/builders/vsphere-iso.html#floppy-configuration) to the VM we are working with.

#### ISOs

You can attach multiple ISOs to an image. For example, you can attach a Windows installer ISO, as well as a VMware tools ISO to a Windows VM. Here’s an example of how this works:

```text
"iso_paths": [
    "[esxi1-nvme] ISO/Windows/14393.0.161119-1705.RS1_REFRESH_SERVER_EVAL_X64FRE_EN-US.ISO",
    "[esxi1-nvme] ISO/VMTools/VMware-tools-windows-11.0.1-14773994.iso"
]
```

#### Floppy Images

Packer gives us the ability to take a file, a directory, or a floppy image, and present it to the target VM as a floppy image. This is very useful if you want to copy scripts to the VM to be executed locally. Here’s an example of how this works:

```text
"floppy_files": [
    "./autounattend.xml",
    "Scripts/vmtools.cmd",
    "Scripts/level0-setup.ps1"
]
```

### Communicators

[Communicators](https://packer.io/docs/communicators/index.html) are the mechanism Packer uses to upload files, execute scripts, after the machine is created. Packer uses WinRM and SSH communicators. More on this later.

### Provisioners

Provisioners are used to handle post image creation tasks, such as OS Customization and installing updates. Provisioners require communicators. In this case, the WinRM communicator will be used with Windows Images, while the SSH communicator will be used to communicate with Linux. We will be using the following provisioners:

| Provisioner Name | Used For |
| --- | --- |
| [Powershell](https://packer.io/docs/provisioners/powershell.html) | Performing all OS Customization Steps in Windows Images |
| [Windows-Restart](https://packer.io/docs/provisioners/windows-restart.html) | Restart Windows Images |
| [Windows-Update](https://github.com/rgl/packer-provisioner-windows-update) | Apply Windows updates (community supported) |
| [Shell](https://packer.io/docs/provisioners/shell.html) | Used to install updates on Linux machines. We also set a custom “execution\_command” that will allow for sudo to be used for all commands. |

## Linux Templates

Linux templates are pretty straight forward. Being born in open source, they are much easier to automate than Windows. Debian based distributions use a preseed file to silently execute the build. We will use packer to do the following:

1. Create a blank VM
2. Attach Linux installer ISO
3. Create and attach media that has preseed.cfg file to the newly created image
4. Start VM
5. Send commands to the running VM via USB emulation to tell the Ubuntu installer to use the preseed.cfg file
6. Update all packages on the template
7. Shut Down VM
8. Mark as Template

Here’s the directory structure:

```text
Ubuntu18/
 ├── preseed.cfg
 ├── ubuntu-18.04.json
 └── ubuntu-vars.json
 0 directories, 3 files
```

## Windows Templates

Most consumers of Packer are using it to manage Linux images, but I rarely hear about managing Windows images. Windows has a bit more moving parts that cause more complexity. It was way harder for me to figure out, even with a couple of great posts I’ll list in the reference area. In order to have a complete windows template, we will need to achieve the following steps:

1. Create a blank VM
2. Attach Windows Installer and VMware Tools ISO
3. Attach floppy image that contains scripts and autounattend.xml
4. Start VM
5. Silently Install Windows Server (windowsPE pass in Autounattend.xml)
6. Install VMware Tools (Specialize pass in Autounattend.xml executes vmtools.cmd)
7. Configure WinRM (oobeSystem pass in Autounattend.xml executes level0-setup.ps1)
8. Perform OS Customization (Packer PowerShell provisioner executes level1-setup.ps1)
9. Install Windows Updates (Packer Windows Update provisioner applies updates)
10. Shut Down VM
11. Mark as Template

Definitely more complex than Linux, eh? Don’t worry though. I’ll do my best to add some value on top of documentation and blog articles that are out there. Here’s the directory structure:

```text
WS19
 ├── autounattend.xml
 ├── Scripts
 │&nbsp;&nbsp; ├── level0-setup.ps1
 │&nbsp;&nbsp; ├── level1-setup.ps1
 │&nbsp;&nbsp; └── vmtools.cmd
 ├── vars-ws19.json
 └── ws19.json
 1 directory, 6 files
```

### Autounattend.xml

Microsoft allows us to provide an answer file to the Windows installer to achieve a silent install of Windows Server. The installer will look in all attached media to find a file named Autounattend.xml. This file contains a number of settings that are explained in a decent amount of detail on this [Microsoft documentation page](https://docs.microsoft.com/en-us/windows-hardware/manufacture/desktop/how-configuration-passes-work). Below is a high level overview of the passes and how we are using them.  
  
I found [this page helpful](https://www.windowsafg.com/server2016.html) in creating the skeleton of the XML file.

![](/wp-content/uploads/2020/03/dep-win8-l-configpassesandexes.jpg)

#### **windowsPE**

- Select disk format
- Select the OS Image (Core, GUI, Datacenter, Standard)
- Add the product key (we’ll be using the 6 month trial)
- Select Locale, Name, Organization

#### offlineServicing

- This configuration pass is used to apply updates, drivers, or language packs to a Windows image.

#### generalize

- We are setting the [property SkipRearm](https://docs.microsoft.com/en-us/windows-hardware/customize/desktop/unattend/microsoft-windows-security-spp-skiprearm)
- Resets the SID

#### specialize

- This configuration pass is used to create and configure information in the Windows image, and is specific to the hardware that the Windows image is installing to.
- Install VMware Tools by executing (vmtools.cmd) in this step to ensure it’s available ASAP for Packer to perform the rest of template configuration steps
- Computer name is set
- Reboots the machine

#### oobeSystem

- Add user, set password
- Execute powershell script (level0-setup.ps1) to enable WinRM, which is required for Packer provisioning

## Examples

Here are a few examples of how the script works

### Windows

The command below will create a windows template with the following details.

|  |  |
| --- | --- |
| Username | Administrator |
| Password | VMware1! |
| Additional User | Labadmin |

If you want to change the password, you will need to specify it both in the vars file, as well as the autounattend.xml. The section you will change looks like this:

```text
 &lt;UserAccounts>
    &lt;AdministratorPassword>
        &lt;Value>VMware1!&lt;/Value>
        &lt;PlainText>true&lt;/PlainText>
    &lt;/AdministratorPassword>
    &lt;LocalAccounts>
        &lt;LocalAccount wcm:action="add">
            &lt;Description>Lab Administrator&lt;/Description>
            &lt;DisplayName>labadmin&lt;/DisplayName>
            &lt;Group>Administrators&lt;/Group>
            &lt;Name>labadmin&lt;/Name>
        &lt;/LocalAccount>
    &lt;/LocalAccounts>
&lt;/UserAccounts>
&lt;AutoLogon>
    &lt;Password>
        &lt;Value>VMware1!&lt;/Value>
        &lt;PlainText>true&lt;/PlainText>
    &lt;/Password>
    &lt;Enabled>true&lt;/Enabled>
    &lt;Username>Administrator&lt;/Username>
&lt;/AutoLogon>
```

#### In Action

```text
packer build -var-file vars-ws19.json ws19.json
vsphere-iso: output will be in this color.

==> vsphere-iso: Creating VM...
==> vsphere-iso: Customizing hardware...
==> vsphere-iso: Mounting ISO images...
==> vsphere-iso: Creating floppy disk...
    vsphere-iso: Copying files flatly from floppy_files
    vsphere-iso: Copying file: ./autounattend.xml
    vsphere-iso: Copying file: Scripts/vmtools.cmd
    vsphere-iso: Copying file: Scripts/level0-setup.ps1
    vsphere-iso: Done copying files from floppy_files
    vsphere-iso: Collecting paths from floppy_dirs
    vsphere-iso: Resulting paths from floppy_dirs : []
    vsphere-iso: Done copying paths from floppy_dirs
==> vsphere-iso: Uploading created floppy image
==> vsphere-iso: Adding generated Floppy...
==> vsphere-iso: Set boot order...
==> vsphere-iso: Power on VM...
==> vsphere-iso: Waiting for IP...
==> vsphere-iso: IP address: 172.16.1.73
==> vsphere-iso: Using winrm communicator to connect: 172.16.1.73
==> vsphere-iso: Waiting for WinRM to become available...
    vsphere-iso: WinRM connected.
==> vsphere-iso: #&lt; CLIXML
==> vsphere-iso: &lt;Objs Version="1.1.0.1" xmlns="http://schemas.microsoft.com/powershell/2004/04">&lt;Obj S="progress" RefId="0">&lt;TN RefId="0">&lt;T>System.Management.Automation.PSCustomObject&lt;/T>&lt;T>System.Object&lt;/T>&lt;/TN>&lt;MS>&lt;I64 N="SourceId">1&lt;/I64>&lt;PR N="Record">&lt;AV>Preparing modules for first use.&lt;/AV>&lt;AI>0&lt;/AI>&lt;Nil />&lt;PI>-1&lt;/PI>&lt;PC>-1&lt;/PC>&lt;T>Completed&lt;/T>&lt;SR>-1&lt;/SR>&lt;SD> &lt;/SD>&lt;/PR>&lt;/MS>&lt;/Obj>&lt;Obj S="progress" RefId="1">&lt;TNRef RefId="0" />&lt;MS>&lt;I64 N="SourceId">1&lt;/I64>&lt;PR N="Record">&lt;AV>Preparing modules for first use.&lt;/AV>&lt;AI>0&lt;/AI>&lt;Nil />&lt;PI>-1&lt;/PI>&lt;PC>-1&lt;/PC>&lt;T>Completed&lt;/T>&lt;SR>-1&lt;/SR>&lt;SD> &lt;/SD>&lt;/PR>&lt;/MS>&lt;/Obj>&lt;/Objs>
==> vsphere-iso: Connected to WinRM!
==> vsphere-iso: Provisioning with Powershell...
==> vsphere-iso: Provisioning with powershell script: Scripts/level1-setup.ps1
    vsphere-iso:
    vsphere-iso:
    vsphere-iso:     Directory: C:\Users\Administrator\Documents\WindowsPowerShell
    vsphere-iso:
    vsphere-iso:
    vsphere-iso: Mode                LastWriteTime         Length Name
    vsphere-iso: ----                -------------         ------ ----
    vsphere-iso: -a----        3/22/2020   3:02 PM              0 Microsoft.PowerShell_profile.ps1
==> vsphere-iso: Restarting Machine
==> vsphere-iso: Waiting for machine to restart...
==> vsphere-iso: A system shutdown is in progress.(1115)
==> vsphere-iso: #&lt; CLIXML
    vsphere-iso: WS19-TPL restarted.
==> vsphere-iso: &lt;Objs Version="1.1.0.1" xmlns="http://schemas.microsoft.com/powershell/2004/04">&lt;Obj S="progress" RefId="0">&lt;TN RefId="0">&lt;T>System.Management.Automation.PSCustomObject&lt;/T>&lt;T>System.Object&lt;/T>&lt;/TN>&lt;MS>&lt;I64 N="SourceId">1&lt;/I64>&lt;PR N="Record">&lt;AV>Preparing modules for first use.&lt;/AV>&lt;AI>0&lt;/AI>&lt;Nil />&lt;PI>-1&lt;/PI>&lt;PC>-1&lt;/PC>&lt;T>Completed&lt;/T>&lt;SR>-1&lt;/SR>&lt;SD> &lt;/SD>&lt;/PR>&lt;/MS>&lt;/Obj>&lt;Obj S="progress" RefId="1">&lt;TNRef RefId="0" />&lt;MS>&lt;I64 N="SourceId">2&lt;/I64>&lt;PR N="Record">&lt;AV>Preparing modules for first use.&lt;/AV>&lt;AI>0&lt;/AI>&lt;Nil />&lt;PI>-1&lt;/PI>&lt;PC>-1&lt;/PC>&lt;T>Completed&lt;/T>&lt;SR>-1&lt;/SR>&lt;SD> &lt;/SD>&lt;/PR>&lt;/MS>&lt;/Obj>&lt;/Objs>
==> vsphere-iso: Machine successfully restarted, moving on
==> vsphere-iso: Uploading the Windows update elevated script...
==> vsphere-iso: Uploading the Windows update check for reboot required elevated script...
==> vsphere-iso: Uploading the Windows update script...
==> vsphere-iso: Running Windows update...
    vsphere-iso: Searching for Windows updates...
    vsphere-iso: Found Windows update (2018-10-15; 20.72 MB): Update for Adobe Flash Player for Windows Server 2019 (1809) for x64-based Systems (KB4462930)
    vsphere-iso: Found Windows update (2020-02-11; 20.75 MB): 2020-02 Security Update for Adobe Flash Player for Windows Server 2019 for x64-based Systems (KB4537759)
    vsphere-iso: Found Windows update (2020-02-25; 71.37 MB): 2020-02 Cumulative Update for .NET Framework 3.5, 4.7.2 and 4.8 for Windows Server 2019 for x64 (KB4538156)
    vsphere-iso: Found Windows update (2020-02-25; 2.34 MB): 2020-01 Update for Windows Server 2019 for x64-based Systems (KB4494174)
    vsphere-iso: Found Windows update (2020-03-10; 30.62 MB): Windows Malicious Software Removal Tool x64 - March 2020 (KB890830)
    vsphere-iso: Found Windows update (2020-03-22; 114.85 MB): Security Intelligence Update for Windows Defender Antivirus - KB2267602 (Version 1.311.1752.0)
    vsphere-iso: Found Windows update (2020-03-10; 15349.68 MB): 2020-03 Cumulative Update for Windows Server 2019 (1809) for x64-based Systems (KB4538461)
    vsphere-iso: Downloading Windows updates (7 updates; 15610.33 MB)...
    vsphere-iso: Waiting for operation to complete (system performance: 44% cpu; 31% memory)...
    vsphere-iso: Installing Windows updates...
    vsphere-iso: Waiting for operation to complete (system performance: 20% cpu; 41% memory)...
    vsphere-iso: Waiting for operation to complete (system performance: 51% cpu; 51% memory)...
    vsphere-iso: Waiting for operation to complete (system performance: 51% cpu; 50% memory)...
    vsphere-iso: Waiting for operation to complete (system performance: 50% cpu; 54% memory)...
    vsphere-iso: Waiting for operation to complete (system performance: 43% cpu; 55% memory)...
    vsphere-iso: Waiting for operation to complete (system performance: 0% cpu; 61% memory)...
    vsphere-iso: Waiting for operation to complete (system performance: 38% cpu; 52% memory)...
    vsphere-iso: Waiting for operation to complete (system performance: 63% cpu; 48% memory)...
    vsphere-iso: Waiting for operation to complete (system performance: 27% cpu; 46% memory)...
    vsphere-iso: Waiting for operation to complete (system performance: 45% cpu; 47% memory)...
    vsphere-iso: Waiting for operation to complete (system performance: 55% cpu; 46% memory)...
    vsphere-iso: Waiting for operation to complete (system performance: 53% cpu; 44% memory)...
    vsphere-iso: Waiting for the Windows Modules Installer to exit...
    vsphere-iso: Waiting for operation to complete (system performance: 81% cpu; 44% memory)...
==> vsphere-iso: Restarting the machine...
==> vsphere-iso: Waiting for machine to become available...
==> vsphere-iso: A system shutdown is in progress.(1115)
==> vsphere-iso: A system shutdown is in progress.(1115)
    vsphere-iso: Waiting for the Windows Modules Installer to exit...
    vsphere-iso: WS19-TPL restarted.
==> vsphere-iso: Running Windows update...
    vsphere-iso: Searching for Windows updates...
    vsphere-iso: Found Windows update (2020-03-19; 4.91 MB): Update for Windows Defender Antivirus antimalware platform - KB4052623 (Version 4.18.2003.6)
    vsphere-iso: Downloading Windows updates (1 updates; 4.91 MB)...
    vsphere-iso: Installing Windows updates...
==> vsphere-iso: Shut down VM...
==> vsphere-iso: Deleting Floppy drives...
==> vsphere-iso: Deleting Floppy image...
==> vsphere-iso: Eject CD-ROM drives...
==> vsphere-iso: Convert VM into template...
Build 'vsphere-iso' finished.

==> Builds finished. The artifacts of successful builds are:
--> vsphere-iso: WS19-TPL
```

### Linux

The command below will create a Ubuntu template with the following details:

|  |  |
| --- | --- |
| Root Password | VMware1! |
| Additional Username (also added to sudoers) | jhowe |
| Additional username’s password | VMware1! |

All of the above can be changed by modifying values in the preseed.cfg file.

#### In Action

```text
packer build -var-file ubuntu-vars.json ubuntu-18.04.json

jhowe@jonlaptopalt:~/git/Personal/HomeLab/packer/Ubuntu18$ packer build -var-file ubuntu-vars.json ubuntu-18.04.json 
vsphere-iso: output will be in this color.

==> vsphere-iso: Creating VM...
==> vsphere-iso: Customizing hardware...
==> vsphere-iso: Mounting ISO images...
==> vsphere-iso: Creating floppy disk...
    vsphere-iso: Copying files flatly from floppy_files
    vsphere-iso: Copying file: ./preseed.cfg
    vsphere-iso: Done copying files from floppy_files
    vsphere-iso: Collecting paths from floppy_dirs
    vsphere-iso: Resulting paths from floppy_dirs : []
    vsphere-iso: Done copying paths from floppy_dirs
==> vsphere-iso: Uploading created floppy image
==> vsphere-iso: Adding generated Floppy...
==> vsphere-iso: Set boot order...
==> vsphere-iso: Power on VM...
==> vsphere-iso: Waiting 10s for boot...
==> vsphere-iso: Typing boot command...
==> vsphere-iso: Waiting for IP...
==> vsphere-iso: IP address: 172.16.1.72
==> vsphere-iso: Using ssh communicator to connect: 172.16.1.72
==> vsphere-iso: Waiting for SSH to become available...
==> vsphere-iso: Connected to SSH!
==> vsphere-iso: Provisioning with shell script: /tmp/packer-shell338854810
    vsphere-iso: Hit:1 http://security.ubuntu.com/ubuntu bionic-security InRelease
    vsphere-iso: Hit:2 http://us.archive.ubuntu.com/ubuntu bionic InRelease
    vsphere-iso: Hit:3 http://us.archive.ubuntu.com/ubuntu bionic-updates InRelease
    vsphere-iso: Hit:4 http://us.archive.ubuntu.com/ubuntu bionic-backports InRelease
    vsphere-iso: Reading package lists...
    vsphere-iso: Reading package lists...
    vsphere-iso: Building dependency tree...
    vsphere-iso: Reading state information...
    vsphere-iso: Calculating upgrade...
    vsphere-iso: The following packages have been kept back:
    vsphere-iso:   linux-generic linux-headers-generic linux-image-generic
    vsphere-iso: The following packages will be upgraded:
    vsphere-iso:   dmidecode gcc-8-base libdrm-common libdrm2 libgcc1 libicu60 libnss-systemd
    vsphere-iso:   libpam-systemd libsqlite3-0 libstdc++6 libsystemd0 libudev1 libxml2
    vsphere-iso:   linux-firmware rsync systemd systemd-sysv udev
    vsphere-iso: 18 upgraded, 0 newly installed, 0 to remove and 3 not upgraded.
    vsphere-iso: Need to get 89.7 MB of archives.
    vsphere-iso: After this operation, 572 kB of additional disk space will be used.
    vsphere-iso: Get:1 http://us.archive.ubuntu.com/ubuntu bionic-updates/main amd64 perl-modules-5.26 all 5.26.1-6ubuntu0.3 [2,763 kB]

[Omitted some output in order to save space. Apt is downloading new packages]

[Omitted some output in order to save space. Apt is unpacking packages]

[Omitted some output in order to save space. Apt is "Setting up... all upgraded packages]

    vsphere-iso: Processing triggers for systemd (237-3ubuntu10.39) ...
    vsphere-iso: Processing triggers for man-db (2.8.3-2ubuntu0.1) ...
    vsphere-iso: Processing triggers for dbus (1.12.2-1ubuntu1.1) ...
    vsphere-iso: Processing triggers for mime-support (3.60ubuntu1) ...
    vsphere-iso: Processing triggers for ureadahead (0.100.0-21) ...
    vsphere-iso: Processing triggers for install-info (6.5.0.dfsg.1-2) ...
    vsphere-iso: Processing triggers for libc-bin (2.27-3ubuntu1) ...
    vsphere-iso: Template Build Complete
==> vsphere-iso: Shut down VM...
==> vsphere-iso: Deleting Floppy drives...
==> vsphere-iso: Deleting Floppy image...
==> vsphere-iso: Eject CD-ROM drives...
==> vsphere-iso: Convert VM into template...
Build 'vsphere-iso' finished.

==> Builds finished. The artifacts of successful builds are:
--> vsphere-iso: Ubuntu18
```

## References

I did a lot of research as when getting this up and running. The following sites were helpful.

- This is an EXCELLENT blog. The article he created unfortunately didn’t work, but it got me started. Either way, it’s worth a look. (<https://dteslya.engineer/automation/2018-12-20-creating_vm_templates_with_packer/>)
- Official Packer Documentation (<https://packer.io/docs/index.html>)
