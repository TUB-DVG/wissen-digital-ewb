HowTo: Insert links in database texts
-------------------------------------

Sometimes it is needed to show links in content, which comes from the database. To make this possible it
is needed to encode the link in the text. This is done by using the Django template language (DTL) inside the database content:
```
    Gegebenenfalls an die Beobachtung anschließendes Interview mit der beobachteten Person, um beobachtetes Verhalten besser zu verstehen (zur Methode von Interviews siehe <a href=“{% url ‚userEngagementDetailsTitle‘ ‚Einzel-Interview‘  %})“>Einzel-Interview</a>
```
The shown text holds a DTL-string with the template tag "url", which renderes the path based on the provided name. As a argument the name of the details page, which should be linked to, is given.
In the models, the following property-method is created (like a getter-function in java):
```
    @property
    def procedureItem(self):
        """This method should be called, when the procedureItem attribute of a
        object of type ProcedureItem is called. It renders the text inside the
        object as a django-template.

        """
        template = Template(self._procedureItem)
        context = Context({})
        return template.render(context)
```
This method is called, when on a object of tyle `ProcedureItem` the procedureItem-attribute is accessed.
It instanciates the django-template-class, with the string, which should be rendered and calls the render()-method on it,
which renders the provided DTL-tags as template. In the end the rendered string is returned. 