# directory-sso

This is the service for authenticating users for services that serve the Exporting is Great campaign for the Department for International Trade (DIT).

## Build status

[![CircleCI](https://circleci.com/gh/uktrade/directory-sso/tree/master.svg?style=svg)](https://circleci.com/gh/uktrade/directory-sso/tree/master)

## Coverage

[![codecov](https://codecov.io/gh/uktrade/directory-sso/branch/master/graph/badge.svg)](https://codecov.io/gh/uktrade/directory-sso)

## Requirements
[Docker >= 1.10](https://docs.docker.com/engine/installation/)

[Docker Compose >= 1.8](https://docs.docker.com/compose/install/)

## Local installation

    $ git clone https://github.com/uktrade/directory-sso
    $ cd directory-sso
    $ make

## Running with Docker
Requires all host environment variables to be set.

    $ make docker_run

### Run debug webserver in Docker
Provides defaults for all environment variables.

    $ make docker_debug

### Run tests in Docker

    $ make docker_test

### Host environment variables for docker-compose
``.env`` files will be automatically created with ``env_writer.py``, based on ``env.json`` and ``env-postgres.json``.

## Running locally without Docker

### Installing

```bash
$ git clone https://github.com/uktrade/directory-sso
$ cd directory-sso
$ virtualenv .venv -p python3.5
$ source .venv/bin/activate
$ pip install -r requirements_text.txt
```

### Running the webserver

```bash
$ source .venv/bin/activate
$ make debug_webserver
```

### Running the tests

```bash
$ make debug_test
```

## Debugging

### Setup debug environment
Requires locally running PostgreSQL (e.g. [Postgres.app](http://postgresapp.com/) for the Mac)

    $ make debug

### Run debug webserver

    $ make debug_webserver

### Run debug tests

    $ make debug_test

## Development data

For development efficiency a dummy user can be loaded into the database from `fixtures/development.json`. To do this run:

```bash
make loaddata
```

The credentials for the development user `dev@example.com`:`password`.

To update `fixtures/development.json` with the current contents of the database run:

```bash
make dumpdata
```

Then check the contents of `fixtures/development.json`.
