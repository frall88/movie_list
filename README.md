# movie_list
Task for showing movies and people appeared there.

Installation
-------
    # Create virtualenv
    export VENV_DIR=venv
    python3.7 -m venv "${VENV_DIR}"
    "${VENV_DIR}"/bin/python3.7 -m ensurepip --upgrade
    "${VENV_DIR}"/bin/pip install pip-tools
    "${VENV_DIR}"/bin/python3.7 -m pip install -e .

Running
-------
    . venv/bin/activate
    python manage.py runserver -h 0.0.0.0 -p 8000


Unit tests
----------
You can run unit tests and different analyzers this way:

    # While being in virtualenv (see 'installation' above')
    pip install -e .[test,dev]
    py.test
    pylint service_api