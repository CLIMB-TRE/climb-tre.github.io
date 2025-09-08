# climb-tre.github.io

## Overview

This repo hosts the source from which the CLIMB-TRE website (https://climb-tre.github.io/) is generated. The pages are built using the [Material theme](https://squidfunk.github.io/mkdocs-material/) for [MkDocs](https://www.mkdocs.org/), with some additional plugins.

## How to edit these pages

Clone the repository:

```
$ git clone https://github.com/CLIMB-TRE/climb-tre.github.io.git
$ cd climb-tre.github.io/
```

From here, create a Python virtual environment and install the dependencies:

```
$ python -m venv .venv
$ source .venv/bin/activate
$ pip install -r requirements.txt
```

Then, we can run the pages locally with:

```
$ mkdocs serve
```

And the site will be available at `http://127.0.0.1:8000/`.

The documentation itself is written in [Markdown](https://www.markdownguide.org/) files in the `docs` folder.  The site configuration is in `mkdocs.yml` (in [YAML](https://yaml.org/) format) in the top-level directory. Don't forget to add new pages to the `nav` section of `mkdocs.yml`.

The GitHub action will deploy changes made to the `main` branch.
