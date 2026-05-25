---
icon: lucide/bug
---

# Caveats

Nothing is ever perfect, is it… There's a number of things listed here that are useful to keep in mind when using or
considering `verri`.

## Error handling

`verri` attempts to handle errors internally, never letting errors bubble out of its own scope, as this would break the
build step, halting any subsequent steps. As such, there's multiple levels of fallback versions used by `verri`. A
:pineapple: version, for example, calls the `git` command line to figure out the commit date and other commits on that
same date. Should anything go wrong during that, there is no real version to speak of, so two things will happen: it
falls back to a purely date-based version (:mango:, to be precise), and marks the resulting version with a
[local identifier](https://packaging.python.org/en/latest/specifications/version-specifiers/#local-version-identifiers)
indicating something went wrong. Even without anything being wrong, this can happen when someone decides to download a
ZIP file with the source of your project, no knowing the git history being omitted from such a download would normally
break the version. When such a download is used with `pip install`, for example, the project could get installed as
version *2026.1.2+vcs.missing*, referencing the day the downloaded package was built, and a marker that should give
either the user or the maintainer a hint on why that version is the way it is. Should even that fail, the ultimate
fallback version will be along the lines of *0.0+unable.to.determine.version*; still an installable and valid PEP-440
version, just not what someone might be expecting.

## Other build backends

`verri` was designed to be used with the `pdm-backend` build backend. As such, it's available versions are callable
Python functions. This might not fit other build backends very well, or at all. At the time of writing, there are no
clear plans to expand the compatibility of `verri` outside of `pdm-backend`, but that might change in the future. If
you're adventurous or otherwise curious, `verri` is pure Python and can be called from anywhere, so integration with the
rest of the world can always be made as a plain Python dependency.

## Repository hygiene during build

:strawberry: and :pineapple: versions depend on being able to query `git` for information. Aside from the
[error handling](#error-handling) in case this goes awry, the version control dependent versions are strict when it
comes to the cleanliness of the repository when a version is being created. Any change in a file tracked by `git` will
cause the created version to include a `+dirty` tag. This includes any steps in a build process that might legitimately
edit files in the repository. A build process that is dependent on changes in files like a `README.md` or a
`_version.py` somewhere should make these edits *after* `verri` determines a build version for the project.
[`pdm-backend`'s build hooks](https://backend.pdm-project.org/hooks/) can provide a way out here, as edits to metadata
are made to `pdm-backend`'s in-memory representation of the project's metadata rather than the file(s) that control it.
Likewise, any edits to tracked files after the version has already been determined will no longer cause the version to
be marked dirty.

## Fetch depth

Continuing with the requirement to interrogate `git` during version creation, many build systems will create a shallow
checkout of the source code for your project. Although this contains all of the code for a project, it can mean that
information `verri` requires for counting commits is missing, and an incorrect version is produced. This is an
unresolved issue at the time of writing, which should be tackled somewhere in the future, though this will likely always
result in issues as required information is simply not available. A fix for this is simple, however: ensure that enough
history is provided at build time. CI/CD systems often allow you to configure this as the *fetch depth*. Setting this to
0 will often fetch all history, which can be expensive for large projects. As `verri` only needs to count the number of
commits on the same day as the commit being built, setting this to a positive number high enough to cover the expected
number of merges / commits on a day should suffice. The value of that number depends on the project being built, of
course.

## Changelogs

Generating changelogs from version history is a common thing to do, which suddenly becomes complicated when the version
number depends on a similar source of information. Matching commits that merged a particular feature with the version
that would have been released with that same commit is outside of `verri`'s scope, and as such left as an exercise to
the reader :grimacing:

As `verri` is pure Python though, it can be used as a build-time dependency outside of the build backend too. In the
future, `verri` might even provide utilities to make this easier, who knows.
