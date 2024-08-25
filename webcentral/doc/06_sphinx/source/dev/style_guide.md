# Style Guide
The following section describes the style guide, which is used throughout the project. It is structured by the different languages used.
## Python
In this section the code style in the python source code is described. 
- Indentation:
  - 1 Tab or 4 Whitespaces
- Naming of identifiers:
  - camelCase for variables, functions and methods, numbers should be written out as characters
  - Classes should be named in PascalCase
  - Constants SNAKE_CASE in upper letters
  - general: 
    - trailing underscore for names, which have the same naming like Python-Keywords
    - identifier and filenames in english language 
    - content is written in german. German identifiers should be translated in the docstring
- Maximum line-length is 80 characters
- Maximum line-length in docstring is 72 characters
- Generally one space before and after an binary operator (+, -, *, /, <, >, ...)
  - an exception of that rule are nestings of binary operators. E.g. `hypo = x*x + y*y`. Only the operators with lowest priority should have a space before and after the binary operator.
- no space before a double dot, comma, ... e.g. `{"numberOfStudents": 2}`
- no space before and after brackets
- no spaces for default values in parameter list: `func(r=3, i=2)`
- for statements going over multiple lines redundant brackets and a trailing comma should be set:
```
list = [
  'a',
  'b',
  'c',
]
```
- Continuation lines:
  - if line exeeds the 80 characters limit or if more than 3 function parameters are used
  - indentation one tab after the tab-level of the line below
  - opening bracket behind function call/definition
  - closing bracket onto new line on tablevel of function-call line
  - return-type and types of parameters should be specified `func(argOne: str, argTwo: inf) -> str`
- if binary operation exceeds the 80 character linelength a line break is added. The linebreak is added before the binary-operator:
```
  income = (grossWages
            + (dividends - qualifiedDividends)
            - iraDeduction)
```
- Imports:
  - only at the start of a module
  - no * imports
  - whole libraries should only be imported if more than 10 classes/functions are used
  - redundant brackets are used, when multiple elements are imported e.g.
```
  from foolib import (
    foo1,
    foo2,
  )
```
- the import-section should be split into 3 parts: First the python standard-libraries are imported, then third-party-libraries and then self-written modules at the end. Each section is separated by a blank line.
- classes: 
  - all attributes should be private/protected.
    - when an attribute is used outside the object an getter-function, with the `property`-decorator should be written
```
class car:
  
  def __init__(self, brandName):
    self.__brandName = brandName
  
  @property
  def brandName(self):
    return self.__brandName

```
- Documentation/Comments
  - docstrings should be used for documentation
  - each module should have a docstring which is surrounded by three double quotation marks
  - each definition has another docstring (methods/functions, classes)
  - numpy-formatting should be used:
    - docstring is composed of paragraphs. Each paragraph is separated by an empty line
    - first line is a one-line summary of the functionality
    - second line is a detailed description 
    - third paragraph holds the description of the parameters
    ```
      parameterName:  parameterTyp
        Description of the parameter
    ```
    - 4. paragraph return-values:
    ```
      type
        description
    ```
    - 5. paragraph: literature
    - 6 paragraph: Examples
