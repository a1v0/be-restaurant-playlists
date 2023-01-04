# Munchify Backend API

## Summary

||||
|-|-|-|
|**Hosted URL**|:|tbc|
|**Minimum Python version**|:|3.8.10|
|**Minimum PostgreSQL version**|:|12.12|

This API is the backend for our Munchify website for restaurant playlists. It's a collaboration between `yos244`, `moshkh`, `Cnmoosavinia` and `a1v0`, aka YMCA.

The API's database includes tables of playlists, restaurants, users and votes.

## Installation Process

After you have cloned the repo from GitHub, install the virtual environment for Python (`venv`):

```bash
python3 -m venv venv # installs venv
. venv/bin/activate # activates the venv
```

Use this command to install the required packages:

```shell
python -m pip install -r requirements.txt
```

Confirm that `Flask` and `psycopg2` are installed, by running:

```shell
pip show psycopg2-binary
flask --version
```

### Installing New Packages

If installing new packages, update the requirements file by running this command:

```shell
python -m pip freeze > requirements.txt
```

## Seeding the database

### Setting environment variables

Create two `.env` files: `.env.test` and `.env.development`.

The `.development` file should contain only `PG_DATABASE=restaurant_playlists`, while `.test` should contain `PG_DATABASE=restaurant_playlists_test`

### Creating the database

To create the database, run the following command in the terminal, ensuring you are in the repo's root directory:

```shell
psql -f ./db/setup.sql
```

### Seeding the dev data

The test data will be seeded automatically by PyTest, but you will need to seed the dev data yourself. Do this using:

```shell
PYTHONPATH=$(pwd) python db/run-seed.py
```

### Testing db queries

To test a database query in isolation, write your query in `db/query-tester.sql` and run the following command in the root dir of the repo:

```shell
psql -f db/query-tester.sql > db/output.txt
```

This will put any query outputs into `db/output.txt`.

## Useful Flask Commands

### Run flask with auto-refresh

Use this command when running the flask app to enable auto-refresh of any changes to the code

```shell
flask --app <example_app.py> --debug run
```

## PyTest

### Running a test

To run a test, you must be in the root directory and you must use this command:

```shell
PYTHONPATH=$(pwd) py.test <optional keyword searches with -k -v>
```

PyTest by default has access only to its own directory. The command above allows it access to all files in the root.

### Preparing a test

The following line is a replacement of the (`.test`) in JS:

```python
def test_file1_method1():
    assert x == expect, "print this if it fails"
```

Use snake case when naming Python files.

By default pytest only identifies the file names starting with `test_` or ending with `_test`

- `test_login.py` - valid
- `login_test.py` - valid
- `testlogin.py` - invalid
- `logintest.py` - invalid

The python version of `.only` is a keyword search

- `py.test -k <file_name> -v`
- `py.test -k method1 -v` (in this case it will search any test containing `method1`)

To replace a describe block in pytest, use:

```python
import pytest
@pytest.mark.set1
def test_file2_method1():
    x = 5
    y = 6
    assert x + 1 == y, "test failed"
    assert x == y, "test failed because x=" + str(x) + " y=" + str(y)

@pytest.mark.set1
def test_file2_method2():
    x=5
    y=6
    assert x+1 == y,"test failed"
```

Run `py.test -m set1`. This will run the methods `test_file1_method1`, `test_file2_method1`, `test_file2_method2`.

### One test with multiple arguments

```python
@pytest.mark.parametrize("input1, input2, output", [(5, 5, 10), (3, 5, 12)])
def test_add(input1, input2, output):
    assert input1 + input2 == output, "failed"
```

### Skipping a test

(Equivalent to adding `.skip`.)

```python
import pytest
@pytest.mark.skip
def test_add_1():
    assert 100 + 200 == 400, "failed"
```

### Pytest Framework Testing an API

`conftest.py` – have a fixture which will supply base url for all the test methods

```python
import pytest
@pytest.fixture
def supply_url():
    return "https://reqres.in/api"
```

Check out this link for further details:
<https://www.guru99.com/pytest-tutorial.html#4>
