---
title: "Creating a Dockerfile for your app"
date: 2021-12-22T02:41:41Z
weight: 3
---

Now that we have some fundamentals of container images and Dockerfiles under our belt it's time to create one for our application. The steps outlined below will work for most applications, whether they're Django, Express, Rails, golang, Elixir or .NET.

## Understanding a Dockerfile

A Dockerfile is a recipe for an image that will contain your app. As part of building this image there are some steps that are almost always included:

1. Choosing a base image
1. Installing any required packages
1. Building the app
1. Add any runtime configuration
1. Specify the runtime commands and entrypoint

### Base Image

Even if you're starting from a blank image (called `scratch` in Docker circles), you've got to start somewhere. There are many options for a starting point, and the best choice is almost always one of the official images for your programming language.

Each image has a number of tags to choose from. These are a combination of underlying base image and language version. For example, for the python official image, the image tagged `python:3.10.2-slim` refers to Python version 3.10.2, built on the latest Debian slim base image.

When you choose a tag, make sure you use the most up-to-date version you're able to. Choosing the underlying base image may be tricky, but to start out with we suggest using images based on the `slim` base image which finds a happy medium between a small image size, and being a familiar environment.

### Install Requirements

There are two sets of requirements that are generally required for your application: those that are installed by the operating system package manager, and those installed by your chosen language's package manager. The best practice is to install the operating system packages first, as it is likely that packages installed by your languages package manager will depend on them.

Some examples of operating system packages you're likely to need:

- database drivers
- compilers and build tools
- libraries for specialised tasks

After installing the operating system packages, installing the package dependencies of your application should be relatively simple. This involves copying whatever file defines the packages to our image, and running the install command. The reason we copy only this file rather than our entire project at this point is to take advantage of Docker's layers and caching. While our application code changes frequently, our dependencies do not. By copying only the file that defines our dependencies, this layer can be kept cached, saving us time when we build our image the next time.

### Build-time Tasks

After installing our requirements, we need to run our build-time tasks.

### Add runtime config

### Runtime tasks
