---
title: "Get your app ready"
date: 2021-12-23T23:10:50Z
weight: 1
---

When you deploy your application using containers, you gain a lot: isolation, consistency, portability, and scalability to name a few. While most applications should be able to run happily in a container, there are a few things that you need to do to make sure you have the best experience using containers.

## Store your data away from the local filesystem

On your personal machine, it's easy to read and write files on the local disk. That changes when you deploy to the cloud. As you deploy your app to the cloud, you need to find other places to keep your data. You should always treat any deployed instance of your app as _ephemeral_ – it could go away at any time and be replaced by a fresh copy, taking any data you've written to the disk with it.

### Database as a Service

When you're first developing an app, it's quick to get started with a simple file-based database like SQLite. In fact for frameworks like Django and Ruby on Rails, this is the default. It's great – you don't have to worry about running a local database server, or other such complications.

Once youto push your app to the cloud you can't rely on files on the local disk. You need something else. This is where Database as a Service comes in. While you could set up your database of choice inside a container, or on a virtual machine, it's not the best use of your time. Instead, you can use a Database as a Service, which gives you an instance of your preferred flavor of database which you can make accessible to your app.

It can scale with you, and you don't have to worry about the details of managing a database server.

### Blob storage

### Temporary files
There is one exception to the rule when it comes to the local disk – temporary files that are sometimes required to satisfy a request. These should truly be temporary and you should be ready for them to go away at any time.


