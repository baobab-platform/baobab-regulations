# Contributing

This repository follows the `baobab-platform` organisation's standard workflow:

- All changes land through a pull request against `main` — no direct pushes.
- At least one CODEOWNERS-required review is mandatory (see
  `.github/CODEOWNERS`); files shared with `baobab-platform/shared` contracts may
  require two.
- Required CI status checks (once activated — see Foundation workflows) must
  pass before merge.
- Development happens inside the `baobab-dev` devcontainer declared in
  `.devcontainer/devcontainer.json` — see that file and
  `.baobab/environment.yaml` for the exact toolchain this repo expects.
- Keep `CHANGELOG.md` current — add one once this repo starts cutting
  releases; it doesn't need one while still scaffolded.

Local verification for the implementation scaffold:

```bash
uv sync --all-groups
make test
make example
```
