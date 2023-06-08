#!/usr/bin/env python3
import django_tables2 as tables
import itertools


class ResultTable(tables.Table):
    """Class defines the table of the search results."""

    row_number = tables.Column(empty_values=(), verbose_name="Nr.:")
    name = tables.Column(verbose_name="Name")
    kindOfItem = tables.Column(verbose_name="Art des Ergebnisses")

    class Meta:
        """Meta data of the table for the search results."""

        template_name = "django_tables2/bootstrap.html"

    def __init__(self, *args, **kwargs):
        """Initialisation for the row counter of the table."""
        super().__init__(*args, **kwargs)
        self.counter = itertools.count()

    def render_row_number(self):
        """Render of the row counter of the table."""
        return f"{next(self.counter) +1 }"
