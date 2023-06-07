#!/usr/bin/env python3
import django_tables2 as tables
# from .models import Person


class ResultTable(tables.Table):
    """Class defines the table of the search results."""

    selection = tables.CheckBoxColumn(accessor="pk", orderable=False)
    name = tables.Column()
    surname = tables.Column()

    class Meta:
        """Meta data of the table for the search results."""

        template_name = "django_tables2/bootstrap.html"
