# Simple ELT 🧙

A script that reads data from local files and ingests the data into a database.

## Using the script

The following command will generate a virtual environment and run the python script.

```
poetry run python src/cli.py \
    --postgres-user "name" \
    --postgres-password "password" \
    --postgres-host "host" \
    --postgres-port "port" \
    --postgres-database "database" \
    --postgres-schema "schema" \
    --data-directory "path/to/directory"
```

As an alternative to using command line options, the same options can be set as environment variables with the `LOAD_` prefix. See the following example:

```
export LOAD_POSTGRES_USER="name"
export LOAD_POSTGRES_PASSWORD="password"
export LOAD_POSTGRES_HOST="host"
export LOAD_POSTGRES_PORT="port"
export LOAD_POSTGRES_DATABASE="database"
export LOAD_POSTGRES_SCHEMA="schema"
export LOAD_DATA_DIRECTORY="path/to/directory"
```