---
title: "Exchange 2010 – Bulk Mailbox Migration In Batches"
date: 2013-06-27T08:04:37-04:00
slug: "exchange-2010-bulk-mailbox-migration-in-batches"
url: /2013/06/27/exchange-2010-bulk-mailbox-migration-in-batches/
author:
  - "jhowe"
year: ["2013"]
month: ["2013-06"]
categories:
  - "automation"
  - "exchange"
  - "powershell"
  - "scripting"
  - "windows-server"
tags: []
aliases:
  - "/2013/06/27/exchange-2010-bulk-mailbox-migration-in-batches/feed/"
---

**Update**:  
**I created a new version of this script [here](http://45.63.13.214/?p=539 "Update: Exchange 2010 – Bulk Mailbox Migration In Batches (The Right Way)")**  
I recently completed a project that involved migrating Exchange 2010 Mailbox role from a standalone server to a Database Availability Group, or DAG. This was a large project that took a lot of time and planning, and had the potential to be very tedious. Fortunately, with a little knowhow, you can automate many of the tedious tasks.

I wanted to be in full control of mailbox migration, so my requirements were fairly strict:

<!--more-->

- Don’t just submit all mailbox move requests en masse
- Submit move requests in “Suspended” status, so that I can ~~manually~~ release them at a later time
- Move smallest mailboxes first, and progress gradually to big mailboxes
- Chose best destination mailbox database
  - I define best as the database with the most free space.
- Only pull mailboxes from one mailbox database at a time

The script below will accomplish these objectives.

Keep in mind, your destination mailbox database is likely named differently than mine – make sure you change it on line number 21.

I’ll post the script I use to release these suspended jobs systematically at a later date.

```powershell
$BatchSize = 5
$sourceMailboxDatabase = "Mailbox Database 1"

Write-Host "Creating Move Requests and Suspending them"

$allmbx = Get-Mailbox -database $sourceMailboxDatabase |
   Get-MailboxStatistics |
   Sort-Object TotalItemSize |
   Select-Object DisplayName,TotalItemSize
   $AllMBXCount = $allmbx.count

Write-Host "There are" $AllMBXCount "mailboxes to be migrated"
Start-Sleep -Seconds 8

$batch = 1
for ($i=1;$i -le $AllMBXCount;$i++)
{
	if ($i % $BatchSize -eq 0)
	{
		#write-host "Batch $batch" -ForegroundColor 'DarkCyan'
		$result = Get-MailboxDatabase -identity "DAG*" -Status |
                Select-Object name,DatabaseSize,AvailableNewMailboxSpace |
                Sort-Object -Property DatabaseSize
		$bestDatabase = $result[0].name
		$batch++
	}

	Write-Host "New Move - Batch:" $batch "-" $bestDatabase "/" $allmbx[$i].DisplayName -ForegroundColor 'DarkGreen'
	New-MoveRequest -TargetDatabase $bestDatabase -Suspend -Identity $allmbx[$i].DisplayName -BatchName "Batch $batch" | out-null

}
```
