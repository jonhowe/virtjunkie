---
title: "Command of the week #3"
date: 2005-09-27T16:30:15-04:00
slug: "command_of_the_week_3"
url: /2005/09/27/command_of_the_week_3/
author:
  - "jhowe"
year: ["2005"]
month: ["2005-09"]
categories:
  - "general"
tags: []
aliases:
  - "/2005/09/27/command_of_the_week_3/feed/"
---

This week’s command is: *useradd*.

This command is used to add new users to your linux system. The syntax is as follows:  
`useradd [options] [user]`

The following was taken from a great site for learning about linux commands(ss64.com) and will further explain the command:

OPTIONS  
-c comment Comment field.

-d dir Home directory.  
The default is to use user as the directory name  
under the home directory specified with the -D option.

-e date Account expiration date.  
date is in the format MM/DD/YYYY.  
Two-digit year fields are also accepted.  
The value is stored as the number of days since January 1, 1970.  
This option requires the use of shadow passwords.

-f days Permanently disable account this many days after the  
password has expired. A value of -1 disables this feature.  
This option requires the use of shadow passwords.

-g group Initial group name or ID number.  
If a different default group has not been specified using the -D option,  
the default group is 1.  
-G groups Supplementary groups given by name or number in a comma-separated  
list with no whitespace.

-k [dir] Copy default files to user’s home directory.  
Meaningful only when used with the -m option.  
Default files are copied from /etc/skel/ unless an alternate dir is specified.

-m Make user’s home directory if it does not exist.  
The default is not to make the home directory.

-o Override. Accept a nonunique uid with the -u option. (Probably a bad idea.)

-s shell Login shell.

-u uid Numerical user ID. The value must be unique unless the -o option is used.  
The default value is the smallest ID value greater than 99 and greater  
than every other uid.

-D [options] Set or display defaults. If options are specified, set them.  
If no options are specified, display current defaults. The options are:

-b dir Home directory prefix to be used in creating home directories.  
If the -d option is not used when creating an account, the  
user name will be appended to dir.

-e date Expire date. Requires the use of shadow passwords.

-f days Number of days after a password expires to disable an account.  
Requires the use of shadow passwords.

-g group Initial group name or ID number.

-s shell Default login shell.
