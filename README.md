# Very versions, such simple, wow

Just some utility functions to get a version for a project. Designed to be used with `pdm-backend` as such:

```toml
[build-system]
requires = ["pdm-backend", "very"]
build-backend = "pdm.backend"

[tool.pdm.version]
source = "call"
getter = "very.versions:commit_date_n1_dev"
```

More to follow. Maybe. It was trying to be simple, remember.
