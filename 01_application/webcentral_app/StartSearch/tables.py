#!/usr/bin/env python3
import django_tables2 as tables
# from .models import Person


class ResultTable(tables.Table):
    selection = tables.CheckBoxColumn(accessor="pk", orderable=False)
    name = tables.Column()
    surname = tables.Column()

    class Meta:
        template_name = "django_tables2/bootstrap.html"
