---
title: "Howto: Set Up Your Own Snort Intrusion Detection System with a Database Backend"
date: 2006-03-29T11:04:10-05:00
slug: "howto_set_up_your_own_snort_intrusion_detection_system_with_a_database_backend"
url: /2006/03/29/howto_set_up_your_own_snort_intrusion_detection_system_with_a_database_backend/
author:
  - "jhowe"
year: ["2006"]
month: ["2006-03"]
categories:
  - "debian"
  - "linux"
  - "servers"
tags: []
aliases:
  - "/2006/03/29/howto_set_up_your_own_snort_intrusion_detection_system_with_a_database_backend/feed/"
---

Okay, truth told, I’m completely bored, so I’m going to write a quick tutorial on how to install and set up the Snort IDS on a Debian Sarge System (although it should work on other distros as well).

**Download and Install Snort**  
`apt-get install snort-mysql`

Enter values in the following screen, but forget about the part about the database  
`cd /usr/share/doc/snort-mysql`  
`mysqladmin -u  -p create`   
`zcat create_mysql.gz | mysql -u  -p`
