Intendation: Tabs, 1 Tab = 4 Whitespaces

* CamelCase, möglichst keine Zahlen, die nicht als Wort ausgeschrieben sind in den Identifiern (Variablen, Funktionen, Klassen)
* Konstanen: SNAKE_CASE in Großbuchstaben
* trailing_underscore\_ für Namen, die genauso heißen sollen wie Python-Keywords
* Identifier NUR in englischer Sprache: Generell gilt: Funktionalität immer in Englisch, Inhalt in deutscher Sprache. Auch Dateinamen sollen in englischer Sprache verfasst werden. Tabellenspalten oder ähnliches, welche in deutsch voliegen, müssen im docstring übersetzt und erklärt werden.
* Maximale Zeilenlänge 80 Zeichen
* Maximale Zeichenlänge für Docstrings 72 Zeichen
* Ein Leerzeichen vor und nach jedem Binäroperator (+, -, \*, /, =, <, >)
* Der Operator mit der niedrigsten Priorität sollte immer mit Leerzeichen umschlossen sein (`hypot2 = x*x + y*y`)
* Kein Leerzeichen vor Doppelpunkt, Komma, aber eins danach (`{eggs: 2}`)
* Keine Leerzeichen vor und nach Klammern
* Innerhalb der Parameterliste von Funktionsaufrufen sollte der = Operator nicht mit Leerzeichen umschlossen sein (`func(r=3, i=2)`)
* Bei mehrzeiligen Statements (Objektdefinitionen, Funktionsaufrufe oder -definitionen) soll ans Ende jeder Zeile ein Komma (redundante brackets und trailing commas) -> git version tracking
  * Beipiel git-version tracking:
    Durch das Trailing Komma wird der git diff Befehl lesbarer. Wird zu einer Liste ohne Trailing Komma ein Element hinzugefügt, zeigt git diff zwei geänderte Zeilen an. Mit Trailing Komma wird nur die hinzugefügte Zeile angezeigt:
    Zu `list` soll ein Element hinzugefügt werden:
    ```
      list = [
              'a',
              'b',
              'c'
              ]
    ```
    ```
          list = [
          'a',
          'b',
      +   'c',
      +   'd'
          ]

    ```
* Continuation Lines:
  * Continuation Lines, wenn 80 Zeichen überschritten und/oder mehr als 3 Funktionsparameter
  * Einrückung der Continuation Lines ein Tab hinter dem Tablevel der Zeile des Funktionsaufrufs/ Objektdefinition/ Funktionsdefinition
  * Die öffnende Klammer direkt hinter den Funktionsaufruf/ Objektdefinition/ Funktionsdefinition, die schließende Klammer in eine neue Zeile auf Tablevel der Zeile der öffnenden Klammer
  * kurze Funktionsaufrufe innerhalb der Continuation Lines bleiben einzeilig
  * Typenangabe von Funktionsparametern durch ( `func(argOne: str, argTwo: int)` )
* Sobald eine Rechnung mit Binäroperator die 80 Zeichen überschreitet, wird nach jedem Term vor dem Binäroperator in die nächste Zeile umgebrochen, dabei werden die weiteren Zeilen mit dem ersten Term der Rechnung aligned, und es werden redundante Klammern benutzt. Gibt es noch eine Klammer-Ebene, so wird diese, wenn möglich, einzeilig geschrieben:

  ```
    income = (grossWages
              + (dividens - qualifiedDividends)
              - iraDeduction)
  ```
* Imports:
  * Imports immer am Anfang jedes Moduls/ jeder Datei, neue Zeile für jede Bibliothek
  * Es sollten möglichst \* Importe vermieden werden, absolute Importe via:

    ```
    import os
    import sys
    ```
    * Ganze Bibliotheken sollten nur importiert werden, wenn man mehr als zehn Klassen oder Funktionen aus diesen verwendet.
  * Redundante Klammern und trailing commas bei Imports, wenn man mehrere Funktionen aus einem Modul importiert, Einrückung um einen Tab der Funktionsnamen:

  ```
  from fooLib import (
    foo1,
    foo2,
    foo3,
  )

  ```
  * Die Import-Sektion soll dreiteilig sein, zuerst die Standard-Bibliotheken, dann third-party-Bibliotheken und am Schluss lokale Bibliotheken und Funktionen.
* Klassen:
  * Objektorientier Code, Standardmäßig sollten alle Elemente einer Klasse private, sollte auf sie von außen zugegriffen werden müssen, so soll man den Property-Decorator (`@property`) nutzen. Private Elemente werden durch einen Double-Underscore gekennzeichnet:

  ```
  class Car:

    def __init__(self, brandName):
      self.__brandName = brandName

    @property:
    def brandName(self):
      return self.__brandName

  ```
