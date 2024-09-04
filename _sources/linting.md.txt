# Static code analysis and linting
To enforce the style guide, configurations for `pylint`, `black` and `djlint` were provided. The configuration is located inside the
`pyproject.toml` file.
To start the analysis process a virtual environment needs to be created and the needed tools need to be installed:
```
    python -m venv venv
    pip install pylint, black, djlint, django
    source venv/bin/activate
```
After that the static code analysis can be started:
```
    cd webcentral/
    pylint src/
```
This will analyse the python files inside `webcentral/src/`.


