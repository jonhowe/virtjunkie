---
title: "Change the Author of Multiple WordPress Posts"
date: 2008-10-18T02:08:17-04:00
slug: "change-the-author-of-multiple-wordpress-posts"
url: /2008/10/18/change-the-author-of-multiple-wordpress-posts/
author:
  - "jhowe"
year: ["2008"]
month: ["2008-10"]
categories:
  - "web-development"
tags:
  - "sql"
  - "wordpress"
aliases:
  - "/2008/10/18/change-the-author-of-multiple-wordpress-posts/feed/"
---

Disclaimer: This idea requires access to the shell on your webserver.

This is the SQL query you’ll use:

```sql
UPDATE wp_posts 
SET post_author='[NEW ID]' 
WHERE post_author='[EXISTING ID]';
```

I had posts that were assigned to Admin (which by default is user ID 1), and I wanted to assign them all to my user (which in this case is user ID 2).

My query looked like this:

```sql
UPDATE wp_posts 
SET post_author='2' 
WHERE post_author='1';
```

That will go through the posts database and update the author for all of them.

—  
Jon
