---
title: "How to Script the Unattended Retrieval of Remote Files using SCP"
date: 2005-12-19T17:22:52-05:00
slug: "how_to_script_the_unattended_retrieval_of_remote_files_using_scp"
url: /2005/12/19/how_to_script_the_unattended_retrieval_of_remote_files_using_scp/
author:
  - "jhowe"
year: ["2005"]
month: ["2005-12"]
categories:
  - "linux"
tags: []
aliases:
  - "/2005/12/19/how_to_script_the_unattended_retrieval_of_remote_files_using_scp/feed/"
---

In one of my previous posts I told how to create a package that’s contents is dumped from the database, archived, encrypted, and put into a public directory.

I also mentioned that a potential security flaw on this system was that someone with enough time and processing power could decrypt your package and get all of it’s contents.

I thought about this and decided that I wanted a better way. So, I found a way to script an unattended / secure connection between the remote computer and the client computer using SCP and SSH keys.

The first thing that you want to do to set this up is make sure that you have a way to use SCP without it prompting you for a password. You do this by using something called an ‘SSH key’. To generate an SSH key use the following command.

`ssh-keygen -t rsa`

What this does is:

1. Creates both a public and private key
2. Asks you where to put both of the generated keys (use the defaults)
3. Asks you if you want to use a passphrase (this isn’t neccessary, and I think that it messes up the unattended part of the command, so don’t do it)

After that you have to put the public key, which should be located at ‘~/.ssh/id\_rsa.pub’ into the users .ssh directory which is inside their home directory (for example: /home/jhowe/.ssh).

After that you have to make sure that the client and server know that in the future they will be connecting to each other without a password. You do this by creating a file on the server in the server user’s .ssh directory called authorized\_keys2 with the information about your private key in it. Fear not, this process is greatly simplified by SCP. Just enter the following command and it will be done for you automatically.

(Put this all on one line)  
`scp  
[Client_Username]/.ssh/id_rsa.pub [Server_Username]@[Server_Address}: /[Server_Username]/.ssh/authorized_keys2`

…Then enter the server username’s password, and it will copy to the file on the server for you. If you want to make sure that it’s there, open ‘/[server\_username]/.ssh/autohorized\_keys2’, and see if it has a bunch of random looking charachters. If so, then it worked.

If all of the steps so far have been completed correctly you should be able to use SCP in a script to get your database archive in a directory that’s not web-readable, therefore eliminating the risk of some ruthless hacker decrypting your database package, and stealing all of your data.

Again, time for the downside. This isn’t a very big downside, but it needs to be mentioned. It’s important to note that the Private key, which was created at the same time as the public key (which was sent to your server) needs to be protected with your life. The reason that I say this is because if it’s stolen anyone that has it will be able to connect to your server if they get it. If there’s a posibility of someone else using the client computer that you enter `chmod 400 ~/.ssh/id_rsa` to make it that only root can read the file.

As always, if you have any problems or questions feel free to leave a comment and I’m be more than happy to help you in any way that I can.

Later,  
Jon Howe
