# cmem-plugin-irdi

Create unique International Registration Data Identifier (IRDI).

[![eccenca Corporate Memory][cmem-shield]][cmem-link][![workflow](https://github.com/eccenca/cmem-plugin-irdi/actions/workflows/check.yml/badge.svg)](https://github.com/eccenca/cmem-plugin-irdi/actions) [![pypi version](https://img.shields.io/pypi/v/cmem-plugin-irdi)](https://pypi.org/project/cmem-plugin-irdi) [![license](https://img.shields.io/pypi/l/cmem-plugin-irdi)](https://pypi.org/project/cmem-plugin-irdi)
[![poetry][poetry-shield]][poetry-link] [![ruff][ruff-shield]][ruff-link] [![mypy][mypy-shield]][mypy-link] [![copier][copier-shield]][copier] 

## Development

- Run [task](https://taskfile.dev/) to see all major development tasks.
- Use [pre-commit](https://pre-commit.com/) to avoid errors before commit.
- This repository was created with [this copier template](https://github.com/eccenca/cmem-plugin-template).

## Plugin Usage

- All fields of the IRDI are configurable, minus `Item Code`, which is created by the plugin
  - Created IRDIs are unique per configuration
- Specify a graph that stores the state of `Item Codes`
- Input and output paths are configurable
  - if no input path is configured, values are read from the URIs of the input (Transformation Input) 

[cmem-link]: https://documentation.eccenca.com
[cmem-shield]: https://img.shields.io/endpoint?url=https://dev.documentation.eccenca.com/badge.json
[poetry-link]: https://python-poetry.org/
[poetry-shield]: https://img.shields.io/endpoint?url=https://python-poetry.org/badge/v0.json
[ruff-link]: https://docs.astral.sh/ruff/
[ruff-shield]: https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json&label=Code%20Style
[mypy-link]: https://mypy-lang.org/
[mypy-shield]: https://www.mypy-lang.org/static/mypy_badge.svg
[copier]: https://copier.readthedocs.io/
[copier-shield]: https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/copier-org/copier/master/img/badge/badge-grayscale-inverted-border-purple.json

