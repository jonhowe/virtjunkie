---
title: "VMware Horizon Workspace – Part 3 – Configure VMware vPostgres External Database"
date: 2013-11-23T00:09:43-05:00
slug: "vmware-horizon-workspace-part-3-configure-vmware-vpostgres-external-database"
url: /2013/11/23/vmware-horizon-workspace-part-3-configure-vmware-vpostgres-external-database/
author:
  - "jhowe"
year: ["2013"]
month: ["2013-11"]
categories:
  - "horizon-workspace"
  - "uncategorized"
  - "vmware"
tags: []
aliases:
  - "/2013/11/23/vmware-horizon-workspace-part-3-configure-vmware-vpostgres-external-database/feed/"
---

In this post I’ll show in detail how to configure Horizon Workspace to use an external database during the install process.  This post is [part of a series](http://45.63.13.214/?p=522) showing how to [configure VMware Horizon Workspace](http://45.63.13.214/?p=522 "VMware Horizon Workspace – Part 0 – Intro") in a production environment. You’ll need an external database to have multiple service virtual appliances, so this should be a requirement for your environment.  This process was suprisingly not trivial for me, however it could have something to do with the fact that I haven’t used postgres sql in the past.

<!--more-->

Some assumptions and prerequisites:

1. You have horizon workspace 1.5.1 (at least) downloaded, deployed to your infrastructure successfully, and you’re ready to go through the web configuration.
2. You have [VMware vFabric Postgres](http://www.vmware.com/products/vfabric-postgres/) downloaded and deployed to your infrastructure successfully, with no configuration added.

1. Proceed through the web configuration until you get to step 2a, and select External Database. Stop here…
2. Prepare your new external database
   1. SSH to the postgres server (I’ll assume the server is named hzn-db.test.in)
   2. Make changes to the postgres config: /var/vmware/vpostgres/9.2/pgdata/postgresql.conf.auto
      1. Max\_connections = 300 (default is 100)
      2. Search\_path = ‘saas’ (no value by default)
   3. You’ll have to prepare the postgre sql schema. Run these commands to configure it. VMware graciously has not provided the default password for the postgres user in any of their documentation, even after I opened a SR requesting the password. For your reference, it is “H0rizon!”. “myPassword” below should be replaced with the password you want to use for your horizon workspace postgres user.
      1. /opt/vmware/vpostgres/current/bin/psql -U postgres -W
      2. DROP SCHEMA IF EXISTS saas CASCADE;
      3. CREATE SCHEMA saas;
      4. CREATE USER horizon WITH PASSWORD ‘**myPassword**‘;
      5. ALTER ROLE horizon SET search\_path TO saas;
      6. CREATE EXTENSION citext WITH SCHEMA saas;
      7. CTRL+D
   4. SSH to your service-va, and run the following command
      1. /usr/local/horizon/bin/setupExternalDb.sh
      2. The wizard will ask you for a postgres admin user (postgres), and the horizon user (horizon). The password for the postgres user, unless you change it is “H0rizon!”, and the password for the horizon user is set in step 3.

This should work – if you run into any issues, please comment!
