# AGENTS

These guidelines apply to the entire repository.

## Commit Messages
- Use the [Conventional Commits](https://www.conventionalcommits.org/) format.
- Begin each message with a type such as `feat`, `fix`, `docs`, `test`, `chore`, etc., followed by a brief description.
- Example: `feat: add shipment tracking endpoint`

## Branch Naming
- Prefix with `feat/`, `fix/`, or `chore/` followed by a short description.
Example: `feat/update-provider-client`

## Code Style
- Write clear, PEP8–compliant Python.
- Include docstrings for public modules, classes, and functions.
- Keep functions short and focused; extract helper functions when logic grows complex.

## Testing
- Ensure all unit tests pass before committing.
- Run:
  ```bash
  pytest
  
## Review Checklist
1. Code is formatted and linted. 
2. Relevant tests and documentation are updated.
3. Tests (if added) are fast and isolated; no real network I/O.
4. Commit message follows Conventional Commit style.
5. Public functions and models fully type‑annotated.
6. No provider schema leaks into domain/API responses.
7. Logs are JSON-formatted and include trace_id.
