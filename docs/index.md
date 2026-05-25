---
icon: lucide/citrus
---

# Verri version, such flavour, wow

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
   [select a function](#choosing-a-flavour) for `pdm-backend` to call, and you're off :pineapple:!

If all you're interested in is adding a calendar versioning scheme to your project, you could stop reading here. If
you're interested in the options, the why and things to look out for, read on.

## Choosing a flavour

Looking at the example `pyproject.toml` snippet above, the actual version being determined at build time is `verri`'s
"pineapple" flavour; tasty! `verri` currently provies 4 flavours, based either on the current date, or on the date of
the commit being built. There's two flavours based on "today", the current date[^utc]:

[^utc]: `verri` will **always** use the UTC timezone when dealing with dates and times, including counting the number of
    seconds or commits since midnight.

- :mango:, or `verri.tasty:mango`: an ISO-formatted date, without leading zeroes to make it PEP-440 compliant;
- :cherries:, or `verri.tasty:cherry`: similar to the :mango:, but adding the number of seconds since midnight to avoid
  creating the same version twice.

Let's say the current date is the 2nd of January 2026, our :mango: version would be *2026.1.2*. A second release on the
same day would create the same version number, which might cause problems. Our :cherries: version, however, would add a
fourth component and thus be different, assuming the builds for the two releases weren't running simultaneous.

Using just the build date or timestamp as a version can be useful, but using the *commit date*[^utc] of a release is
even better. That way, when a release is rebuilt later, it would arrive at the same version as any previous build of the
same commit. `verri` provides that exact thing in two different flavours:

- :strawberry:, or `verri.tasty:strawberry`: the commit date being built as an ISO-formatted date, suffixed with the
  number of commits before it on the same day;
- :pineapple:, or `verri.tasty:pineapple`: similar to the :strawberry:, with the added requirement that only a "release"
  version will be created if the build is being performed
    1. on a CI/CD environment (like GitHub Actions, or GitLab CI/CD, determined through environment variables);
    1. while the repository is clean, no files that are tracked by `git` are modified when the version is determined;
    1. on the project's default branch (either the explicitly configured one, or `main` / `master`).

So when the merge commit of the latest feature was made on the 3rd of April 2026, our :strawberry: version would be
*2026.3.4.0*, or *2026.3.4.1* if it wasn't the first, and so on. A :pineapple: version will omit the final *.0*, but
number subsequent releases on the same day in the same way. Any build using a :pineapple: version not being performed on
a CI/CD environment, however, would result in a version like *2026.3.4.dev1+a1b2c3d*, referencing the commit hash for
the commit being built instead and putting the commit counter for the day up as a development version.

Additionally, both :strawberry: and :pineapple: flavours will mark the version with a `+dirty`
[local identifier](https://packaging.python.org/en/latest/specifications/version-specifiers/#local-version-identifiers)
if the repository isn't clean when the version is determined. The :pineapple: version is the most complex of all of the
options `verri` provides, but also the most meaningful. It is meant to provide a function version for anyone building a
project locally, but only creating a releasable version number when an actual release is being made. `verri` won't
change anything about a project itself, but a locally built or installed version will be distinguishable from one that
was meant to be a release.

Choosing a version that fits your project best is up to you. When in doubt, it might help to know that the way a
:pineapple: version works is the reason `verri` was created :wink:

## What's with the fruit?

Good question… Initially, discussion around versions would refer to a template like `yyyy.mm.dd` as an ISO-date version,
or something along those lines. As that same discussion went on, however, the added requirements being included in
determining what version to use in which circumstances, made the names of these templates cumbersome. After trying to
explain `isodate_num_or_commit_when_local` to others, the template names took the complete opposite direction and
started using names that are easy to say and remember, even if they are meaningless on their own. Using the names of
fruit, it's clear that these functions have something in common, and it allows `verri` to call them tasty :yum:
