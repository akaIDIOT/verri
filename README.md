# Verri version, such flavour, wow

A set of opinionated yet tasty and simple versioning schemes to set-and-forget for python projects. Using `pdm-backend`,
like this:

```toml
[build-system]
requires = ["pdm-backend", "verri"]
build-backend = "pdm.backend"

[project]
dynamic = ["version"]

[tool.pdm.version]
source = "call"
getter = "verri.tasty:pineapple"
```

There's a few flavours available:

- 🥭, `verri.tasty.mango`: a purely date-based version, like *yyyy.mm.dd*;
- 🍒, `verri.tasty.cherry`: another date-based version, less likely to create duplicates by using the number of seconds
  in the day like *yyyy.s*;
- 🍓, `verri.tasty.strawberry`: a version based on the HEAD commit date, appending a counter at the end for the number
  of commits since the HEAD commit date, like *yyyy.mm.dd.n*;
- 🍍, `verri.tasty.pineapple`: also based on the HEAD commit date, creating a 🍓 'release version' on CI environments or
  referencing the HEAD commit's hash otherwise.
