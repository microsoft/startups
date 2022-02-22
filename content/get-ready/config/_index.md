---
title: "Configuration"
date: 2022-01-11T02:28:49Z
weight: 1
---

## Make your app configurable from the outside

When you deploy your application to the cloud, you're going to want to configure it. Whether the configuration changes the behaviour of the app, or is connection details for a database, it is best to keep this separate from the packaged application. This means that you can deploy the same package to different environments with different configurations passed in, making everything simpler.

{{< resized "EmbeddedConfig.jpg" "600x" >}}

This means that where previously you may have configured your application by editing configuration files, you now need to inject configuration using environment variables or an external configuration service.

### Environment variables

One of the best ways to pass configuration values to our application is environment variables. They are a tried-and-tested way to pass data from a process to one that is executing. You might be familiar with them in a command-line context, but they are useful when starting programs in other ways (like inside a container!).

{{< resized "EnvironmentVariables.jpg" "400x" >}}

By passing configuration variables through Environment Variables, you are able to have a single deployable artefact (your container image) which can be configured based on the deployment environment it is running in (development, testing, or production).

## Excercise: Moving configuration to environment variables

### Step 1: Finding your configuration

In our sample project, the configuration is stored in `project/settings.py`, as is the convention for Django projects. In some cases some configuration values might be embedded in code or in other configuration files. If you miss some, it's okay – you can always come back and fix it later.

When we look in `project/settings.py` we see a lot of values. Not all of these are things that need to be configured from the outside. There are a few that stand out, though.

```python
# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '_*&5c@1153xw6=489*2*=&*%=4)8f^m54kb@3ca-cb(wm%b@wm'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []
```

We see some rather ominous warnings here, and they give us a clue as to what we might want to make configurable. The `SECRET_KEY` is used to provide cryptographic signing within the app for things like sessions, cookies and password reset tokens. `ALLOWED_HOSTS` helps prevent some Cross Site Request Forgery (CSRF) attacks, and is required when we set the `DEBUG` setting to `False` (which we will also need to do).

Using environment variables for these configuration values is relatively straight-forward:

```python
# Since the secret key is a string, we can pass it straight through.
SECRET_KEY = os.getenv('SECRET_KEY')

# DEBUG expects a boolean, so we check if the value is equal to "True"
DEBUG = os.getenv('DEBUG') == "True"

# ALLOWED_HOSTS is an array, so we split the environment variable on commas.
ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', '').split(',')
```

If we run our server now and try and reach a page, we get an error:

```shell
python3 manage.py runserver
```

{{< resized "ErrorScreenshot.png" "600x" >}}

We haven't supplied any environment variables so our configuration is causing an error. We can fix that by adding them to our command:

```shell
SECRET_KEY=verysecure ALLOWED_HOSTS=localhost,127.0.0.1 DEBUG=False python3 manage.py runserver
```

That's a lot of typing, and it's not very fun. We can use a package to keep a set of environment variables _just for local development_. Most languages have a package called "dotenv" which will do just this. Since we're working in django, we're going to add the `python-dotenv` package to our `requirements.txt` file:

```shell
echo python-dotenv >> requirements.txt
```

After adding it to `requirements.txt` we must install the package:

```shell
pip install -r requirements.txt
```

Then add the following lines to the top of `project/settings.py`:

```settings.py
from dotenv import load_dotenv
load_dotenv()
```

And create a new file in the root of your project called `.env`, with your environment variables:

```.env
SECRET_KEY=alotoflettersthatareonlyusedindevelopment
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
```

{{% notice note %}}
You should not add your `.env` file to git, because it can often contain sensitive information. Instead, create a copy, replacing any sensitive information with placeholders and name it `.env-template` to help others onboard to the project and properly configure their environments.
{{% /notice %}}

Now running the server no longer results in any errors. Congratulations! You've set up an app to use environment variables for configuration!
