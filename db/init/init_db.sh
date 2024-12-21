#!/bin/bash

# Create the database if it does not exist
psql -U "$POSTGRES_USER" -h "$DATABASE_HOST" -c "SELECT 'CREATE DATABASE $POSTGRES_DB' WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = '$POSTGRES_DB') LIMIT 1;" > /dev/null 2>&1

# Create the user if it does not exist
psql -U "$POSTGRES_USER" -h "$DATABASE_HOST" -c "DO \$\$ BEGIN IF NOT EXISTS (SELECT 1 FROM pg_roles WHERE rolname = '$POSTGRES_USER') THEN CREATE USER $POSTGRES_USER WITH ENCRYPTED PASSWORD '$POSTGRES_PASSWORD'; END IF; END \$\$;" > /dev/null 2>&1

# Grant all privileges on the database to the user
psql -U "$POSTGRES_USER" -h "$DATABASE_HOST" -c "GRANT ALL PRIVILEGES ON DATABASE $POSTGRES_DB TO $POSTGRES_USER;"


# Replace placeholders with actual environment variables and run the SQL commands
#psql -U "$POSTGRES_USER" -h "$DATABASE_HOST" -c "CREATE DATABASE $POSTGRES_DB;"
#psql -U "$POSTGRES_USER" -h "$DATABASE_HOST" -c "CREATE USER '$POSTGRES_USER' WITH ENCRYPTED PASSWORD '$POSTGRES_PASSWORD';"
#psql -U "$POSTGRES_USER" -h "$DATABASE_HOST" -c "GRANT ALL PRIVILEGES ON DATABASE $POSTGRES_DB TO '$POSTGRES_USER';"
