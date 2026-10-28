---
title: "VMware Provisioning using Hashicorp Terraform  – Part 2"
date: 2020-07-06T09:00:00-04:00
lastmod: 2021-07-05T22:22:32-04:00
slug: "vmware-provisioning-using-hashicorp-terraform-part-2"
url: /2020/07/06/vmware-provisioning-using-hashicorp-terraform-part-2/
author:
  - "jhowe"
year: ["2020"]
month: ["2020-07"]
categories:
  - "automation"
  - "hashicorp"
  - "infrastructureascode"
  - "terraform"
  - "vmware"
tags: []
aliases:
  - "/vmware-provisioning-using-hashicorp-terraform-part-2/"
  - "/2020/07/06/vmware-provisioning-using-hashicorp-terraform-part-2/feed/"
---

In the [first part of this series](/vmware-provisioning-using-hashicorp-terraform/) we went over Terraform at a very high level and discussed a basic example of using it to provision a single Windows VM or a single Linux VM. While this is a helpful baseline, it doesn’t realistically help us when defining our application structure in code. For example, if you wanted to set up a [three tier application](https://en.wikipedia.org/wiki/Multitier_architecture#Three-tier_architecture) you’ll need to have three separate instances of the project we used. At that point we’re not really gaining much efficiency over deploying a template in vCenter. In this post I’ll discuss Terraform Modules, give an example of how to store your Terraform Module in GitHub, and provide a real-life example of how to deploy a three tier application using multiple source images.

<!--more-->

Table of Contents

Toggle

- [Introduction to Terraform Modules](#Introduction_to_Terraform_Modules "Introduction to Terraform Modules")
  - [Terraform Registry](#Terraform_Registry "Terraform Registry")
- [Roll Your Own Module](#Roll_Your_Own_Module "Roll Your Own Module")
  - [Best Practices](#Best_Practices "Best Practices")
  - [Why store your module in GitHub?](#Why_store_your_module_in_GitHub "Why store your module in GitHub?")
  - [File Structure](#File_Structure "File Structure")
    - [main.tf](#maintf "main.tf")
    - [variables.tf](#variablestf "variables.tf")
    - [output.tf](#outputtf "output.tf")
- [How to use this module?](#How_to_use_this_module "How to use this module?")
- [References and what’s next?](#References_and_whats_next "References and what’s next?")
  - [What’s Next?](#Whats_Next "What’s Next?")
  - [References](#References "References")

## Introduction to Terraform Modules

In Part 1 of this series I [compared traditional programming languages to Terraform](/vmware-provisioning-using-hashicorp-terraform/). We can do the same thing with Modules. For example, with Powershell or Python, you can download a module that provides functionality and consume that functionality in your code without having to author it. The same thing happens in Terraform, and just like with other languages, you can create your own, or download one from a third party.

### Terraform Registry

Thankfully, [Hashicorp provides us with a registry](https://registry.terraform.io/) that we can use to find and consume Terraform Modules. At the time this post is published, the Terraform Registry contains support for [63 providers](https://registry.terraform.io/browse/providers) and has [3454 Modules](https://registry.terraform.io/browse/modules). So if you are looking for specific functionality, check there first!

## Roll Your Own Module

That said, you may have a need to create your own module, or if you’re like me, want to make sure you understand how modules work before you use one that someone else created.

### Best Practices

First and foremost, you’ll want to take a look at the official documentation from Hashicorp on the standard module structure. It gets pretty in-depth, but I’ll hit on a few high level important items.

- Store your module in github
- At the very least, make sure you split your variables and outputs into different TF files
- Include an examples directory and show every variation of how to call your module. For example, if you can create a linux image or a windows image, but you need to call them differently, show an example for each.
- Include a README.md file that has a description of the module, but also references your examples

### Why store your module in GitHub?

Aside from the wide ranging benefits of using version control, using GitHub will allow you to call a specific version of your module.

### File Structure

The following files should be in your GitHub reposity. When you run `terraform init`, it will be downloaded to the .terraform directory on the machine running the project.

#### main.tf

<script src="https://gist.github.com/jonhowe/7526c2316eda915116ae63248154b4cb.js"></script>

#### variables.tf

<script src="https://gist.github.com/jonhowe/5d44ecc0680f4c64447f9e7bab7b5150.js"></script>

#### output.tf

<script src="https://gist.github.com/jonhowe/81b6205c683c0a9273e29b9c62ee8a79.js"></script>

## How to use this module?

Now that we’ve created our module and have it in Github, all we need to do in order to complete our initial goal of having a three tier application is to create a single main.tf file, and call the module 3 times. Below is an example that allows us to set separate information for each of the new VMs.

<script src="https://gist.github.com/jonhowe/f81432f089cb3bbc36113ce29e4f1db4.js"></script>

## References and what’s next?

### What’s Next?

At this point we have shown how to create and [manage images using packer](/vmware-template-packer/), a [couple](/vmware-provisioning-using-hashicorp-terraform/) of [parts](/vmware-provisioning-using-hashicorp-terraform-part-2/) on how to use Terraform to deploy infrastructure, so all we have left is doing configuration of our newly created VMs.

- Use Ansible to configure our newly provisioned VMs
- Wrap the Terraform VM Deployment process, as well as the Ansible VM configuration process together into a single process you execute once
- Use Ansible to do a greenfield deployment of a vSphere environment

### References

- [Part 1 – Provision VMware VMs using Terraform](/vmware-provisioning-using-hashicorp-terraform/)
- [Terraform Registry](https://registry.terraform.io/)
- [Module Structure](https://www.terraform.io/docs/modules/index.html#standard-module-structure)
