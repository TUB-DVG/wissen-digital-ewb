# Static code analysis
- [Prerequisites](#prerequisites)
- [Linters](#linters)
  - [Pylint (.py)](#linters-python)
  - [djLint (.html)](#linters-django)
  - [ESLint (.js)](#linters-javascript)
- [Formatters](#formatters)
  - [Black (.py)](#formatters-python)
  - [djLint (.html)](#formatters-django)
  - [ESLint (.js)](#formatters-javascript)

Here you can find how to setup linters and formatters that are used in this codebase.

All required dotfiles should be already included inside this directory. If not, please follow the steps below.

<a id="prerequisites"></a>
## Prerequisites
- [node](https://nodejs.org/en)
- [python](https://www.python.org/) and [pip](https://pip.pypa.io/en/stable/)

Please refer to the installation process according to your operating system.

<a id="linters"></a>
## Linters
<a id="linters-python"></a>
### Pylint (.py)
We use **Pylint** to help with static code analysis. It provides a sensible out of the box configuration without the need to manually configure. However, custom rules can be easily added. You can find the full documentation [here](https://pylint.readthedocs.io/en/stable/).

#### Setup
1. Download and install Pylint `pip install pylint`.
2. Create a new file in your project root directory called `pyproject.toml`.
3. Add this following rule:
```
[tool.pylint.format]
max-line-length = 80
```
4. Lint a file: `pylint path/to/file.py`.
    
    4.1 Or a directory: `pylint path/to/directory`.
5. _Visual Studio Code users_: Download [Pylint](https://marketplace.visualstudio.com/items?itemName=ms-python.pylint) extension to see hints and warning as you type. Additionally, add these following lines inside your VS Code's `settings.json`:
```
"pylint.path": [
    "pylint"
],
```
Now you should have a fully functional Pylint experience.

<a id="linters-django"></a>
### djLint (.html)
We use **djLint** to help with linting (and later formatting) our Django template files. It also provides good out of the box experience without any complications. You can find the full documentation [here](https://www.djlint.com/).

#### Setup
1. Download and install djLint `pip install djlint`.
2. Create a new (or add to an existing) file in your project root directory called `pyproject.toml`.
3. Add these following rules:
```
[tool.djlint]
profile = "django"
indent = 2
max_line_length=80
max_blank_lines=1
close_void_tags=true
include="H017"
```
4. Lint a file: `djlint path/to/template.html --lint`.

    4.1 Or a directory: `djlint path/to/directory --lint`.
5. _Visual Studio Code users_: Download [djLint](https://marketplace.visualstudio.com/items?itemName=monosans.djlint) extension to see hints and warning as you type. 

Now you should have a fully functional djLint experience.

<a id="linters-javascript"></a>
### ESLint (.js)
We use **ESLint** to lint our JavaScript code. It is the standard tool. You can find the full documentation [here](https://eslint.org/).

#### Setup
1. Download and install ESLint `npm install eslint --global`.

_Note:_ `--global` flag is generally not recommended. However, as this is mainly a Django project without Node.js, we'll install ESLint globally.

2. Create a new file in your project root directory called `.eslintrc.js`.
3. Add these following lines:
```
module.exports = {
  "env": {
    "browser": true,
    "es2021": true
  },
  "extends": "eslint:recommended",
  "parserOptions": {
    "ecmaVersion": "latest",
    "sourceType": "module"
  },
  "rules": {
    "semi": [1, "always"],
    "quotes": [1, "double"]
  }
};

```
4. Lint a file: `npx eslint path/to/file.js`.
    
    4.1 Or a directory: `npx eslint path/to/directory`.
5. _Visual Studio Code users_: Download [ESLint](https://marketplace.visualstudio.com/items?itemName=dbaeumer.vscode-eslint) extension to see hints and warning as you type.

Now you should have a fully functional ESLint experience.

<a id="formatters"></a>
## Formatters
<a id="formatters-python"></a>
### Black (.py)
We use **Black** as our main formatter for all our Python files. It is a very opinionated tool which tries to provide a universal coding style. It is advised not to change the default configuration (the options to change them are limited anyways). You can find the full documentation [here](https://black.readthedocs.io/en/stable/).

#### Setup
1. Download and install Black `pip install black`.
2. Create a new (or add to an existing) file in your project root directory called `pyproject.toml`.
3. Add this following rule:
```
[tool.black]
line-length = 80
```
4. Format a file: `black path/to/file.py`.

    4.1 Or a directory: `black path/to/directory`.
5. _Visual Studio Code users_: Download [Black](https://marketplace.visualstudio.com/items?itemName=ms-python.black-formatter) extension to use as a default formatter (and take advantage of the format keyboard shortcut). Additionally, add these following lines inside your `settings.json`:
```
"[python]": {
    "editor.defaultFormatter": "ms-python.black-formatter"
},
"black-formatter.path": [
    "black"
],
```

Now you should have a fully functional Black formatter.

<a id="formatters-django"></a>
### djLint (.html)
We use **djLint** again to help with formatting our Django template files. The advantage is the usage of our existing linter rules and enforcing them through its formatter functionality. You can find the full documentation [here](https://www.djlint.com/).

#### Setup
_Skip steps 1, 2 and 3 if you have previously installed and setup djLint._
1. Download and install djLint `pip install djlint`.
2. Create a new (or add to an existing) file in your project root directory called `pyproject.toml`.
3. Add these following rules:
```
[tool.djlint]
profile = "django"
indent = 2
max_line_length=80
max_blank_lines=1
close_void_tags=true
include="H017"
```
4. Format a file: `djlint path/to/template.html --reformat`.

    4.1 Or a directory: `djlint path/to/directory --reformat`.
5. _Visual Studio Code users_: Download [djLint](https://marketplace.visualstudio.com/items?itemName=monosans.djlint) extension to use as a default formatter (and take advantage of the format keyboard shortcut). Additionally, add these following lines inside your `settings.json`:
```
"[html]": {
    "editor.defaultFormatter": "monosans.djlint"
},
"djlint.useEditorIndentation": false,
```

Now you should have a fully functional djLint formatter.

<a id="formatters-javascript"></a>
### ESLint (.js)
We use **ESLint** again as similarly to djLint it already provides a formatting functionality out of the box. There is no need to install additional formatters in this case. You can find the full documentation [here](https://eslint.org/).

#### Setup
_Skip steps 1, 2 and 3 if you have previously installed and setup ESLint._

1. Download and install ESLint `npm install eslint --global`.

_Note:_ `--global` flag is generally not recommended. However, as this is mainly a Django project without Node.js, we'll install ESLint globally.

2. Create a new file in your project root directory called `.eslintrc.js`.
3. Add these following lines:
```
module.exports = {
  "env": {
    "browser": true,
    "es2021": true
  },
  "extends": "eslint:recommended",
  "parserOptions": {
    "ecmaVersion": "latest",
    "sourceType": "module"
  },
  "rules": {
    "semi": [1, "always"],
    "quotes": [1, "double"]
  }
};

```
4. Format a file: `npx eslint --fix path/to/file.js`.
    
    4.1 Or a directory: `npx eslint --fix path/to/directory`.
5. _Visual Studio Code users_: Download [ESLint](https://marketplace.visualstudio.com/items?itemName=dbaeumer.vscode-eslint) extension to use as a default formatter (and take advantage of the format keyboard shortcut). Additionally, add these following lines inside your `settings.json`:
```
"eslint.format.enable": true,
"[javascript]": {
    "editor.defaultFormatter": "dbaeumer.vscode-eslint"
},
```

Now you should have a fully functional ESLint formatter.
