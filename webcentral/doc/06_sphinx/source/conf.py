# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

import sys
import os

project = "webcentral"
copyright = "2023, DVG"
author = "DVG"
release = "0.0.1"

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration


# )
# sys.path.append(
#     "/home/tobias/Aufgaben/07_dockerWithDB/webcentral/01_application/webcentral_app/webcentral_app/",
# )
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "webcentral_app.settings")
# from django.conf import settings
# import django
#
# django.setup()
extensions = [
    # "sphinx.ext.autodoc",
    "myst_parser",
    "sphinxcontrib.mermaid",
    "sphinx.ext.napoleon",
    "sphinx.ext.githubpages",
]

templates_path = ["_templates"]
exclude_patterns = []

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "alabaster"
html_static_path = ["_static"]