* Dokumentation/Kommentare:
  * Es sollten Docstrings zur Dokumentation des Quelltextes verwendet werden. Jedes Modul (jede .py-Datei) sollte einen modulweiten Docstring verwenden.
  * Docstrings sind dreifache, doppelte Anführungszeichen
  * Jede weitere Definition erhält einen Docstring (Klassen und Funktionen)
  * Der Docstring besitzt die Numpy-Formatierung:
    * es wird ReStructuredText (rst) verwendet.
    * Der Docstring besteht aus Absätzen. Die Absätze sind durch eine Leerzeile getrennt.
    * der erste Absatz stellt eine einzeilige Zusammenfassung der Funktionalität dar.
    * der zweite Absatz stellt eine ausführliche Beschreibung dar.
    * dritter Absatz: Parameter:

    ```
      ParameterName : ParameterTyp
        Beschreibung des Parameters






    ```
    * vierter Absatz: Rückgabewerte

    ```
      type
        Beschreibung






    ```
    * Fünfter Absatz: Relevante Literatur
    * Sechster Absatz: Beispiele

  ```
    def foo(var1, var2, *args, long_var_name="hi", only_seldom_used_keyword=0, **kwargs):
      r"""Summarize the function in one line.

      Several sentences providing an extended description. Refer to
      variables using back-ticks, e.g. `var`.

      Parameters
      ----------
      var1 : array_like
          Array_like means all those objects -- lists, nested lists, etc. --
          that can be converted to an array.  We can also refer to
          variables like `var1`.
      var2 : int
          The type above can either refer to an actual Python type
          (e.g. ``int``), or describe the type of the variable in more
          detail, e.g. ``(N,) ndarray`` or ``array_like``.
      *args : iterable
          Other arguments.
      long_var_name : {'hi', 'ho'}, optional
          Choices in brackets, default first when optional.

      Returns
      -------
      type
          Explanation of anonymous return value of type ``type``.
      describe : type
          Explanation of return value named `describe`.
      out : type
          Explanation of `out`.
      type_without_description

      References
      ----------
      Cite the relevant literature, e.g. [1]_.  You may also cite these
      references in the notes section above.

      .. [1] O. McNoleg, "The integration of GIS, remote sensing,
         expert systems and adaptive co-kriging for environmental habitat
         modelling of the Highland Haggis using object-oriented, fuzzy-logic
         and neural-network techniques," Computers & Geosciences, vol. 22,
         pp. 585-588, 1996.

      Examples
      --------
      These are written in doctest format, and should illustrate how to
      use the function.

      >>> a = [1, 2, 3]
      >>> print([x + 3 for x in a])
      [4, 5, 6]
      >>> print("a\nb")
      a
      b






  ```
  * Sphinx ist ein Tool um gut lesbare Dokumentation zu erstellen.
  * Sphinx erstellt zunächst eine Ordnerstruktur mit Quelltextdateien, diese Dateien sind per Default reStructuredText-Dateien (.rst), es kann aber auch auf Markdown, Python-Source Files, Jupyter-Notebooks uvm. umgestellt werden. Dies kann mit (`sphinx-quickstart docs`) durchgeführt werden. Dabei gibt der erste Parameter den Pfad zum Ordner an, indem die Dokumentations-Quelltexte erstellt werden sollen. Hier Unterordner (`docs`) des momentanen Verzeichnisses.
  * in (`docs/source`) sind die .rst-Dateien gespeichert. Unter anderem die (`index.rst`) ist die basisdatei für die spätere Main-Seite.
  * (`conf.py`) ist die Konfiguration des Sphinx-Projekts. Hier werden auch Paket-Abhängigkeiten spezifiziert.
  * Mit dem Befehl (`make html`) wird ein HTML-Dokument aus den Quelltexten erstellt. Sie liegen in (`build`)
  * es kann auf einfache Weise eine API-Dokumentation erstellt werden, dazu müssen zwei Dateien angepasst werden:
  * In die (`conf.py`):

  ```
    extensions = [ 'sphinx.ext.autodoc',
               ]






  ```

  Mithilfe dieses Pakets kann aus den Docstrings eine API-Dokumentation erstellt werden.
  * es wird eine neue Quelltextdatei mit dem Namen (`apidoc.rst`) erstellt. Diese erhält den folgenden Inhalt:

  ```
    API Documentation
    =================

    .. automodule:: pythonDateiName
       :members:






  ```

  Dabei müssen alle Python-Dateien angegeben werden, aus denen die Docstring-Information extrahiert werden soll.
  * in der (`index.rst`) muss auf die neue Quelletextdatei referenziert werden. Dies ist durch Angabe des Namens der Quelltextdatei möglich. Es wird in einer neuen Zeile an die (`index.rst`) das Folgende angehängt:

  ```
      apidoc






  ```
  * nach erneutem Build-Prozess sollte die API-Dokumentation als HTML gerendert worden sein.
  * Die Examples können per doctest-Modul getestet werden. Dazu muss ein weiteres Modul zu den Extensions in der (`conf.py`) hinzugefügt werden:

  ```
    extensions = [ 'sphinx.ext.autodoc',
                  'sphinx.ext.doctest',
                  ]






  ```
  * es kann nun die korrekte Ausgabe der Beispiele überprüft werden

  ```
    make doctest






  ```
