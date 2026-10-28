---
title: "Howto: AJAX Regular Expression Email Verifier"
date: 2006-03-31T23:05:13-05:00
slug: "howto_ajax_regular_expression_email_verifier"
url: /2006/03/31/howto_ajax_regular_expression_email_verifier/
author:
  - "jhowe"
year: ["2006"]
month: ["2006-03"]
categories:
  - "php"
  - "web-development"
tags: []
aliases:
  - "/2006/03/31/howto_ajax_regular_expression_email_verifier/feed/"
---

It’s important to do form validation for obvious reasons. This is an implementation of an email checker that uses php regular expressions, and a little bet if pizzaz with asynchronous javascript and xml, or AJAX.

[Here’s the example.](/blog/blogfiles/ajax_email_regex/ajax_email_regex.php)

A quick rundown of how this works is:

1. You type in a string
2. You hit submit
3. The data is transfered asynchronously (without refreshing the page) to the server
4. The server checks to see if the email is valid or invalid
5. If it’s valid it tells you so, as well as if it’s not

The guts of the script are here:  
`if (eregi("^[a-zA-Z0-9_-.+]+@[a-zA-Z0-9-]+.[a-zA-Z0-9-_.]+$",$email)) {  
//return confirmation that it worked  
}  
else {  
//return that it didn't work  
}`

Basically, it checks to see if there’s either a lowercase or uppercase a-z or 0-9 or an underscore, or a dash, or a period before the @ sign ([a-zA-Z0-9\_-.+]+@). Then after the @ sign it checks for the same thing except for the period and the underscore up until another dot. After that dot it checks once again for the same charachters as the first set.

Hopefully this helps someone. If you have any questions feel free to email me at “howe -dot- jon -at- gmail -dot- com” and I’ll help you however I can.

Later,  
Jon Howe
