---
icon: lucide/terminal
---

# CLI

Whether for debugging or integration into a process where calling a Python function is complicated, `verri` exposes a
simple commandline interface that will output the same flavours of PEP-440 compliant versions:

```console
$ verri tasty pineapple
2026.1.2.dev1+a1b2c3d
```

The `tasty` in this is a required argument, if only to keep things aligned with the naming of things on the Python side.
When a command is used to create an argument to another command, the trailing newline that it outputs can be an
issue. The `-n` / `--no-newline` option is there to alleviate this, much like `echo` would:

```console
VERSION=$( verri tasty mango --no-newline )
```

!!! note
    If a command would edit a file that is tracked by git, any subsequent attempts to create a version for the
    repository in question might be marked as dirty, depending on the version flavour in use. See
    [repository hygiene during build](caveats.md#repository-hygiene-during-build).
