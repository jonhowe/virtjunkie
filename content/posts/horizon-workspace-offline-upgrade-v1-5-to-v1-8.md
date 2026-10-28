---
title: "Horizon Workspace – Offline Upgrade – v1.5 to v1.8"
date: 2014-04-12T22:49:46-04:00
slug: "horizon-workspace-offline-upgrade-v1-5-to-v1-8"
url: /2014/04/12/horizon-workspace-offline-upgrade-v1-5-to-v1-8/
author:
  - "jhowe"
year: ["2014"]
month: ["2014-04"]
categories:
  - "horizon-workspace"
  - "vmware"
tags: []
aliases:
  - "/2014/04/12/horizon-workspace-offline-upgrade-v1-5-to-v1-8/feed/"
---

![horizon-3](https://new.virtjunkie.com/wp-content/uploads/2014/04/horizon-3.png)After upgrading several different environments to Horizon Workspace 1.8, it’s become clear to me that the “offline upgrade” feature is something that should be used whenever possible. Maybe it’s just the environments I’ve worked in, but going from 1.5 to 1.8 takes much much longer than going from 1.0-1.5. This guide is intended to help you accomplish an offline upgrade from 1.5 to 1.8, while having a plan to restore to 1.5 in case of a failure. This is the fastest process I have found to perform the upgrade. Even with these measures, I’d plan on getting a 4-5 hour outage window for a production environment (2 connector, service, gateway, data virtual appliances)

<!--more-->

First thing is first – VMware currently only provides the update repo files mentioned in the [documentation center](http://pubs.vmware.com/horizon-workspace-18/topic/com.vmware.hw-upgrade.doc_18/GUID-50372CFD-AD3C-44F0-9F1B-5C5E1E8D98D9.html) if you call and speak to global support services.

1. Call VMware GSS and request update repo files for the offline upgrade from horizon workspace 1.5 to 1.8. Ensure that they provide you with the files “configureupdate.hzn”, and “updatelocal.hzn”.
2. Copy the “updatelocal.hzn” file to the configurator-va directory: /usr/local/horizon/lib/menu/
3. Copy the “configureupdate.hzn” file to every virtual appliance in the directory: /usr/local/horizon/scripts/
4. Set the permissions of each script to 700 (chmod 700 /usr/local/horizon/scripts/configureupdate.hzn)
5. Add the “configureupdate.hzn” script to the sudoers file on each va. A snippet of the end of the sudoers file will look like this:
   1. /usr/local/horizon/scripts/setupSshKeys.hzn, \
   2. /sbin/reboot, \
   3. **/usr/local/horizon/scripts/configureupdate.hzn**
6. Create the following directory structure on a web server that’s accessible by every horizon workspace app. Note, the [published documentation](http://pubs.vmware.com/horizon-workspace-18/topic/com.vmware.hw-upgrade.doc_18/GUID-50372CFD-AD3C-44F0-9F1B-5C5E1E8D98D9.html) says to create the service-va directory “srv”, but the script specifies the directory “svc”.
   1. vapp
      1. conn
      2. cfg
      3. gty
      4. svc
      5. dta
7. Extract each update repo zip file to their respective directories.
8. Run the following snippet on the configurator-va to make sure your setup is good to proceed, and configure each VA to use the local update source. If there are no errors appear, you’re good to keep going.
   1. /usr/local/horizon/lib/menu/updatelocal.hzn checkurl http://yourhost/vapp
   2. /usr/local/horizon/lib/menu/updatelocal.hzn seturl http://yourhost/vapp
9. At this point, you can proceed with your upgrade as normal. Here’s the steps I personally use to prep for the upgrade to ensure that there are no issues.
10. Backup your postgres database – On the command line of your vFabric postres server, run this command:
    1. /opt/vmware/vpostgres/current/bin/pg\_dump -U postgres -W –clean -f ~/Before\_HWS\_1.8.data saas
    2. The default password is H0rizon!
11. Run the script below – requires vmware powercli. Ensure that your postgres server has the default name. If it doesn’t, change the script below.

```powershell
#Connect to virtualcenter
Connect-viserver -Server [your virtualcenter server] -Credential (Get-Credential)

#Shut down horizon workspace and vmware vfabric postgres
Get-vapp -name "Horizon-Workspace" | stop-vapp
get-vm -Name "VMware vFabric Postgres" | shutdown-vmguest

#Create snapshot of all of the VMs in Horizon Workspace and vFabric Postgres
get-vapp -Name Horizon-Workspace | get-vm | New-Snapshot -Name "Pre_1.8" -Description "Taken before 1.8 Upgrade"
get-vm -Name "VMware vFabric Postgres" | New-Snapshot -Name "Pre_1.8" -Description "Taken before 1.8 Upgrade"

#Start horizon workspace and postgres VM
Get-vm -name "VMware vFabric Postgres" | start-vm
Get-vapp -name "Horizon-Workspace" | start-vapp
```
