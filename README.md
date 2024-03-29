# cmem-plugin-irdi

Create unique [ECLASS](https://eclass.eu/support/technical-specification/structure-and-elements/irdi) IRDIs

[![eccenca Corporate Memory](https://img.shields.io/badge/eccenca-Corporate%20Memory-orange)](https://documentation.eccenca.com)   

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
