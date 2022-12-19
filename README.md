# be-restaurant-playlists

Sleigh-ers final project backend repo

Team Members
A, M, C, Y

An app for Foodies

=> Make eat-lists of all the food places on your radar
=> Find inspiration from other users eat-lists

# Installation Process:

Install the virtual environment for Python (venv)
`python3 -m venv venv`
`. venv/bin/activate`

Use this command to install the required packages
`python -m pip install -r requirements.txt`

Confirm that Flask and psychopg2 are installed

# New Packages

When installing new Packages create a requirements file by running this command
`python -m pip freeze > requirements.txt`

# Seeding database

To create the database run the following command in the terminal ensuring you are in the repo directory:
`psql -f ./db/setup.sql`

# Query tester
To test a query run the following command in the root dir of the repo:
`psql -f db/query-tester.sql > db/output.txt`
