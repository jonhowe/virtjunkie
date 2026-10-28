---
title: "RSA SecurID Integration With VMware Horizon View Fails During sdconf.rec Upload"
date: 2013-06-28T15:03:23-04:00
slug: "rsa-securid-integration-with-vmware-horizon-view-fails-during-sdconf-rec-upload"
url: /2013/06/28/rsa-securid-integration-with-vmware-horizon-view-fails-during-sdconf-rec-upload/
author:
  - "jhowe"
year: ["2013"]
month: ["2013-06"]
categories:
  - "vmware"
tags: []
aliases:
  - "/2013/06/28/rsa-securid-integration-with-vmware-horizon-view-fails-during-sdconf-rec-upload/feed/"
---

When trying to upload a sdconf.rec file to Horizon View 5.2, you receive the following error:

[text]  
Invalid file size of 2,770 bytes. The RSA Configuration file size must be between 512 and 2,048 bytes.  
[/text]

[![view-rsa-error](/wp-content/uploads/2013/06/view-rsa-error-300x253.png)](/wp-content/uploads/2013/06/view-rsa-error.png)

<!--more-->

Buried deep within RSA documentation, is the acknowledgement that this is a known issue, and that it will be resolved “in a future release of VMware Horizon View”. They do provide a fix, but it didn’t work for me.

The fix is as follows:

1. Log onto the Connection Server OS as an admin. Copy your sdconf.recfile onto the server (e.g. in documents).
2. From a command prompt run “ldp” (Microsoft’s LDAP browser).
3. From Connection > Connectenter server as 127.0.0.1 and port as 389.
4. From Connection > Bindselect the top radio button “Bind as currently logged on user”.
5. From View > Tree for BaseDN, click the down arrow at the end of the field and select dc=vdi,dc=vmware,dc=int.
6. In the left pane, click the +to expand the tree and double click on ou=Properties… then ou=Server… then the Connection Server name. (e.g. CN=<COMPUTERNAME>,OU=Server,OU=Properties,DC=vdi,DC=vmware,DC=int)
7. Right click on the Connection Server entry and select Modify.
8. In Edit Entry, specify an attribute of pae-SecurIDConf. Leave the Operation set to Add, select Insert File and navigate to your sdconf.rec file and select it. Click Enter, then click Run. This will upload your sdconf.rec file into LDAP. This will distribute it to all Connection Servers and will automatically place the sdconf.rec file in the right location for View.

Unfortunately, I received an error when I tried to click run, indicating that there is already a value assigned to that attribute.  There might be a better way to fix this, but I ended up manually clearing the value of the attribute, and then going into LDP again to insert the sdconf.rec file.

I used the following steps within adsiedit to manually clear the value, since I am not very familiar with the LDP tool.

1. Open ADSI Edit (Win+R, adsiedit.msc)
2. Open the Action menu, and select Connect To
3. Use the following details to connect to the VMware Horizon View Local LDAP store
   1. [![adsiedit](/wp-content/uploads/2013/06/adsiedit-300x295.png)](/wp-content/uploads/2013/06/adsiedit.png)
4. Navigate to the following OU with ADSI Edit: (OU=Server,OU=Properties,DC=vdi,DC=vmware,DC=int)
   1. [![adsiedit-1](/wp-content/uploads/2013/06/adsiedit-1-214x300.png)](/wp-content/uploads/2013/06/adsiedit-1.png)
5. Select the Connection Server in question, and select properties
6. Navigate to the attribute pae-SecurIDConf and select Edit
7. Click the clear option, then OK, Apply, OK
8. You should now be able to upload the sdconf.rec using the ldp tool.
