# be-restaurant-playlists

Sleigh-ers final project backend repo

Team Members
Y, M, C, A

An app for Foodies

- Make eat-lists of all the food places on your radar
- Find inspiration from other users eat-lists

## Installation Process

Install the virtual environment for Python (venv):

```shell
python3 -m venv venv
. venv/bin/activate
```

Use this command to install the required packages

```shell
python -m pip install -r requirements.txt
```

Confirm that `Flask` and `psycopg2` are installed.

## New Packages

When installing new packages, update the requirements file by running this command

```shell
python -m pip freeze > requirements.txt
```

## Setting environment variables

Create two `.env` files: `.env.test` and `.env.development`.

The `.development` file should contain only `PG_DATABASE=restaurant_playlists`, while `.test` should contain `PG_DATABASE=restaurant_playlists_test`

## Seeding the database

To create the database, run the following command in the terminal, ensuring you are in the repo's root directory:

```shell
psql -f ./db/setup.sql
```

## Testing db queries

To test a database query, run the following command in the root dir of the repo:

```shell
psql -f db/query-tester.sql > db/output.txt
```

This will put any query outputs into the text document.

## PyTest Notes

`assert x == expect, "print this if it fails"`

The following line is a replacement of the (`.test`) in JS:

```python
def test_file1_method1():
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
https://www.guru99.com/pytest-tutorial.html#4
