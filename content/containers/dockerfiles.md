---
title: "Introduction to Dockerfiles"
date: 2021-12-22T02:41:41Z
weight: 2
---

If a container is a way of packaging your application so that you can take it places, a Dockerfile is the list of things to pack and how to pack them into a container image.

## Writing our first Dockerfile

A very simple Dockerfile looks like this:

```Dockerfile
FROM alpine

RUN date > created.txt
ENV GREETING=Hello

CMD [ "/bin/sh", "-c", "echo", "Hello world!" ]

```

Let's break down what each line does:

```Dockerfile
FROM alpine
```

`FROM` tells Docker what we want to base our container image on. In our case we're starting with an Alpine Linux image from the public DockerHub container registry. Alpine Linux is great because it's light-weight, keeping our image size down. In most cases you'll start with an official image for the language or framework you're using, like the Go, .NET, or Ruby.

```Dockerfile
RUN date > created.txt
```

One of the most important commands you'll see in a Dockerfile, the `RUN` command executes whatever command you specify and keeps the result as part of your image. It's great for installing libraries, compiling your code, or running setup scripts. In this case, we've just saved the current date to a file called `created.txt`.

```Dockerfile
ENV GREETING=hello
```

The `ENV` command allows us to specify an environment variable. This is used during the build process, but can also be overriden when we run the container (which you'll see an example of later).

```Dockerfile
CMD [ "sh", "-c" "echo", "$GREETING world!" ]
```

Finally this Dockerfile includes `CMD`, which is the command run by our container. In this case, it's a the traditional greeting of any tutorial or workshop.

## Building our first container

First create a new directory to work from.

```bash
mkdir greeting
cd greeting
```

Then copy the Dockerfile from above into a file called `Dockerfile` in that directory.

Now we can build our container image.

```bash
$ docker build -t greeting

[+] Building 1.8s (6/6) FINISHED
 => [internal] load build definition from Dockerfile                                          0.0s
 => => transferring dockerfile: 34B                                                           0.0s
 => [internal] load .dockerignore                                                             0.0s
 => => transferring context: 2B                                                               0.0s
 => [internal] load metadata for docker.io/library/alpine:latest                              1.3s
 => CACHED [1/2] FROM docker.io/library/alpine@sha256:21a3deaa0d32a8057914f36584b5288d2e5ecc  0.0s
 => [2/2] RUN date > created.txt                                                              0.4s
 => exporting to image                                                                        0.0s
 => => exporting layers                                                                       0.0s
 => => writing image sha256:3d3e5d90c53bc2471b4a3643ce309c74577c9bc54a944009f6223821369ccb0c  0.0s
 => => naming to docker.io/library/greeting                                                   0.0s
```

That will find the Dockerfile in our current directory, pull down the base Alpine image, run the commands and then leave you with a resulting image that we have given the tag `greeting`. We can check it by using this command:

```bash
$ docker images greeting

REPOSITORY   TAG       IMAGE ID       CREATED          SIZE
greeting     latest    3d3e5d90c53b   18 seconds ago   5.59MB
```

We can see our greeting image has been successfully created, and is ready for us to run.

## Running our first container

Now we can run the container.

```bash
$ docker run -it --rm greeting

Hello world!
```

We can also pass environment variables to our container so uses a different greeting.

```bash
$ docker run -it --rm -e GREETING=Salutations greeting

Salutations world!
```

One last trick – we can run a completely different command and see what time our container was built.

```bash
$ docker run -it --rm greeting cat created.txt

Thu Dec 23 00:52:02 UTC 2021
```

Play around with your Dockerfile and the `docker run` command to help you be comfortable with what you can do with Docker and container images. Experimenting is one of the best ways to master new tools.

## Getting Practical

This Dockerfile isn't particularly useful - we want something to help us package our application. Our next module will take us through building a dockerfile for our app.
