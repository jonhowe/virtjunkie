---
title: "Update: Exchange 2010 – Bulk Mailbox Migration In Batches (The Right Way)"
date: 2013-09-04T00:50:49-04:00
slug: "update-exchange-2010-bulk-mailbox-migration-in-batches-the-right-way"
url: /2013/09/04/update-exchange-2010-bulk-mailbox-migration-in-batches-the-right-way/
author:
  - "jhowe"
year: ["2013"]
month: ["2013-09"]
categories:
  - "uncategorized"
tags: []
aliases:
  - "/2013/09/04/update-exchange-2010-bulk-mailbox-migration-in-batches-the-right-way/feed/"
---

In June I added a [post on how to](/2013/06/27/exchange-2010-bulk-mailbox-migration-in-batches/ "Exchange 2010 – Bulk Mailbox Migration In Batches") migrate exchange 2010 mailboxes to an Exchange 2010 DAG in a controlled fashion. Since then I’ve completely restructured the script and made it an all-in-one solution.

<!--more-->

The first section of the script contains variables that need to be set.

```powershell
#region ========================================================================
# Created on:	9/3/2013 8:01 PM
# Created by:	Jon Howe
# URL: /2013/09/04/update-exchange-2010-bulk-mailbox-migration-in-batches-the-right-way/
# Filename:		Set-MailboxMoveActive-v2.ps1
#endregion ========================================================================

#region Set Variables
#Amount of mailboxes to migrate at a time
$BatchSize = 5
#Mailbox DB to pull mailboxes from
$sourceMailboxDatabase = "Mailbox Database 3"
#Default amount of time to sleep when we hit a roadblock
$sleepMinutes = 20
#Time to start migrating mailboxes
$startTime = Get-Date -Hour 23 -Minute 00 -Second 00
#Time to stop migrating mailboxes
$stopTime = Get-Date -Hour 05 -Minute 00 -Second 00
#Array containing all of your DAG servers (used to check disk space)
$DAG_Servers = @("EXCH-DAG-A","EXCH-DAG-B")
#OS label for the DAG DAGA/Log drives on your DAG servers.
$OS_Label_Prefix = "DAGDB*"
#Threshold for stopping the migration (in bytes)
$MinOSDriveFreeBytes = 16106127360 #32212254720 is 30GB, 16106127360 is 15GB
#endregion Set Variables

$PS_Is_Awesome = $TRUE #!!!
While ($PS_IS_Awesome) #region Main Loop
{
#region Check for Business Hours
if ( (Get-Date) -gt $stopTime -and (Get-Date) -lt $startTime ) #region In Business Hours
{
	Write-Host "We're in business hours. Sleeping..." -ForegroundColor 'DarkCyan'
	Start-Sleep -Seconds ($sleepMinutes * 60)
} #endregion In Business Hours
else #region Out of Business Hours
{
	#region Check to make sure drive space isn't too low
	foreach($mbx in $DAG_Servers)
	{
		$space = `
		get-WmiObject win32_volume -ComputerName $mbx |
		select driveletter,label,freespace,capacity |
		where {$_.label -like $OS_Label_Prefix}

		foreach($drive in $space)
		{
			$human_freespace = [math]::Round($drive.freespace / (1024*1024*1024),1)

			if ($drive.freespace -lt $MinOSDriveFreeBytes)
			{
				Write-Host "Drive" $drive.driveletter "on server $mbx with label" $drive.label "is under 30 GB. It's currently at" $human_freespace "GB..."
				write-host "Sleeping for $sleepMinutes minutes." -ForegroundColor 'DarkCyan'
				for ($i = 1; $i -le ($sleepMinutes * 60); $i++)
				{
					Write-Progress -Activity 'Drive Space is too low. Waiting until it frees up.' -Status "We've waited $i Seconds" -SecondsRemaining (($sleepMinutes * 60)-$i)
					sleep -Seconds 1
				}
			}
		}
	}
	#endregion Check to make sure drive space isn't too low

	#region Check to see if a move-request is currently occurring
	if (Get-MoveRequest | Where-Object { $_.Status -eq "Queued" -or $_.Status -eq "InProgress" -or $_.Status -eq "CompletionInProgress"})
	{
		Write-Host "There are move requests currently processing.  Sleeping for $sleepMinutes minutes" -ForegroundColor 'DarkCyan'

		for ($i = 1; $i -le ($sleepMinutes * 60); $i++)
		{
			Write-Progress -Activity "Can't begin if move requests are already running. Waiting for them to complete" -Status "We've waited $i Seconds" -SecondsRemaining (($sleepMinutes * 60)-$i)
			sleep -Seconds 1
		}
		continue
	}
	#endregion Check to see if a move-request is currently occurring

	#region General information display and information gathering.
	Write-Host "We're out of business hours, drive space looks good, and there are no batches running" -ForegroundColor 'Yellow'
	write-host "Let's submit one!" -ForegroundColor 'Yellow'

	# Get Mailbox Sizes
	Write-Host "Getting Mailbox Sizes" -ForegroundColor 'Blue'
	$allmbx = Get-Mailbox -database $sourceMailboxDatabase |
   		Get-MailboxStatistics |
   		Sort-Object TotalItemSize |
   		Select-Object DisplayName,TotalItemSize

	#endregion General information display and information gathering.

	# Submit move requests to best datatabase
	Write-Host "Submitting move requests now" -ForegroundColor 'Blue'

	$batch = 1
	for ($i=1;$i -le 5;$i++) #region For Loop
	{
		#region Determine the best database to send mailboxes to
		if ($i % $BatchSize -eq 0)
    	{
			# Find best Database
			$result = Get-MailboxDatabase -identity "DAG*" -Status |
 				Select-Object name,DatabaseSize,AvailableNewMailboxSpace |
        		Sort-Object -Property DatabaseSize

			$bestDatabase = $result[0].name

			$batch++
		}
		#endregion Determine the best database to send mailboxes to

	#Submit the mailbox move requests
	Write-Host "New Move -" $allmbx[$i].DisplayName "to DB" $bestDatabase  -ForegroundColor 'DarkGreen'
	New-MoveRequest -TargetDatabase $bestDatabase -Identity $allmbx[$i].DisplayName | out-null

	} #endregion For Loop

	Write-Host "Batches submitted. Sleeping for $sleepMinutes minutes" -ForegroundColor 'DarkCyan'
	for ($i = 1; $i -le ($sleepMinutes * 60); $i++)
	{
		Write-Progress -Activity 'Waiting while move requests complete' -Status "We've waited $i Seconds" -SecondsRemaining (($sleepMinutes * 60)-$i)
		sleep -Seconds 1
	}

} #endregion Out of Business Hours
#endregion Check for Business Hours
} #endregion Main Loop
```
