# TemplateConfig

TemplateConfig is a simple set of configurations that when passed enables the template engine.

!!! info
    Currently Esmerald supports `Jinja2` and `Mako`.

## Requirements

This section requires `jinja` or `mako` to be installed. You can do it so by running:

```shell
$ pip install esmerald[templates]
```

## TemplateConfig and application

To use the TemplateConfig in an application instance.

```python hl_lines="4-5 9"
{!> ../docs_src/configurations/template/example1.py!}
```

Another example

```python hl_lines="4-5 9"
{!> ../docs_src/configurations/template/example2.py!}
```

## Parameters

All the parameters and defaults are available in the [TempalteConfig Reference](../references/configurations/template.md).

## TemplateConfig and application settings

The TemplateConfig can be done directly via [application instantiation](#templateconfig-and-application)
but also via settings.

```python
{!> ../docs_src/configurations/template/settings.py!}
```

This will make sure you keep the settings clean, separated and without a bloated **Esmerald** instance.
