---
Title: Quickstart on Pipenv (Python packaging tool)
Date: 2020-04-01
Author: smirza
Slug: intro-to-pipenv
Summary: A quickstart guide for pipenv that captures a collection of all its useful commands/operations.
Tags: python
Status: published
---

This blog was originally posted on:
[https://sm087.github.io/pipenv-quickstart.html](https://sm087.github.io/pipenv-quickstart.html)

Pipenv is a packaging tool for Python that solves some common problems associated with the typical workflow using pip, virtualenv, and the good old requirements.txt.

## Installation

`pip3 install pipenv`

## Package installation using pipenv

`pipenv install requests`

If a pipenv is not setup for the application yet, running the above will create a virtual environment along with the installation of pipenv and also create `Pipfile` and `Pipfile.lock` under the application directory.

The below shows a sample pipfile (`toml`):

```
[[source]]
name = "pypi"
url = "https://pypi.org/simple"
verify_ssl = true

[dev-packages]

[packages]
requests = "*"

[requires]
python_version = "3.7"
```

you can install package you need, flask. For example you need version 0.12.1 and not the latest version, so go ahead and be specific by:

`pipenv install flask==0.12.1`

You can also install directly from a version control system by:

`pipenv install -e git+https://github.com/requests/requests.git#egg=requests`

## Production Environment based package Install

Let’s say you have some unit tests for the application that you are building, and you want to use pytest for running them. You don’t need pytest in production so you can specify that this dependency is only for development with the --dev argument:

`pipenv install pytest --dev`

This package will be auto added by pipenv to the Pipfile under `[dev-packages]`.

## Activate your pipenv environment

Spawn a shell in a virtual environment to isolate the development of your app by running:

`pipenv shell`

## Deactivate your pipenv environment

To deactivate the environment spawned by running the above command use `exit`. Avoid using `deactivate` as this does not completely (not a clean) exit from a pipenv environment.

```
(myenv)$ exit
exit
```

## Running a script

You can run a script without activating the environment created.

`pipenv run python scripts.py`

You can also run a command in the virtual environment without launching a shell by:

`pipenv run <insert command here>`

## Install from requirements.txt

You can install required packaged for an app from a legacy virtual environment `requirements.txt`

`pipenv install -r pathto/requirements.txt`

## Uninstall a Package

Now, let’s say you no longer need a package. You can uninstall it:

`pipenv uninstall requests`

If you want to wipe off all the packages from the environment:

`pipenv uninstall --all`

### Pip Freeze in pipenv

This is the equivalent to `pip freeze`, gives you the list of packages installed under that environment.

`pipenv lock -r`

## PipEnv Path(s)

To find out where your virtual environment is located:

`pipenv --venv`

To find out where your project home is

`pipenv --where`

## Package vulnerabilities

Check for security vulnerabilities in your environment:

`pipenv check`

## Environment Variables and PipEnv

Pipenv supports the automatic loading of environmental variables when a .env file exists in the project directory. That way, when you pipenv shell to open the virtual environment, it loads your environmental variables from the file. The .env file just contains key-value pairs:

```text
SECRET_KEY=somerandomekey
```

```
14:03:47~/PycharmProjects/cloudMigrationDVApp$ pipenv run python
Loading .env environment variables…
Python 3.7.3 (v3.7.3:ef4ec6ed12, Mar 25 2019, 16:52:21)
[Clang 6.0 (clang-600.0.57)] on darwin
Type "help", "copyright", "credits" or "license" for more information.
>>> import os
>>> os.environ['SECRET_KEY']
'somerandomekey'
>>>
```

## Dependency mapping with PipEnv (with pipenv graph command)

Pipenv can show a dependency graph to understand your top-level dependencies and their sub-dependencies:

`pipenv graph`

```
$ pipenv graph
openpyxl==2.6.2
  - et-xmlfile [required: Any, installed: 1.0.1]
  - jdcal [required: Any, installed: 1.4.1]
requests==2.22.0
  - certifi [required: >=2017.4.17, installed: 2019.3.9]
  - chardet [required: >=3.0.2,<3.1.0, installed: 3.0.4]
  - idna [required: >=2.5,<2.9, installed: 2.8]
  - urllib3 [required: >=1.21.1,<1.26,!=1.25.1,!=1.25.0, installed: 1.25.3]
```

## Switch to a different python version

Given a situation if your app python version needs to be changed from one version to another pipenv `pipfile` can be edited to change the python version under:

```
[requires]
python_version = "3.6" ## changed from 3.7 to 3.6
```

And then by running the below will reinstall the virtual environment with the version specified.

`pipenv --python 3.6`

## To remove pipenv completely

You can remove the pipenv environment completely by running

`pipenv --rm`

This will still not delete the `Pipfile` and the `Pipfile.lock`, this would need to be manually removed (If not needed).

To install the pipenv with the pipfile`s in place, run:

`pipenv install`

## Changing version of a package installed

In order to update a pip package change the version under the pip file.

```
[packages]
openpyxl = "*"
requests = "==2.22.0" # Changed from 2.21 to 2.22
```

and then run:

`pipenv install`

Should result in the required version installed:

```
$ pipenv lock -r | grep requests
requests==2.22.0
```

## Production Ready

Once your application is ready with the required packages in development, You need to lock your environment to ensure you have the same (version) packages in production:

`pipenv lock`

This will create/update your `Pipfile.lock`, which you’ll never need to (and are never meant to) edit manually.

Once you get your code and `Pipfile.lock` in your production environment, you should install the last successful environment recorded by:

`pipenv install --ignore-pipfile`

This tells Pipenv to ignore the Pipfile for installation and use what’s in the Pipfile.lock.

## Dev Environment

To setup packages and environment for `dev` environment:

`pipenv install --dev`

## From legacy virtualenv to pipenv

If you have a dev-requirements.txt or something similar, you can add those to the Pipfile as well by:

`pipenv install -r dev-requirements.txt --dev`

Additionally, you can go the other way and generate requirements files from a `Pipfile`.

`pipenv lock -r > requirements.txt`
`pipenv lock -r -d > dev-requirements.txt`

## Resources to Refer

- [Five Myths About Pipenv](https://medium.com/@grassfedcode/five-myths-about-pipenv-698c5f198e4b)
- [Why you should use pyenv + Pipenv for your Python projects](https://hackernoon.com/reaching-python-development-nirvana-bb5692adf30c)
- [Configuring Pipenv in Visual Studio Code](https://olav.it/2017/03/04/pipenv-visual-studio-code/)
