# Contributing

Contributions are welcome! Please open a pull request against the `main` branch.

## Development Setup

1. Fork and clone the repository:

   ```bash
   git clone https://github.com/<your-username>/ha-mempool-integration.git
   cd ha-mempool-integration
   ```

2. Create a feature branch:

   ```bash
   git checkout -b my-feature
   ```

3. Install linting dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Run linting locally before committing:

   ```bash
   ruff check .
   ruff format . --check
   ```

5. Auto-fix lint and formatting issues:

   ```bash
   ruff check . --fix
   ruff format .
   ```

## Local Testing in Home Assistant

Copy (or symlink) the integration into your HA config directory:

```bash
cp -r custom_components/mempool /path/to/ha-config/custom_components/
```

Restart Home Assistant after each change.

## Submitting a Pull Request

1. Push your branch to your fork.
2. Open a pull request against `main` on the upstream repository.
3. CI will automatically run HACS validation, hassfest, and linting checks — all must pass.
4. Describe what your change does and why.

## CI Workflows

| Workflow | Trigger | Purpose |
|---|---|---|
| **Validate** | Push/PR to `main`, daily, manual | HACS validation and hassfest checks |
| **Lint** | Push/PR to `main` | Ruff linting and format checks |

## License

By contributing, you agree that your contributions will be licensed under the [MIT License](LICENSE).
