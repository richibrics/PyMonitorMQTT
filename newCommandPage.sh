#!/bin/bash

cp docs/commands/template_page.md docs/commands/$1.md
mkdir docs/_includes/data/commands/$1
mkdir docs/_includes/data/commands/$1/example
mkdir docs/_includes/data/commands/$1/extra
