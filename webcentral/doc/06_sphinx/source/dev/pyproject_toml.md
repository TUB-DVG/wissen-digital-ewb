# pyproject.toml

In this section you will understand howto use and configure the pyproject.toml.
Therfore we also add some general information about this file. More information
you will find in the following links:
- https://packaging.python.org/en/latest/guides/writing-pyproject-toml/
- tutorials:
  - https://betterprogramming.pub/a-pyproject-toml-developers-cheat-sheet-5782801fb3ed
  - https://www.youtube.com/watch?v=QMY-OkckDwo

## general inforamtion about our pyproject.toml

The file pyproject.toml is a general config file for python projects. Based on
this config file you can build python packages with packaging tools, like
setupTool, poetry, Flit or so on. It is a replacement of the former config files
setup.py/setup.cgf.

It is defined in PEP 518, PEP 517, PEP 621, PEP 660, PEP 725 and PEP 735.

By the pyproject.toml things like, can be defined:
- python dependencies
- code linter, like pylint
- code formater, like black
- python tests
- ...

It is a toml-file, obviously (see [https://toml.io/en/](https://toml.io/en/)).

## howto use the pyproject.toml

### local installation for development

Creating editable installation of our project:

```shell
pip install -e '.[dev]'
```

For the general installation see [project install](InstalltionBasic).


### general structure of our pyproject.toml

In this section the structure of our pyproject.toml file will be explained.
Therfore the functions of the parts (not complete) of the file will be commented.


#### build system
The table build-system defines the tool for python packaging. In this case the
package tool "setuptools" is setup. It can easily change to other tools, like
poetry.

```toml
[build-system]
requires = ["setuptools", "setuptools-scm"]
build-backend = "setuptools.build_meta"

```

#### project information
The table project includes information and the overall needed dependencies.
Here "name" and "version" always needed to be setup.
```toml
[project]
name = 'wissenplattEWB'
version = '0.1'
authors = [
    {name = "name surname"},
]
description = "WenDE - Wissensplattform: is a platform providing knowledge about tool and data for the researcher community of the EnergieWendeBauen."
...
]
dependencies = [
    "channels==XXXX",
...
]

```
#### directory structure specific setup
The following code lines are needed to specify the root of the program code.
```toml
# root folder of the python/django not found automatically
[tool.setuptools.packages.find]
where = ["01_application"]
#include = ["pkg*"]  # alternatively: `exclude = ["additional*"]`
namespaces = false
```

#### specific dependencies
It is possible to setup specific dependencies for specific tasks, like develop
or test the program code.

```toml
[project.optional-dependencies]
dev = [
    "pylint",
...
]
test = [
    "coverage[toml] ==XXXX",
...
]
```

#### code style
The following code blocks include definitions for the code style of our project.
Here the definitions for the linter pylint and the formater black are set up.

```toml
[tool.pylint.format] max-line-length = 80

[tool.pylint.basic]
variable-naming-style = "camelCase"
function-naming-style = "camelCase"

[tool.djlint]
profile = "django"
indent = 2
max_line_length=80
max_blank_lines=1
close_void_tags=true
include="H017"

[tool.black]
line-length = 80

```
