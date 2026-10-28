---
title: "Howto: Convert NRG Files to ISO Files"
date: 2007-01-24T23:55:28-05:00
slug: "howto-convert-nrg-files-to-iso-files"
url: /2007/01/24/howto-convert-nrg-files-to-iso-files/
author:
  - "jhowe"
year: ["2007"]
month: ["2007-01"]
categories:
  - "linux"
tags: []
aliases:
  - "/2007/01/24/howto-convert-nrg-files-to-iso-files/feed/"
---

I recently got a couple fo CD images from a friend in the NRG format, and wanted to burn them to a couple of CD-R’s. Here’s the process I used to do this:

```bash
sudo apt-get install nrg2iso
nrg2iso original_image.nrg new_image.iso
```

Then just use k3b, gnomebaker, or your favorite CD Burning software to burn the ISO.

Jon
