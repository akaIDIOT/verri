---
icon: lucide/citrus
---

# Getting started

`verri` is an opinionated, yet simple tool to add a PEP-440 compliant calendar versioning (or
[CalVer](https://calver.org/)) scheme to your Python project. It was made to integrate with `pdm-backend`'s way to
declare and use a dynamic version:

```toml title="pyproject.toml" hl_lines="2 6 10"
[build-system]
requires = ["pdm-backend", "verri"]  # add dependency (1)
build-backend = "pdm.backend"

[project]
dynamic = ["version"]  # dynamic version (2)

[tool.pdm.version]
source = "call"
getter = "verri.tasty:pineapple"  # such flavour (3)
```

1. Add `verri` tot the list of required dependencies for the build system, so any tool you're using to install
   your project will know to install both `pdm-backend` and `verri` before letting `pdm.backend` build your project.

2. Declare the version of the project to be dynamic, telling the build backend (`pdm-backend` in this case) to expect
   additional configuration to resolve a version in a way other than typing it directly into the project's
   `pyproject.toml` file.

3. `pdm-backend` enables you to call a function at build time to determine a version. This is where `verri` comes in,
   [select a function](#choosing-a-flavour) for `pdm-backend` to call, and you're off :rocket:!

If all you're interested in is adding a calendar versioning scheme to your project, you could stop reading here. If
you're interested in the options, the why and things to look out for, read on.

## Choosing a flavour

## What's with the fruit?
