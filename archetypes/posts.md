---
title: "{{ replace .Name "-" " " | title }}"
date: {{ .Date }}
slug: "{{ .Name }}"
author:
  - jhowe
year:
  - '{{ .Date.Format "2006" }}'
month:
  - '{{ .Date.Format "2006-01" }}'
categories: []
tags: []
---
