Sitemap urls auditor
====================

[![CI](https://github.com/alena-kono/sitemap-urls-auditor/actions/workflows/ci.yml/badge.svg)](https://github.com/alena-kono/sitemap-urls-auditor/actions/workflows/ci.yml)
[![wemake-python-styleguide](https://img.shields.io/badge/style-wemake-000000.svg)](https://github.com/wemake-services/wemake-python-styleguide)
[![Maintainability](https://api.codeclimate.com/v1/badges/359f2d6b85523379f24e/maintainability)](https://codeclimate.com/github/alena-kono/sitemap-urls-auditor/maintainability)

**WARNING!** Not production ready! (I'm pretty sure it's quite obvious fact :) )

At the moment, this project is at MVP stage.

Purpose
-------

This simple CLI-tool is used to check and display status codes of each URL of any website.

Prerequisites
-------------

As a product & project manager in a small team, I need to check our website’s “health”.
“Health” in terms of product mgmt and SEO means that every URL presented in sitemap.xml responds to the request with 200 code.

I don’t want to check this manually.

I just want my product to be healthy and wealthy.

Features
--------
- This CLI tool accepts only one argument (URL) and one option (--filename).
- Can output result only to default pager or .json file.
- `--help` option is also available.
- Based on great `typer` [library](https://typer.tiangolo.com) by [*tiangolo*](https://github.com/tiangolo).
- `poetry` for managing dependencies.
- `mypy` for static typing.
- Uses `wemake-python-styleguide` for linting (IT WAS FUN!).
- `github-actions` as CI tool.

How it works
------------
1. Sitemap-urls-parser finds and fetches `sitemap.xml` for given website.
2. Extracts all urls from `sitemap.xml`.
3. Sends requests to each url and saves response status codes.

Requirements & Installation
---------------------------

Developed and runs on `python 3.9`.

1. Clone this project to your local machine

        $ git clone https://github.com/alena-kono/sitemap-urls-auditor.git

        $ cd sitemap-urls-auditor/

2. Install necessary dependencies

        $ poetry install

3. Activate poetry virtual environment shell:

        $ poetry shell

How to use
----------
- For example, we want to check urls of `typer` website. For that we'll need only its homepage url which is https://typer.tiangolo.com. To run tool and print result via the default pager:

        $ sitemap-urls-auditor https://typer.tiangolo.com

    Result example:

        $
        {
            "200": [
                "https://typer.tiangolo.com/",
                "https://typer.tiangolo.com/alternatives/",
                "https://typer.tiangolo.com/contributing/",
                "https://typer.tiangolo.com/features/",
                ...,
            ],
        }

- Or we can add `--filename` option and pass a filename argument to save our result to .json.

        $ sitemap-urls-auditor https://typer.tiangolo.com --filename output_typer_urls.json

- For help run:

        $ sitemap-urls-auditor --help

List of improvements
--------------------
◻️ Add tests.

✅️ Make human readable alias for `poetry run python sitemap_urls_auditor/cli/cmd_handlers.py URL`.

◻️ Implement option `--summary` which outputs pivot information about urls' statuses (Develop command handler, two methods are already implemented - [here](https://github.com/alena-kono/sitemap-urls-auditor/blob/16af6f736881999998f778f1bed8160b8b42aef6/sitemap_urls_auditor/sitemap/url_collection.py#L107) and [here](https://github.com/alena-kono/sitemap-urls-auditor/blob/16af6f736881999998f778f1bed8160b8b42aef6/sitemap_urls_auditor/sitemap/url_collection.py#L130)).

◻️ Implement progress bar.

◻️ Add .csv to supported output formats.
