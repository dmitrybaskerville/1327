2811
====

**THIS PROJECT IS DEPRECATED! No security updates, bugfixes or support will be provided. For the successor of myhpi.de, head to the [new project](https://github.com/fsr-de/myHPI).**

A student representatives website.

## Development

You need to download the source code of 1327 to contribute:

```bash
git clone https://github.com/fsr-de/1327.git
```

Freshly created code needs to be tested - besides our use of unit tests, linting and continous integration, it is possible to run the application in a non-production environment using *Vagrant* or a *Virtual Environment*.

1327 requires `Python 3.6` or higher.

### Vagrant

You can simply set up an execution environment using `vagrant`:

```bash
vagrant up
```

This will set up a virtual machine and run it. Running this for the first time might take a while.

To connect to it and start the application do:

```bash
vagrant ssh
# This will take you inside the virtual machine
./manage.py run
```

At that point you created a vagrant box, running a [PostgreSQL](https://www.postgresql.org/) database server, [Apache](https://httpd.apache.org/) web server and the [Django](https://www.djangoproject.com/) application. The contents are available on the default port `8000`, which allows you to access the website at `http://localhost:8000`.

To login with your local user instead of the default OpenID login, you have to visit `http://localhost:8000/login?local_login=1`

### Virtual Environment

Another way of executing this django application is the use of a virtual python environment. This way bypasses the needs for a virtual machine and simplifies the life with multiple python versions installed.

Before creating a virtual environment, make sure to use `Python 3.6` or higher:

```bash
python --version
# example output
Python 3.6.0
```

Now you can create a virtual environment with that python version:

```bash
python -m venv env
source env/bin/activate
pip install -r requirements-dev.txt
python manage.py migrate
python manage.py createsuperuser --username=admin
python manage.py run
```

After you're done with these steps, you'll need to install all static dependencies
via [Yarn](https://yarnpkg.com/lang/en/).
1. Install Yarn
2. go into the directory `static`
3. run the command `yarn`

#### Troubleshooting

| Error         | Solution    |
| ------------- |-------------|
| `Fatal error: Python.h: No such file or directory`      | Are you on a Debian system (e.g. Ubuntu)? Debian doesn't install development tools by default. Since some of the 1327 dependencies need to be compiled, we need those. You need to install them in your system, e.g. for Python 3.6 via `sudo apt-get install python3.6-dev`, and then recreate the virtual environment.

## Deployment

For deploying on a single machine 1327 you'll need to install all requirements from `requirements.txt`, and you can follow these [instructions](https://github.com/fsr-itse/1327/wiki/Deployment), for setting up a webserver and starting all scripts using a Process Control System, if you like.
You'll also need to setup yarn, as indicated in the last section.

## License

The software is licensed under the terms of the [MIT license](LICENSE). Please note that non-MIT-licensed contents might be part of this repository.
