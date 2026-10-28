---
title: "VMware 5.1 – Virtual Machine Disks Consolidation Is Needed"
date: 2013-02-11T12:44:14-05:00
slug: "vmware-5-1-virtual-machine-disks-consolidation-is-needed"
url: /2013/02/11/vmware-5-1-virtual-machine-disks-consolidation-is-needed/
author:
  - "jhowe"
year: ["2013"]
month: ["2013-02"]
categories:
  - "servers"
  - "vmware"
tags: []
aliases:
  - "/2013/02/11/vmware-5-1-virtual-machine-disks-consolidation-is-needed/feed/"
---

I received the following message today on one of my production VM’s.

[![Virtual Machine Consolidation Needed](/wp-content/uploads/2013/02/vmconsolidationneeded.png)](/wp-content/uploads/2013/02/vmconsolidationneeded.png)

You can use these steps to resolve this issue.

<!--more-->

In order to resolve this, you need to use the “consolidate” option within the VM menu.

[![consolidate1](/wp-content/uploads/2013/02/consolidate1.png)](/wp-content/uploads/2013/02/consolidate1.png)

According to [VMware KB 2003638](http://kb.vmware.com/kb/2003638),

Consolidating snapshots may be required when:

- The snapshot commit fails due to locked files. For details on how to release the lock on locked files, see [Investigating virtual machine file locks on ESXi/ESX (10051)](http://kb.vmware.com/selfservice/microsites/search.do?cmd=displayKC&docType=kc&docTypeID=DT_KB_1_1&externalId=10051).
- There is a temporary loss of communication between the vCenter Server and the ESXi/ESX host during snapshot commit. To refresh the connectivity, restart the ESXi/ESX host management agents. For more information, see [Restarting the Management agents on an ESXi or ESX host (1003490)](http://kb.vmware.com/selfservice/microsites/search.do?cmd=displayKC&docType=kc&docTypeID=DT_KB_1_1&externalId=1003490).
