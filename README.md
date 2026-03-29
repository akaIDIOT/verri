# Verri version, such flavour, wow

A set of opinionated yet tasty and simple versioning schemes to set-and-forget for python projects. Using `pdm-backend`,
like this:

```toml
[build-system]
requires = ["pdm-backend", "verri"]
build-backend = "pdm.backend"

[tool.pdm.version]
source = "call"
getter = "verri.tasty:strawberry"
```

More to follow. Maybe. It was trying to be simple, remember.
