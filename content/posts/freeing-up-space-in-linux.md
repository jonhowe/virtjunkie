---
title: "Quick Tips for freeing up space in Linux"
date: 2019-06-25T09:26:31-04:00
slug: "freeing-up-space-in-linux"
url: /2019/06/25/freeing-up-space-in-linux/
author:
  - "jhowe"
year: ["2019"]
month: ["2019-06"]
categories:
  - "linux"
  - "servers"
tags: []
aliases:
  - "/2019/06/25/freeing-up-space-in-linux/feed/"
---

Practice what you preach, right? I try to keep my root partition on my personal machine pretty anemic.. usually between 40G and 60G. However, lately I’ve been running out of space and I wasn’t sure why. Here are a few tips and tricks for finding the culprit, and freeing up some space.

<!--more-->

**Identify Large Files**  
First thing’s first.. let’s figure out what’s taking up the space. The snippet below will locate large files

```text
sudo find / -mount -ls | awk '{print $7, $11}' | sort -rn | less
```

**Duplicate Snaps**  
Snapd by default keeps 2 copies of your snaps. Unfortunately, you can’t set the default amount to keep to anything less than 2. Since this is my personal machine, and some of my snaps are pretty large (~1G in come cases), I only want to keep a single copy of them. The snippet below will remove all but the latest copy of a snap.

```text
snap list --all | while read snapname ver rev trk pub notes; do if [[ $notes = *disabled* ]]; then snap remove "$snapname" --revision="$rev"; fi; done
```

If you want to keep more than the default of 2 snaps, you can use this snippet:

```text
sudo snap set system refresh.retain=5
```

**Snapd Snapshots?**  
For some reason I had a number of snapd snapshots on my system. You can list them like this:

```text
snap saved
```

The “Saved” column is a unique identifier that is required when removing a snap. To remove a snapshot with ID of 1, run the following snippet:

```text
snap forget 1
```

**Docker Logs Are Out Of Control!**  
When I identified the large files, I saw that a docker container was using >20G of space. I stopped the container, removed the log file, and then started the container again. To prevent this issue from happening in the future, start your container while specifying the max-file and max-size parameters like the snippet below:

```text
docker run --log-opt max-size=15m --log-opt max-file=2 dockerapp
```

**Journal is using way too much space**  
Since this is a personal workstation and logging isn’t my biggest priority, we can limit the journal. To see how much space you’re currently using, run the following snippet

```text
journalctl --disk-usage
```

There are three ways you can limit the journal:

1. Limit by size of all journal files
2. Limit by amount of journal files
3. Limit by age of journal files

You can handle each one of these using the snippets below

```text
# By Size - Specify values in bytes or use K, M, G, T, P, E as units 
# for the specified sizes
journalctl --vacuum-size=200M

# By amount of files
journalctl --vacuum-files=15

# By age of files - specified with the usual "s", "m", "h", "days", 
# "months", "weeks" and "years" suffixes
journalctl --vacuum-time=7days
```

[You can check the manpage online here](https://www.freedesktop.org/software/systemd/man/journalctl.html)

**Spotify Cache in Snap**  
I recently noticed that Spotify has been caching tons of data on my desktop. Since I pay them to be a streaming service, I don’t really appreciate this. Fortunately, there’s a way to limit how much they cache on my machine. The changes below will limit Spotify to only cache 256MB locally.

```text
edit this file:
/home/$USER/snap/spotify/current/.config/spotify/prefs

add the line:
storage.size=256
```

**In Conclusion**  
It should go without saying that you should adhere to completely different standards if you’re running out of space on a server, and that you should test these snippets on a mission critical system. These steps should all be non-intrusive on a desktop, if you’re concerned, test them on a less critical system first.
