---
title: "How to Back up a MYSql Database for Simple Offsite Storage"
date: 2005-12-15T13:04:54-05:00
slug: "how_to_back_up_a_mysql_database_for_simple_offsite_storage"
url: /2005/12/15/how_to_back_up_a_mysql_database_for_simple_offsite_storage/
author:
  - "jhowe"
year: ["2005"]
month: ["2005-12"]
categories:
  - "servers"
tags: []
aliases:
  - "/2005/12/15/how_to_back_up_a_mysql_database_for_simple_offsite_storage/feed/"
---

For those of you who have been reading this blog for a while you that in the past I’ve had some problems keeping this server up and running for any amount of time.

This got old because every time that my server died, I’d loose all of my blog posts, which stinks because there’s usually a ton of them.

To combat this ever threatning possibility, I decided to write a bash script for linus that does a few things:

1. Backs up the entire database
2. Archives them
3. Encrypts them using [CCRypt](http://ccrypt.sourceforge.net/), although you can substitute that for whatever you want without bash knowledge
4. Places the encrypted archive in a directory. (I just stuck the archive in a public web directory.

I should clarity a little bit… Putting even a highly encrypted archive in a public directory is not 100% secure. It’s especially not recommended if you are storing sensitive data, and especially if you’re storing passwords in plaintext in your database. (Please don’t do that…). Consider yourself warned.

Unfortunately, there’s another security flaw here, although like the last one, it’s not a show-stopper (for me at least). The only way that I could do the entire process automatically is by storing the password in a plaintext file somewhere either in the script itself or some external file (which is how it’s being distributed now). I think that it’s possible to create a [wrapper](http://en.wikipedia.org/wiki/Wrapper) that contains the password in a compiled (much less human readable), and have that access ccrypt, but I don’t have the time or need for that right now, although it is a good idea :).

I should probably mention that this script is meant to be run by a cron script.

So, without further ado, here it is:

`#!/bin/sh  
  
# backs up all databases  
# archives them  
# encrypts them  
# places them in a directory that you choose  
  
  
user=[database usename]  
pass=[database password]  
finaldir=[directory to store final encrypted archive]  
passpath=[path to a text file containing plaintext password]  
#=======================================================  
#You shouldn' have to edit anything below here  
#=======================================================  
  
  
workingdir=/root/dbback  
dumpname=db.sql  
pathtosql=/usr/bin/mysqldump  
arch=$dumpname.tar.gz  
crypto=$arch.cpt  
  
  
# Test to see if $workingdir exists  
[ -d $workingdir ] || mkdir $workingdir  
  
  
# Backs up all databases temporarily to $homedir/$dumpname  
$pathtosql -u $user --password=$pass -A > $workingdir/$dumpname  
  
  
# archives the database  
tar -czf $workingdir/$arch $workingdir/$dumpname  
  
  
# encrypts DB package  
ccrypt -e -fbrk $passpath $workingdir/$arch  
  
  
# copies the encrypted archive to $finaldir  
cp -Rf $workingdir/$crypto $finaldir/db@$(date +%F).tar.gz.cpt  
  
  
# make the encrypted database internet readable  
chmod 755 $finaldir/*.cpt  
  
  
# removes the files that were used in the creation of the encrypted archive  
rm -f $workingdir/*`

If you have any qyestions, or comments feel free to leave a comment and I’ll get back to you ASAP.

Later,  
Jon Howe
