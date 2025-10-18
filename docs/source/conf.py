# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

import fitstoolz
from datetime import date

author = 'Sphesihle Makhathini'
maintainer = 'Mika Naidoo, Athanesus Ramaila'
project = 'simms'
copyright = f'{date.today().year}, {author}'

release = fitstoolz.__version__
version = fitstoolz.__version__

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

language = 'en'

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
#    'sphinx_rtd_theme',
]

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

html_theme = 'classic'

