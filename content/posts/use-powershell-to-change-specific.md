---
title: "Use PowerShell to Update Specific AD User’s Description Field with Last Login Time"
date: 2013-04-19T12:00:31-04:00
slug: "use-powershell-to-change-specific"
url: /2013/04/19/use-powershell-to-change-specific/
author:
  - "jhowe"
year: ["2013"]
month: ["2013-04"]
categories:
  - "featured"
  - "powershell"
  - "scripting"
  - "automation"
  - "servers"
  - "win"
tags: []
aliases:
  - "/2013/04/19/use-powershell-to-change-specific/feed/"
---

I encountered a challenge today that was fun to fix.  There’s an Organizational Unit in my AD setup that has historically been used to store disabled AD objects instead of deleting them.

When an employee leaves the organization, our standard procedure  is as followed:

1. Disable User Object
2. Move to separate OU (IE AD://internal.msd/disabled/users)
3. Update Description field with something like: Disabled by [username] on [date]
4. Retain user object for x amount of days, then tombstone it.

Best laid plans of mice and men… yada yada…

<!--more-->

I was able to go through all of these user objects that didn’t get their description updated with the one liner below. I’ll explain this beginning with script line 3 below:

- (Line 3) Find all users in the OU: ‘OU=Users,OU=Disabled,DC=internal,DC=msd’ – customize this to your environment
- (Line 4) Exclude objects where the description does not contain the word “disabled”.
- (Lines 5-7) Loop through each object that remains and update the description with the same object’s last login date.

FYI – this script requires the Quest ActiveRoles Powershell Toolkit (<http://www.quest.com/powershell/activeroles-server.aspx>)

```powershell
#This script requires Quest AD Tools
add-pssnapin Quest.ActiveRoles.ADManagement

#Everything below this is on one line
get-QADUser -searchroot 'OU=Users,OU=Disabled,DC=internal,DC=msd'
| Where-Object { $_.Description -notlike &quot;*disabled*&quot; }
| ForEach-Object { set-qaduser -identity
(get-qaduser $_.samaccountname) -description
(&quot;Last Login: &quot; + (get-qaduser $_.samaccountname).lastlogon})
```

I’m sure there’s a more elegant way to handle this, but in 30 minutes I created this one liner, and updated *a lot* of user objects.

Cheers!
