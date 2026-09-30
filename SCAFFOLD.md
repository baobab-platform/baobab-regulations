# Implementation scaffold (2026-09-30)

This tree activates the **application scaffold** for `baobab-platform/baobab-regulations`
on top of the existing ADR-only repository.

## How to apply upstream

From a clone of `baobab-platform/baobab-regulations`:

```bash
# Preserve upstream docs/adr and any existing LICENSE / CONTRIBUTING
rsync -a --exclude '.git' --exclude 'docs/adr' path/to/this/scaffold/ .

# Resolve template leftovers
rm -f TEMPLATE-USAGE.md
rm -f .baobab/*.example .devcontainer/*.example 2>/dev/null || true

# Activate toolchain
uv sync --all-groups
cp .env.example .env
make test
make example
```

Upstream already contains:

- `docs/adr/` — ADR-REG-0001 … ADR-REG-0030
- Apache-2.0 `LICENSE`
- engine-template remnants under `.github/` (Foundation workflows may still be `.example`)

This scaffold **adds** the Python execution-plane skeleton, offline reference
evaluator for the UG→ZA coffee profile, tests, compose stack, and activated
`.baobab` / `.devcontainer` files. It does **not** replace the ADR corpus.

## Verify locally

```bash
uv sync --all-groups   # requires Python >= 3.14 (baobab-dev / uv)
make test
make example
docker compose up -d   # postgres + opa (optional for offline tests)
make run               # http://localhost:8080/healthz
```

See `docs/operations/scaffold-status.md` for activated vs deferred scope.
