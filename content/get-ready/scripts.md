---
title: "Scripts"
date: 2022-01-11T02:29:28Z
---

## Prefer admin scripts over interactive commands

As we build our products, we often find ourselves in the command-line running various commands as part of setting up and running our apps. While we're building this makes sense – but as we deploy we want to automate as much of this as possible.

There's a couple of reasons for this – firstly, it makes everything more repeatable are reliable. Almost every engineer has war stories about an incorrectly typed command causing issues. Having those commands automated removes that risk. Secondly there is your time and energy – if you don't have to think about these steps you can invest your energy into your product

We can divide the common times we run interactive commands into three types:

### Build-time tasks

There's a few things that we do every time we build our app – it might be compiling code, installing dependencies or creating other artefacts to be deployed withour app. It's important to reflect on the steps we take each time we build our app as these will become central in our Continuous Integration/Continuous Delivery (CI/CD) pipleline.

Common build-time tasks include:

- Installing dependency packages
- Collecting and pre-processing static assets like images, stylesheets and javascript.
- Updating manifest files
- Generating (but not running) database migrations.

Your application build may include other tasks, so it is worthwhile to reflect as you work on your application, and keep a text file with commands you run frequently.

### Deploy Tasks

Just like tasks that happen each time we build our application, there are some tasks which we need to do as part of deployment. These are commonly centred around the infrastructure your application relies upon. The tasks commonly include:

- Running database migrations
- Clearing caches
- Deploy or configuring infrastructure

Since you're not yet deploying an application, it can be hard to know what these tasks might be. A good rule of thumb is that any time you might be tempted to log into a server as part of a deployment process, this is a deploy task which you need to capture and include in an automated deployment.

### Ad-hoc Tasks

Finally, there are ad-hoc tasks. These tasks happen occasionally and may be part of the general maintenance of your application. In general it is best to avoid ad-hoc tasks where possible, but where they must happen, creating ways for them to be done consistently and securely is important.
