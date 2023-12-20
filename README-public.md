# cmem-plugin-irdi

Create unique [ECLASS](https://eclass.eu/support/technical-specification/structure-and-elements/irdi) IRDIs


This is a plugin for [eccenca](https://eccenca.com) [Corporate Memory](https://documentation.eccenca.com).

You can install it with the [cmemc](https://eccenca.com/go/cmemc) command line
clients like this:

```
cmemc admin workspace python install cmem-plugin-irdi
```

## Plugin Usage

- All fields of the IRDI are configurable, minus `Item Code`, which is created by the plugin
  - Created IRDIs are unique per configuration
- Specify a graph that stores the state of `Item Codes`
- Input and output paths are configurable
  - if no input path is configured, values are read from the URIs of the input (Transformation Input)