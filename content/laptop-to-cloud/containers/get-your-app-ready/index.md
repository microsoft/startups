---
title: "Get your app ready"
date: 2021-12-23T23:10:50Z
---

When you deploy your application using containers, you gain a lot: isolation, consistency, portability, and scalability to name a few. While most applications should be able to run happily in a container, there are a few things that you need to do to make sure you have the best experience using containers.

## Make your app configurable from the outside

Once your application is packaged into a container image, while it is *possible* to modify it by creating extra layers, it is recommend that you treat it as immutable. The same image should be deployed to development, testing, and production environments with changes in configuration values driving any changes in behavior.

{{< resized "EmbeddedConfig.jpg" "600x" >}}

This means that where previously you may have configured your application by editing configuration files, you now need to inject configuration using environment variables or an external configuration service.


### Environment variables

One of the best ways to pass configuration values to our application is environment variables. They are a tried-and-tested way to pass data from a process to one that is executing. You might be familiar with them in a command-line context, but they are useful when starting programs in other ways (like inside a container!).

{{< resized "EnvironmentVariables.jpg" "400x" >}}

By passing configuration variables through Environment Variables, you are able to have a single deployable artefact (your container image) which can be configured based on the deployment environment it is running in (development, testing, or production).

{{< youtube id=r9MWQsIGrM0?rel=0 >}}


## Store your data away from the local filesystem

### Blob storage

### Temporary files

## Send your logs to the console

## Prefer admin scripts over interactive commands

##

