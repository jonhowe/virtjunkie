---
title: "Modify DNS Records via Powershell"
date: 2014-05-20T23:28:22-04:00
slug: "modify-dns-records-via-powershell"
url: /2014/05/20/modify-dns-records-via-powershell/
author:
  - "jhowe"
year: ["2014"]
month: ["2014-05"]
categories:
  - "powershell"
  - "scripting"
  - "automation"
  - "windows-server"
tags: []
aliases:
  - "/2014/05/20/modify-dns-records-via-powershell/feed/"
---

Over the past few months [I’ve been doing](http://blogs.vmware.com/euc/2014/04/vmware-horizon-6-unveiled-today.html) [a lot of work](http://searchvirtualdesktop.techtarget.com/news/2240219383/VMwares-Horizon-6-faces-uphill-battle-against-Citrix-XenApp) with VMware Horizon 6. I’m not going to go into details, as [VMware has done a great job doing that](http://www.vmware.com/horizon-event), plus I’m under a NDA. Suffice to say, details that have been provided suffice if you’re just looking for info.

In my company sponsored lab environment, I have [HWS 1.8](http://www.vmware.com/products/horizon-workspace) deployed in feature/option parity compared to production. Deploying a second instance of HWS (perhaps a pre-release version), is challenging, due to DNS/Reverse DNS Checks that are done.

Anyways – the reason you’re probably here is to find out how to systematically modify DNS records, so here ya go!

<!--more-->

To create the A Record Test-A-Record with IP 192.168.100.100 to DNS Server corp-dns-1 in zone corp.internal, use the following command:

```powershell
Add-DnsServerResourceRecordA -Name Test-A-Record -IPv4Address 192.168.100.100 -ZoneName corp.internal -ComputerName corp-dns-1
```

To remove the same record, run the following command:

```powershell
Remove-DnsServerResourceRecord -ZoneName corp.internal -ComputerName corp-dns-1 -Name Test-A-Record -RRType "A"
```

So, in order to switch between environments, you can use the following snippets:

Switch From Original state to Alternate Environment:

```powershell
Add-DnsServerResourceRecordA -ZoneName corp.internal -ComputerName corp-dns-1 -Name configurator-va -IPv4Address [configurator-ip-address]
Add-DnsServerResourceRecordA -ZoneName corp.internal -ComputerName corp-dns-1 -Name service-va -IPv4Address [service-ip-address]
Add-DnsServerResourceRecordA -ZoneName corp.internal -ComputerName corp-dns-1 -Name connector-va -IPv4Address [connector-ip-address]
Add-DnsServerResourceRecordA -ZoneName corp.internal -ComputerName corp-dns-1 -Name gateway-va -IPv4Address [gateway-ip-address]
```

Revert Back to original state:

```powershell
Remove-DnsServerResourceRecord -ZoneName corp.internal -ComputerName corp-dns-1 -RRType "A" -Name configurator-va
Remove-DnsServerResourceRecord -ZoneName corp.internal -ComputerName corp-dns-1 -RRType "A" -Name service-va
Remove-DnsServerResourceRecord -ZoneName corp.internal -ComputerName corp-dns-1 -RRType "A" -Name connector-va
Remove-DnsServerResourceRecord -ZoneName corp.internal -ComputerName corp-dns-1 -RRType "A" -Name gateway-va

Add-DnsServerResourceRecordA -ZoneName corp.internal -ComputerName corp-dns-1 -Name configurator-va -IPv4Address 10.69.0.110
Add-DnsServerResourceRecordA -ZoneName corp.internal -ComputerName corp-dns-1 -Name service-va -IPv4Address 10.69.0.111
Add-DnsServerResourceRecordA -ZoneName corp.internal -ComputerName corp-dns-1 -Name connector-va -IPv4Address 10.69.0.113
Add-DnsServerResourceRecordA -ZoneName corp.internal -ComputerName corp-dns-1 -Name gateway-va -IPv4Address 10.69.0.117
```

Hope this helps!

Source: [MS Technet](http://technet.microsoft.com/en-us/library/jj649850.aspx)
