# Verri version, such flavour, wow

A set of opinionated yet tasty and simple calender-based PEP-440 compliant versioning schemes to set-and-forget for
Python projects. Using `pdm-backend`, like this:

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

- 🥭, `verri.tasty.mango`: a purely date-based version, like *2026.1.2*;
- 🍒, `verri.tasty.cherry`: another date-based version, less likely to create duplicates by using the number of seconds
  in the day like *2026.12345*;
- 🍓, `verri.tasty.strawberry`: a version based on the HEAD commit date, appending a counter at the end for the number
  of commits since the HEAD commit date, like *2026.1.2.0*;
- 🍍, `verri.tasty.pineapple`: also based on the HEAD commit date, creating a 'release version' much like the strawberry
  flavour on CI/CD environments or referencing the HEAD commit's hash otherwise, like *2026.1.2* or *2026.1.2+a1b2c3d*.

Note that the commit-based versions assume your project is using `git`, and `git` is available as a command line tool.
Both of these flavours will mark the version as "dirty" if tracked files contain uncommited changes when the version is
being established. The 🍍 flavour will consider a version a release if the following is true:

- a build is being run on a CI/CD environment (detected through environment variables);
- the repository is considered clean when the version is determined;
- the build is run for the repository's default branch.

As `verri` is designed to be simple, it's great for projects that don't want or need to follow semantic version, but
also don't want to keep building *0.1.0* forever. If your project needs a version that makes a clear reference to a
point in time, and you don't want to have to think about it again, verri could be great for you! If you need a
semantically meaningful version or want to control the version number manually, verri might not be great for you.

`verri` was created with `pdm-backend` in mind, so deliberately exposes it's flavours as callable functions. See
[`pdm-backed`'s documentation](https://backend.pdm-project.org/metadata/#dynamic-project-version) for more information
on how this can be configured for your project. Other build systems might be able to use verri as well; there's no
dependencies on PDM anywhere, and the versions are simple Python functions.
