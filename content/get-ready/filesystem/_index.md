---
title: "Filesystem"
date: 2022-01-11T02:29:07Z
weight: 2
---

## Store your data away from the local filesystem

On your personal machine, it's easy to read and write files on the local disk. That changes when you deploy to the cloud. As you deploy your app to the cloud, you need to find other places to keep your data. You should always treat any deployed instance of your app as _ephemeral_ – it could disappear at any time and be replaced by a fresh copy, taking any data you've written to the disk with it.

The reason for this is that when you deploy to the cloud, it's common that you will _scale out_ your application. That means that instead of adding memory or CPU power to a single host (which is called _scaling up_), you add more instances of your application to serve requests. That means that files stored locally aren't easily shared, and inconsistency can develop between your application instances. If you instead rely on an external service to store this shared state (like a Database as a Service or blob storage), you can reduce the complication of your application and scale out with ease.

{{% notice note %}}

There is one exception to the rule when it comes to the local disk – temporary files that are required to satisfy a request. These should truly be temporary and you should be ready for them to go away at any time.

{{% /notice %}}

### Database as a Service

When you're first developing an app, it's quick to get started with a simple file-based database like SQLite. In fact for frameworks like Django and Ruby on Rails, this is the default. It's great – you don't have to worry about running a local database server, or other such complications.

Once you to push your app to the cloud you can't rely on files on the local disk. You need something else. This is where Database as a Service comes in. While you could set up your database of choice inside a container, or on a virtual machine, it's not the best use of your time. Instead, you can use a Database as a Service, which gives you an instance of your preferred flavor of database which you can make accessible to your app.

It can scale with you, and you don't have to worry about the details of managing a database server.

## Exercise: Adding a database server to your application

### Create a database server

First we need to create a database server in the cloud. This involves choosing which kind of database we need and which size, setting up an administrator, and choosing where to deploy it. We can do all this without leaving Visual Studio Code.

{{% notice tip %}}
We use the Visual Studio Code [Command Palette](https://code.visualstudio.com/docs/getstarted/userinterface#_command-palette) to run commands in this exercise. To open the command palette, press **Control** + **Shift** + **P** on Linux and Windows, or **Command** + **Shift** + **P** on macOS.
{{% /notice %}}

1. Choose **Azure Database: Create Server** from the command palette.
  ![](database_create_server.png)
2. Select **PostgreSQL Flexible Server** from the list of options.
  ![](select_server_type.png)
3. Enter a unique name for your database server.
  ![](name_server.png)
4. Enter an admin username for the database server. For this example we will use **relecloud_admin**.
  ![](admin_user.png)
5. Enter an admin password for the database server. Make sure you make a note of the password.
  ![](admin_password.png)
6. Re-enter the admin password to confirm it.
7. Create a new resource group to contain the database server.
  ![](create_resourcegroup.png)
  ![](resourcegroup.png)
8. Select a region to deploy your database server to. It is best to choose a region where you plan to deploy your application servers.
  ![](region.png)

It may take a short while for the database server to be created.

### Configure the server to allow you to access it

By default, all connections to your new database server are blocked by the firewall. To connect to the database server we must add a firewall rule which allows your current IP address to connect to the server.

1. Select **PostgreSQL: Configure Firewall** from the command palette.
  ![](postgresql_firewall.png)
2. Choose the database server you just created from the list.
  ![](select_account.png)
3. Click _Yes_ on the resulting dialog to create the firewall rule for your IP address.
  ![](firewall_dialog.png)

### Create the database

Now that we have access to our database server, we want to create a database just for our application. The server already has a default `postgres` database, but we don't want to modify that.

Select **PostgreSQL: Create Database** from the command palette.

Choose a name for your database. We will use `relecloud`.

Congratulations! You've created the database.

### Configure the application to connect to the database server

Add `psycopg2` to `requirements.txt`.

  ```txt
django
django-crispy-forms
python-dotenv
psycopg2
  ```

Install the package with pip:

  ```cli
  pip install -r requirements.txt
  ```

We're going to update the database section of `project/settings.py` to point to your newly created database server. Currently it is configured to use the file-based sqlite3 database.

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```

We're going to use environment variables so we avoid storing any sensitive values to source control.

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.getenv('DB_NAME'),
        'HOST': os.getenv('DB_HOST'),
        'USER': os.getenv('DB_USER'),
        'PASSWORD': os.getenv('DB_PASSWORD')
    }
}
```

Now that the application is reading from the environment variables, we need to set the local environment variables for the app in the `.env` file we created previously.

To get the information we need, we'll select the **PostgreSQL: Copy Connection String** command from the command palette. Then, select the subscription you've deployed into, the database server, and finally the database you've created. The connection string will then be copied to your clipboard.

Paste the connection string into the bottom your `.env` file. It should look something like this:

```text
postgres://relecloud_admin:VerySecurePassword!1@demo-relecloud.postgres.database.azure.com:5432/relecloud
```

We need to extract different parts of this connection string to use as environment variables. The format of the URL is:

```text
postgres://DB_USER:DB_PASSWORD@DB_HOST:5432/DB_NAME
```

So extracting the fields into our `.env` file will look like this:

```.env
DB_USER=relecloud_admin
DB_PASSWORD=VerySecurePassword!1
DB_HOST=demo-relecloud.postgres.database.azure.com
DB_NAME=relecloud
```

Once you've added the fields, remove the connection string from the end of the `.env` file.

### Run migrations

We've got the database configured to connect to our new database in Azure, but right now it's empty. If we were to start our app now, it would throw errors because none of the structures the app requires are there. We can run migrations to set up those structures in the Postgres database:

```bash
python3 manage.py migrate
```

Now with those migrations complete, we can launch our local server.

```bash
python3 manage.py runserver
```

You should see the application successfully running.

Congratulations! You're one step closer to deploying your app to the cloud!
